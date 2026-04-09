import numpy as np
import pandas as pd

from src.config import EPSILON, LOWER_IS_BAD_KPIS, UPPER_IS_BAD_KPIS


def add_anomaly_score(
    df: pd.DataFrame,
    value_col: str,
    threshold: float,
) -> pd.DataFrame:
    """
    Add robust anomaly scoring based on rolling median and MAD.
    """
    out = df.copy()

    median_col = f"{value_col}_baseline_median"
    mad_col = f"{value_col}_baseline_mad"
    count_col = f"{value_col}_history_count"

    score_col = f"{value_col}_anomaly_score"
    diff_col = f"{value_col}_baseline_diff"
    flag_col = f"{value_col}_is_anomaly"
    direction_col = f"{value_col}_anomaly_direction"

    if median_col not in out.columns or mad_col not in out.columns:
        raise KeyError(f"Baseline columns missing for {value_col}")

    out[diff_col] = out[value_col] - out[median_col]
    out[score_col] = np.abs(out[diff_col]) / (1.4826 * out[mad_col].clip(lower=EPSILON))

    def classify_direction(diff: float):
        if pd.isna(diff):
            return None
        if diff > 0:
            return "up"
        if diff < 0:
            return "down"
        return "flat"

    out[direction_col] = out[diff_col].apply(classify_direction)

    if value_col in LOWER_IS_BAD_KPIS:
        bad_side = out[diff_col] < 0
    elif value_col in UPPER_IS_BAD_KPIS:
        bad_side = out[diff_col] > 0
    else:
        bad_side = pd.Series(True, index=out.index)

    enough_history = out[count_col].fillna(0) > 0
    out[flag_col] = (out[score_col] >= threshold) & bad_side & enough_history

    return out
