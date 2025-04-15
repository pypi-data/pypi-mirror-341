try:
    from importlib.metadata import version
    __version__ = version("quine-meta")
except Exception:
    __version__ = "unknown"
