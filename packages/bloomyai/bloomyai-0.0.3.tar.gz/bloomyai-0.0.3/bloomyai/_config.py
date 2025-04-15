# Private variable to store credentials
_credentials = {
    "api_key": None,
    "base_url": None,
}


def set_credentials(
    api_key: str | None,
    base_url: str | None,
):
    """
    Sets the credentials in our private _credentials dict.
    This function is used internally by init() to store credentials securely.
    """
    global _credentials
    _credentials = {
        "api_key": api_key,
        "base_url": base_url,
    }


def get_credentials():
    """
    Returns the _credentials dict.
    For internal use only.
    """
    return _credentials
