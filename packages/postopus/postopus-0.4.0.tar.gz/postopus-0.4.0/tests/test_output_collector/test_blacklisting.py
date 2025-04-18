import logging
import os
import re
import shutil
from pathlib import Path

import pytest

from postopus.output_collector import OutputCollector


@pytest.fixture
def run_with_weird_files(methane_run: Path, testdata_dir: Path):
    targetpath = testdata_dir / "methane_with_additional_files"
    target = targetpath / methane_run.name
    gitignore_file = targetpath / ".gitignore"

    # Check if there is something to do or everything is up to date.
    # Use the .gitignore file to get the timestamp.
    if (
        targetpath.exists()
        and gitignore_file.exists()
        and gitignore_file.stat().st_mtime >= methane_run.stat().st_mtime
        and gitignore_file.stat().st_mtime >= Path(__file__).stat().st_mtime
    ):
        return target

    if targetpath.exists():
        shutil.rmtree(targetpath)

    shutil.copytree(methane_run, target, copy_function=os.link)
    (target / ".DS_Store").touch()
    (target / "static" / ".DS_Store").touch()
    (target / "td.general" / ".DS_Store").touch()
    (target / "output_iter" / ".DS_Store").touch()
    (target / "output_iter" / "td.0000000" / ".DS_Store").touch()
    (target / "output_iter" / "__pycache__").mkdir()
    (target / "processdata.ipynb").touch()
    (target / "processdata.py").touch()
    (target / "__pycache__").mkdir()
    (target / "__pycache__" / "processdata.pyc").touch()

    # These specific files are not blacklisted by default, but the output
    # collector should ignore them either way (emmiting a waring).
    for directory in [
        (target / "output_iter" / "foo"),
        (target / "output_iter" / "foo.bar"),
        (target / "output_iter" / "foo.bar.baz"),
    ]:
        directory.mkdir()
        (directory / "testfile.vtk").touch()

    # Create a dummy file to know if timestamps of the source are newer for
    # the next run. (Doesnt work directly by getting any timestamp of the
    # duplicated folder as os.link is used...). As we should place a proper
    # .gitignore inside anyway combine this.
    gitignore_file.write_text(f"# created by {Path(__file__).name}\n*")

    return target


def test_output_collector_blacklist(run_with_weird_files: Path, caplog):
    caplog.set_level(logging.WARNING)
    oc = OutputCollector(run_with_weird_files)
    assert "Skipping folder" in caplog.text
    assert "output_iter/foo" in caplog.text
    assert "output_iter/foo.bar" in caplog.text
    assert "output_iter/foo.bar.baz" in caplog.text
    # The folder __pycache__ should be ignored by the output collector and not result in a warning.
    assert "__pycache__" not in caplog.text

    output = oc.output
    assert output.keys() == {"default"}
    assert output["default"].keys() == {
        "scf",
        "td",
        "profiling",
    }
    # Check the expected outputs. We especially do not expect an output like ".DS_Store".
    assert output["default"]["scf"].keys() == {
        "info",
        "wf",
        "density",
        "forces",
        "convergence",
    }
    assert output["default"]["td"].keys() == {
        "wf",
        "density",
        "multipoles",
        "laser",
        "current",
        "energy",
    }

    # Make sure that with debug logs enabled we get the information about ignored folders.
    caplog.set_level(logging.DEBUG)
    oc = OutputCollector(run_with_weird_files)
    assert re.search(r"Ignoring file .*\.DS_Store ", caplog.text)
    assert re.search(r"Ignoring folder .*__pycache__ ", caplog.text)
