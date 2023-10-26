import sys

def eprint(*args, **kwargs):
    """
    Print to stderr

    Args:
        *args: The arguments to print
        **kwargs: The keyword arguments to print
    
    Returns:
        None
    """
    print(*args, file=sys.stderr, **kwargs)