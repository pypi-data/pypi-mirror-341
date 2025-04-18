"""Collection of tests to test access on profiling data."""

from pathlib import Path

import pandas as pd
import pytest

from postopus import Run


def test_profiling_file(methane_run: Path):
    run = Run(methane_run)
    data = run.default.profiling.time()

    assert isinstance(data, pd.DataFrame)
    # we cannot test for actual values, but we can check for a few
    # column and index names
    assert "CUM NUM_CALLS" in data.columns
    assert "CUM TOTAL_TIME" in data.columns
    assert "COMPLETE_RUN" in data.index


def test_profiling_file_multisystem(celestial_bodies_run: Path):
    run = Run(celestial_bodies_run)
    data = run.default.profiling.time()

    assert isinstance(data, pd.DataFrame)
    # we cannot test for actual values, but we can check for a few
    # column and index names
    assert "CUM NUM_CALLS" in data.columns
    assert "CUM TOTAL_TIME" in data.columns
    assert "COMPLETE_RUN" in data.index

    # make sure profiling data is only available on the default system
    with pytest.raises(AttributeError):
        run.SolarSystem.profiling.time()
