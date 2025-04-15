try:
    from importlib.metadata import version
    __version__ = version("quine-observer-jtag")
except Exception:
    __version__ = "unknown"
