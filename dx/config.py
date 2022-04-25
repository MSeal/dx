import os


def in_noteable_env() -> bool:
    """
    Check if we are running in a Noteable environment.

    FUTURE: this will be used to determine whether IPython formatters
    are automatically updated.
    """
    return "NTBL_USER_ID" in os.environ


def in_nteract_env() -> bool:
    # TODO: handle this?
    return False
