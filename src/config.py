from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

INPUT_FILE = DATA_DIR / "sample_hourly_kpi.csv"

LOOKBACK_HOURS = 168  # 7 days
MIN_HISTORY_POINTS = 48
EPSILON = 1e-6

KPI_COLUMNS = [
    "rrc_success_rate",
    "e_rab_success_rate",
    "dl_prb_utilization",
    "dl_throughput_mbps",
]

LOWER_IS_BAD_KPIS = {
    "rrc_success_rate",
    "e_rab_success_rate",
    "dl_throughput_mbps",
}

UPPER_IS_BAD_KPIS = {
    "dl_prb_utilization",
}

DEFAULT_THRESHOLD_BY_KPI = {
    "rrc_success_rate": 3.5,
    "e_rab_success_rate": 3.5,
    "dl_prb_utilization": 3.5,
    "dl_throughput_mbps": 3.5,
}
