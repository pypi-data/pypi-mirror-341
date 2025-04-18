import threading
from collections.abc import Callable


class Interval(threading.Thread):
    """Call a function on an interval.
    
    This does not account for the time it takes to run the function, so it's
    really interval seconds since the completion of the previous run.
    
    Parameters
    ----------
    interval : float
        The number of seconds to wait
    function : callable
        The function to run
    args : tuple, optional
        The arguments to pass to the function
    kwargs : dict, optional
        The keyword arguments to pass to the function
        
    Examples
    --------
    >>> t = Interval(30.0, f, args=None, kwargs=None)
    >>> t.start()
    >>> t.cancel()
    """
    def __init__(
        self,
        interval: float,
        function: Callable[[], None],
        args: tuple = None,
        kwargs: dict = None,
    ):
        threading.Thread.__init__(self)
        self.daemon = True
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = threading.Event()

    def cancel(self):
        """Stop the interval."""
        self.finished.set()

    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            if not self.finished.is_set():
                self.function(*self.args, **self.kwargs)


# Wrappers - similar to setInterval/clearInterval in JS
def set_interval(
    func: Callable[[], None],
    seconds: float,
    args: tuple = None,
    kwargs: dict = None,
) -> Interval:
    """Set an interval to call a function every N seconds and start it.
    
    Parameters
    ----------
    func : callable
        The function to call
    seconds : float
        The number of seconds to wait between calls
    args : tuple, optional
        The arguments to pass to the function
    kwargs : dict, optional
        The keyword arguments to pass to the function
        
    Returns
    -------
    Interval
        The interval object
        
    Examples
    --------
    >>> my_interval = set_interval(lambda: print("Hello, world!"), 1.0)
    >>> # Do other stuff...
    >>> my_interval.cancel()  # or clear_interval(my_interval)
    """
    interval = Interval(seconds, func, args, kwargs)
    interval.start()
    return interval


def clear_interval(interval: Interval):
    """Clear an interval.
    
    Parameters
    ----------
    interval : Interval
        The interval to clear
        
    Examples
    --------
    >>> my_interval = set_interval(lambda: print("Hello, world!"), 1.0)
    >>> # Do other stuff...
    >>> clear_interval(my_interval)
    """
    interval.cancel()