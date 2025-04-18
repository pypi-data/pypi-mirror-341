# flake8: noqa: I003
from functools import wraps
import queue
import threading
import time
import traceback
from typing import Callable, Optional, TypeVar

from fabric.functions.udf_exception import UserDataFunctionTimeoutError
from fabric.internal.logging import UdfLogger
from fabric.internal.decorators.function_parameter_keywords import CONTEXT_PARAMETER

from .constants import Timeout

import asyncio
import inspect
import functools

T = TypeVar('T')

logger = UdfLogger(__name__)

def add_timeout(func: Callable[..., T], function_timeout: int = Timeout.FUNC_TIMEOUT_IN_SECONDS):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # This will raise a TimeoutError if the function takes longer than the timeout
            if inspect.iscoroutinefunction(func):
                return await asyncio.wait_for(func(*args, **kwargs), function_timeout)
            else:
                loop = asyncio.get_event_loop()
                return await asyncio.wait_for(loop.run_in_executor(None, functools.partial(func, *args, **kwargs)), function_timeout)
        except asyncio.TimeoutError:
            return UserDataFunctionTimeoutError(function_timeout)
        
    return wrapper