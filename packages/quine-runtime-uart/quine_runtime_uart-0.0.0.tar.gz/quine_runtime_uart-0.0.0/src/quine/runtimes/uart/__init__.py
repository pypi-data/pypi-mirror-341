try:
    from importlib.metadata import version
    __version__ = version("quine-runtime-uart")
except Exception:
    __version__ = "unknown"
