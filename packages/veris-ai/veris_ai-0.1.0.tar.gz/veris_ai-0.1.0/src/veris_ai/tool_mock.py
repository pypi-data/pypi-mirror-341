import inspect
import json
import logging
import os
from collections.abc import Callable
from functools import wraps
from typing import Any, Union, get_type_hints

import httpx

logger = logging.getLogger(__name__)

class ToolMock:
    """Class for mocking tool calls."""
    def __init__(self):
        self.endpoint = os.getenv("VERIS_MOCK_ENDPOINT_URL")
        if not self.endpoint:
            raise ValueError("VERIS_MOCK_ENDPOINT_URL environment variable is not set")
        # Default timeout of 30 seconds
        self.timeout = float(os.getenv("VERIS_MOCK_TIMEOUT", "30.0"))

    def _convert_to_type(self, value: Any, target_type: type) -> Any: # type: ignore
        """Convert a value to the specified type."""
        if target_type == Any:
            return value
            
        # Handle basic types
        if target_type in (str, int, float, bool):
            return target_type(value)
            
        # Handle List types
        if hasattr(target_type, "__origin__") and target_type.__origin__ == list:
            if not isinstance(value, list):
                raise ValueError(f"Expected list but got {type(value)}")
            item_type = target_type.__args__[0]
            return [self._convert_to_type(item, item_type) for item in value]
            
        # Handle Dict types
        if hasattr(target_type, "__origin__") and target_type.__origin__ == dict:
            if not isinstance(value, dict):
                raise ValueError(f"Expected dict but got {type(value)}")
            key_type, value_type = target_type.__args__
            return {self._convert_to_type(k, key_type): self._convert_to_type(v, value_type) 
                   for k, v in value.items()}
            
        # Handle Union types
        if hasattr(target_type, "__origin__") and target_type.__origin__ == Union:
            for possible_type in target_type.__args__:
                try:
                    return self._convert_to_type(value, possible_type)
                except (ValueError, TypeError):
                    continue
            raise ValueError(f"Could not convert {value} to any of the union types {target_type.__args__}") # noqa
            
        # For other types, try direct conversion
        return target_type(value)

    def mock(self, func: Callable) -> Callable:
        """Decorator for mocking tool calls."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Check if we're in simulation mode
            env_mode = os.getenv("ENV", "").lower()
            if env_mode != "simulation":
                # If not in simulation mode, execute the original function
                return await func(*args, **kwargs)

            logger.info(f"Simulating function: {func.__name__}")
            sig = inspect.signature(func)
            type_hints = get_type_hints(func)
            
            # Extract return type object (not just the name)
            return_type_obj = type_hints.pop("return", Any)
            
            # Create parameter info
            params_info = {}
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            for param_name, param_value in bound_args.arguments.items():
                params_info[param_name] = {
                    "value": param_value,
                    "type": type_hints.get(param_name, Any).__name__,
                }

            # Get function docstring
            docstring = inspect.getdoc(func) or ""

            ctx = bound_args.arguments.pop('ctx', None)
            session_id = None
            if ctx:
                try:
                    session_id = ctx.request_context.lifespan_context.session_id
                except AttributeError:
                    logger.warning("Cannot get session_id from context.")

            # Prepare payload
            payload = {
                "session_id": session_id,
                "tool_call": {
                    'function_name': func.__name__,
                    'parameters': params_info,
                    'return_type': return_type_obj.__name__,
                    'docstring': docstring,
                }
            }

            # Send request to endpoint with timeout
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.endpoint, json=payload)
                response.raise_for_status()
                mock_result = response.json()["result"]
                logger.info(f"Mock response: {mock_result}")
                
                # Parse the mock result if it's a string
                if isinstance(mock_result, str):
                    try:
                        mock_result = json.loads(mock_result)
                    except json.JSONDecodeError:
                        # If it's not valid JSON, treat it as a raw string
                        pass
                
                # Convert the mock result to the expected return type
                return self._convert_to_type(mock_result, return_type_obj)

        return wrapper

veris = ToolMock()
