"""Utility functions for handling paths and Python imports."""
import os
import sys
import inspect
from typing import Optional, Union


def setup_root(n_up: int = 0, return_root: bool = False, verbose: bool = False) -> Optional[str]:
    """
    Add the root directory to the sys.path (PYTHONPATH).
    
    Args:
        n_up: Number of directories to go up (0 - current directory)
        return_root: If True, return the root directory
        verbose: If True, print the root directory
    
    Returns:
        Optional[str]: The root directory path if return_root is True, otherwise None
        
    Raises:
        RuntimeError: If called from an IPython/Jupyter environment
    
    Note:
        This function will consider the directory of the caller.
        If you call this function from a file $DIR/file.py, it will add $DIR to sys.path given n_up=0
    
    Example:
        >>> from src.utils.path_handler import setup_root
        >>> setup_root(n_up=1)  # Adds parent directory to sys.path
    """
    _raise_error_if_in_ipython("setup_root is not designed to be used in a Jupyter Notebook")
    
    # Get the caller's filename
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    caller_dir = os.path.dirname(caller_filename)
    
    # Calculate the root directory
    root_dir = os.path.abspath(os.path.join(caller_dir, *['..' for _ in range(n_up)]))
    
    # Add to sys.path if not already there
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    
    if verbose:
        print(f"Added {root_dir} to sys.path")
    
    if return_root:
        return root_dir
    return None


def _raise_error_if_in_ipython(msg: str) -> None:
    """
    Raise an error if the code is running in IPython.
    
    Args:
        msg: The error message to display
        
    Raises:
        RuntimeError: If running in an IPython environment
    """
    try:
        get_ipython()  # type: ignore
        raise RuntimeError(msg)
    except NameError:
        # get_ipython doesn't exist, so not running in IPython.
        pass