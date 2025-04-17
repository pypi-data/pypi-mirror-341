import importlib
import pytest

submodules = [
    "config",
    "csv",
    "email",
    "file",
    "function",
    "github",
    "local",
    "markdown",
    "ml",
    "ocr",
    "report",
    "serialization",
    "text",
]

@pytest.mark.parametrize("submodule", submodules)
def test_import_pyfunc2_submodule(submodule):
    modname = f"pyfunc2.{submodule}"
    try:
        importlib.import_module(modname)
    except Exception as e:
        pytest.fail(f"Import failed for {modname}: {e}")
