try:
    from importlib.metadata import version
    __version__ = version("quine-target-aarch64")
except Exception:
    __version__ = "unknown"
