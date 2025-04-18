from __future__ import annotations

import pandas as pd

from ._base import OutputProxy


class ProfilingOutput(OutputProxy):
    """Proxy for profiling output in run/profiling/time.000000"""

    __output__ = "time"

    def __call__(self) -> pd.DataFrame:
        columns = [
            "TAG",
            "CUM NUM_CALLS",
            "CUM TOTAL_TIME",
            "CUM TIME_PER_CALL",
            "CUM MIN_TIME",
            "CUM MFLOPS",
            "CUM MBYTES/S",
            "CUM %TIME",
            "|",
            "SELF TOTAL_TIME",
            "SELF TIME_PER_CALL",
            "SELF MFLOPS",
            "SELF MBYTES/S",
            "SELF %TIME",
        ]

        return pd.read_table(
            list(self._output_field.files)[0],
            sep=r"\s+",
            names=columns,
            skiprows=4,
            index_col="TAG",
            usecols=lambda x: x != "|",
        )
