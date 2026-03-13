"""
Auto-generated data file from : economy.n_workers_full_time
Generated at: 2026-03-08T14:59:20.398583
Rows: 2
Columns: ['group', 'n_workers_full_time']
"""

import polars as pl

METADATA = {
    "source": "economy.n_workers_full_time",
    "generated_at": "2026-03-08T14:59:20.398583",
    "row_count": 2,
    "filter_options": {
        "group": ['bottom_50', 'top_1'],
    },
    "kpis": {
        "n_workers_full_time_sum": 69395788.03702487,
        "n_workers_full_time_mean": 34697894.02,
        "n_workers_full_time_min": 2016187.6679,
        "n_workers_full_time_max": 67379600.36912487,
    },
}

n_workers_full_time = pl.DataFrame({
    "group": [
        "top_1", "bottom_50",
    ],
    "n_workers_full_time": [
        2016187.6679, 67379600.36912487,
    ],
})
