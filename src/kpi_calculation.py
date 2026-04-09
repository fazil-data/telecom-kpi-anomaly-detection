import numpy as np
import pandas as pd


def safe_rate(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """
    Calculate percentage safely.
    """
    denominator = denominator.astype(float)
    numerator = numerator.astype(float)

    return np.where(
        denominator > 0,
        (numerator / denominator) * 100.0,
        np.nan,
    )


def calculate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create telecom KPI fields from raw counters.
    """
    required_cols = [
        "timestamp",
        "cell_id",
        "rrc_attempts",
        "rrc_success",
        "e_rab_attempts",
        "e_rab_success",
        "dl_prb_utilization",
        "dl_throughput_mbps",
    ]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")

    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"])

    out["rrc_success_rate"] = safe_rate(out["rrc_success"], out["rrc_attempts"])
    out["e_rab_success_rate"] = safe_rate(out["e_rab_success"], out["e_rab_attempts"])

    out = out.sort_values(["cell_id", "timestamp"]).reset_index(drop=True)
    return out
