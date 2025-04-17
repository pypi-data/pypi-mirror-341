import inspect


async def ensure_awaitable(func, *args, **kwargs):
    """
    Ensures a function call returns an awaitable result.
    Works with both synchronous and asynchronous functions.

    Args:
        func: The function to call
        *args, **kwargs: Arguments to pass to the function

    Returns:
        The awaited result of the function
    """
    result = func(*args, **kwargs)

    if inspect.isawaitable(result):
        return await result
    return result
