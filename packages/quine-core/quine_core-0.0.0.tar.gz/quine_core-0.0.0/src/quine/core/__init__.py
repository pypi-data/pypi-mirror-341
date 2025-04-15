try:
    from importlib.metadata import version
    __version__ = version("quine-core")
except Exception:
    __version__ = "unknown"
