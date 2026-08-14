from typing import Any, Callable
import time
from constrain_llm.config.logging import get_logger



def timed_call(
    func: Callable[..., Any], 
    msg_stem:str ='Function call completed in', 
    *args, 
    **kwargs
) -> tuple[Any, float]:
    logger = get_logger(func.__name__)
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    logger.info(f'{msg_stem} {elapsed:.3f}s.')
    return result