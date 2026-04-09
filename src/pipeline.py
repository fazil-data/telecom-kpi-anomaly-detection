import pandas as pd

from src.config import (
    DEFAULT_THRESHOLD_BY_KPI,
    INPUT_FILE,
    KPI_COLUMNS,
    LOOKBACK_HOURS,
    MIN_HISTORY_POINTS,
    OUTPUT_DIR,
)
from src.kpi_calculation import calculate_kpis
from src.baseline import add_rolling_baseline
from src.anomaly_scoring import add_anomaly_score


def load_input_data(file_path=INPUT_FILE) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def run_anomaly_pipeline(
    file_path=INPUT_FILE,
    lookback_hours: int = LOOKBACK_HOURS,
    min_history_points: int = MIN_HISTORY_POINTS,
    threshold_by_kpi: dict | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Run anomaly detection pipeline for all configured KPIs.
    """
    threshold_by_kpi = threshold_by_kpi or DEFAULT_THRESHOLD_BY_KPI

    raw_df = load_input_data(file_path=file_path)
    base_df = calculate_kpis(raw_df)

    result_df = base_df.copy()

    for kpi in KPI_COLUMNS:
        result_df = add_rolling_baseline(
            df=result_df,
            value_col=kpi,
            lookback_hours=lookback_hours,
            min_history_points=min_history_points,
        )
        result_df = add_anomaly_score(
            df=result_df,
            value_col=kpi,
            threshold=threshold_by_kpi[kpi],
        )

    anomaly_summary = build_anomaly_summary(result_df)
    return result_df, anomaly_summary


def build_anomaly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Produce a long-format anomaly table for analyst review.
    """
    records = []

    for kpi in KPI_COLUMNS:
        flag_col = f"{kpi}_is_anomaly"
        score_col = f"{kpi}_anomaly_score"
        diff_col = f"{kpi}_baseline_diff"
        direction_col = f"{kpi}_anomaly_direction"
        median_col = f"{kpi}_baseline_median"

        subset = df.loc[df[flag_col]].copy()
        if subset.empty:
            continue

        subset["kpi_name"] = kpi
        subset["kpi_value"] = subset[kpi]
        subset["baseline_value"] = subset[median_col]
        subset["anomaly_score"] = subset[score_col]
        subset["baseline_diff"] = subset[diff_col]
        subset["anomaly_direction"] = subset[direction_col]

        records.append(
            subset[
                [
                    "timestamp",
                    "cell_id",
                    "kpi_name",
                    "kpi_value",
                    "baseline_value",
                    "baseline_diff",
                    "anomaly_score",
                    "anomaly_direction",
                ]
            ]
        )

    if not records:
        return pd.DataFrame(
            columns=[
                "timestamp",
                "cell_id",
                "kpi_name",
                "kpi_value",
                "baseline_value",
                "baseline_diff",
                "anomaly_score",
                "anomaly_direction",
            ]
        )

    summary_df = pd.concat(records, ignore_index=True)
    summary_df = summary_df.sort_values(
        ["timestamp", "cell_id", "kpi_name"],
        ascending=[True, True, True],
    ).reset_index(drop=True)

    return summary_df


def save_outputs(result_df: pd.DataFrame, anomaly_summary: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(OUTPUT_DIR / "hourly_kpi_anomaly_output.csv", index=False)
    anomaly_summary.to_csv(OUTPUT_DIR / "anomaly_summary.csv", index=False)
