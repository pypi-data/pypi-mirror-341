try:
    from importlib.metadata import version
    __version__ = version("quine-runtime-qemu")
except Exception:
    __version__ = "unknown"
