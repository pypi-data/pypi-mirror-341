try:
    from importlib.metadata import version
    __version__ = version("quine-target-subleq")
except Exception:
    __version__ = "unknown"
