import functools
import time
from logging import Logger
from typing import Callable


def log_debug(msg: str, logger: Logger = None, **kwargs):
    if logger:
        logger.debug(msg, **kwargs)
    else:
        print(msg)


def on_fail(**kwargs):
    delay = kwargs["cdelay"]
    logger = kwargs.get("logger")
    msg = f"Sleeping for {delay} secconds."
    log_debug(msg, logger)
    time.sleep(delay)


def producer_on_fail(**kwargs):
    producer_kwarg = "producer"
    delay = kwargs["cdelay"]
    logger = kwargs.get("logger")
    producer_instance = kwargs["args"][0] # magic:(hacky way to get the producer)
    producer = getattr(producer_instance, producer_kwarg, None)
    assert producer is not None
    msg = f"Polling with timeout: {delay} seconds"
    log_debug(msg, logger)
    producer.poll(delay)


def retry(times: int,
          logger: Logger = None,
          delay: int = 2,
          backoff: int = 5,
          on_fail : Callable = on_fail):
    """Retry decorator implementating exponential backfff

    Args:
        times: Number of times to run the code. If times=3, it will catch the exception the first 2 times and tries to run it.
                The last time it doesn't catch the exception.
        logger: logger to log the error
        delay: delay between retries
        backoff: multiplier to delay
        on_fail: first class function that is to be run after a failed attempt.

    """
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            current_iter, cdelay = 1, delay
            msg = "method: {func.__name__} [Try number: {current_iter}/{times} times]."
            success_msg = "method: {func.__name__} success."
            failed_msg = "method: {func.__name__} failed."

            while current_iter <= times:

                log_debug(msg.format(**locals()), logger=logger)
                try:
                    result = func(*args, **kwargs)
                    log_debug(msg=success_msg.format(**locals()), logger=logger)
                    return result
                except Exception as e:
                    log_debug(msg=failed_msg.format(**locals()),
                              exc_info=True,
                              logger=logger)
                    current_iter += 1

                    if current_iter > times:
                        # No error handling for the last time
                        # Reraise the error
                        raise

                    on_fail(**locals())
                    cdelay *= backoff

        return wrapper_retry

    return decorator_retry
