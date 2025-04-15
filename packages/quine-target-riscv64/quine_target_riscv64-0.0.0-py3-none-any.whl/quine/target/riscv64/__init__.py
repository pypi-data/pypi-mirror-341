try:
    from importlib.metadata import version
    __version__ = version("quine-target-riscv64")
except Exception:
    __version__ = "unknown"
