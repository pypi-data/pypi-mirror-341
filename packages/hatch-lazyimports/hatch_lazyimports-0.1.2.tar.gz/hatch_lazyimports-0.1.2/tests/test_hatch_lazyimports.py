from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest
from hatchling.metadata.core import ProjectMetadata
from hatchling.plugin.manager import PluginManager
from packaging.metadata import Metadata

if TYPE_CHECKING:
    from hatch_lazyimports.lazyimports_hook import LazyimportsHook


PYPROJECT_TOML = """\
[build-system]
requires = ['hatchling', 'hatch-lazyimports']
build-backend = 'hatchling.build'

[project]
name = 'cowboy'
version = '1.0'
dynamic = ['entry-points', 'entry-points.lazyimports']
requires-python = '>=3.9'

[tool.hatch.metadata.hooks.lazyimports]
entry_point_name = "test_lazyimports"

[tool.hatch.build.targets.wheel]
packages = ["src/cowboy"]
sources = ["src"]
"""


PYTHON_FILE = """\
from lazyimports import lazy_imports

with lazy_imports():
    from my_module import MyClass
    import other_module

__version__ = "1.0"
__all__ = ["other_module"]
"""


@pytest.fixture()
def project_path(tmp_path: Path) -> Path:
    project_path = tmp_path / "cowboy"
    pkg_file_path = project_path.joinpath("src/cowboy/__init__.py")

    pkg_file_path.parent.mkdir(parents=True, exist_ok=True)

    project_path.joinpath("pyproject.toml").write_text(PYPROJECT_TOML)
    pkg_file_path.write_text(PYTHON_FILE)

    return project_path


@pytest.fixture
def hook(project_path: Path) -> LazyimportsHook:
    pm = PluginManager()
    pm.metadata_hook.collect(include_third_party=True)
    plugin = pm.manager.get_plugin("lazyimports")
    hook_cls = plugin.hatch_register_metadata_hook()

    return hook_cls(project_path, {})


@pytest.fixture
def metadata(project_path: Path) -> tuple[LazyimportsHook, dict[str, Any]]:
    return ProjectMetadata(project_path, None).config["project"]


def test_basic(hook: LazyimportsHook, metadata: dict) -> None:
    hook.update(metadata)

    value = metadata["entry-points"]["lazyimports"]["lazyimports_auto"]
    assert value == "~cowboy,my_module,other_module,my_module:MyClass#2"


def test_end_to_end(project_path: Path, tmp_path: Path) -> None:
    import zipfile
    import configparser

    from build.__main__ import build_package

    out_dir = tmp_path / "dist"
    build_package(
        srcdir=project_path,
        outdir=out_dir,
        distributions=["wheel"],
        isolation=False,
    )

    entry_points = configparser.ConfigParser()
    with zipfile.ZipFile(out_dir / "cowboy-1.0-py3-none-any.whl", "r") as whl:
        assert "cowboy-1.0.dist-info/entry_points.txt" in whl.namelist()
        metadata = Metadata.from_email(
            whl.open("cowboy-1.0.dist-info/METADATA").read().decode("utf-8")
        )
        entry_points.read_string(
            whl.open("cowboy-1.0.dist-info/entry_points.txt").read().decode("utf-8")
        )

    assert metadata.name == "cowboy"
    assert "lazyimports" in entry_points.sections()
