try:
    from importlib.metadata import version
    __version__ = version("quine-observer-qemu")
except Exception:
    __version__ = "unknown"
