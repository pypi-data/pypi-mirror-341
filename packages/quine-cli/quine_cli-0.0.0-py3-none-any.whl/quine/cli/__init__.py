try:
    from importlib.metadata import version
    __version__ = version("quine-cli")
except Exception:
    __version__ = "unknown"
