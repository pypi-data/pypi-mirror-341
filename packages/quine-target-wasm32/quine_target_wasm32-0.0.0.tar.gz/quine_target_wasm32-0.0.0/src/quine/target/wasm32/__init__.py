try:
    from importlib.metadata import version
    __version__ = version("quine-target-wasm32")
except Exception:
    __version__ = "unknown"
