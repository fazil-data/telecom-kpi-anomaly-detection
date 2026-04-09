import numpy as np
import pandas as pd

from src.config import EPSILON


def add_rolling_baseline(
    df: pd.DataFrame,
    value_col: str,
    lookback_hours: int,
    min_history_points: int,
) -> pd.DataFrame:
    """
    For each cell, compute rolling baseline statistics using only prior values.
    """
    work = df.copy()

    median_col = f"{value_col}_baseline_median"
    mad_col = f"{value_col}_baseline_mad"
    mean_col = f"{value_col}_baseline_mean"
    std_col = f"{value_col}_baseline_std"
    count_col = f"{value_col}_history_count"

    def per_cell(group: pd.DataFrame) -> pd.DataFrame:
        s = group[value_col].astype(float)

        shifted = s.shift(1)
        rolling_obj = shifted.rolling(window=lookback_hours, min_periods=min_history_points)

        baseline = pd.DataFrame(index=group.index)
        baseline[median_col] = rolling_obj.median()
        baseline[mad_col] = rolling_obj.apply(
            lambda x: np.median(np.abs(x - np.median(x))),
            raw=True,
        )
        baseline[mean_col] = rolling_obj.mean()
        baseline[std_col] = rolling_obj.std(ddof=0)
        baseline[count_col] = rolling_obj.count()

        baseline[mad_col] = baseline[mad_col].fillna(0.0)
        baseline[std_col] = baseline[std_col].fillna(0.0)

        return baseline

    baseline_df = (
        work.groupby("cell_id", group_keys=False, observed=True)
        .apply(per_cell)
        .reset_index(level=0, drop=True)
    )

    work = pd.concat([work, baseline_df], axis=1)
    work[mad_col] = work[mad_col].clip(lower=EPSILON)
    work[std_col] = work[std_col].clip(lower=EPSILON)

    return work
