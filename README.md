# Telecom KPI Anomaly Detection

This project demonstrates a clean and reproducible anomaly detection pipeline for telecom network KPIs using hourly time-series data.

It calculates service quality KPIs from raw counters, builds rolling historical baselines per cell, and flags unusual behaviour using robust anomaly scoring.

## Project Objective

The goal of this project is to detect unusual KPI behaviour at the cell-hour level using historical baselines.

Typical use cases include:

- proactive monitoring of network quality
- identifying abnormal drops in success rates
- spotting unusual PRB utilization spikes
- highlighting throughput degradation
- supporting analyst review with explainable anomaly outputs

## KPIs Included

The sample pipeline covers:

- `rrc_success_rate`
- `e_rab_success_rate`
- `dl_prb_utilization`
- `dl_throughput_mbps`

## Methodology

### 1. KPI Calculation
Success-rate KPIs are derived from attempt and success counters:

- RRC Success Rate = `rrc_success / rrc_attempts * 100`
- E-RAB Success Rate = `e_rab_success / e_rab_attempts * 100`

### 2. Historical Baseline
For each cell and KPI, the pipeline calculates rolling historical statistics using only prior observations:

- rolling median
- rolling MAD (median absolute deviation)
- rolling mean
- rolling standard deviation

### 3. Anomaly Scoring
An anomaly score is calculated based on the distance from the rolling median, scaled by MAD:

- robust against outliers
- explainable
- suitable for operational monitoring

### 4. Directional Flagging
The pipeline only flags anomalies in the operationally bad direction:

- drops in success-rate KPIs
- drops in throughput
- spikes in PRB utilization

## Project Structure

telecom-kpi-anomaly-detection/
- `src/config.py` → project settings and KPI rules
- `src/kpi_calculation.py` → KPI derivation from raw counters
- `src/baseline.py` → rolling baseline creation
- `src/anomaly_scoring.py` → robust anomaly scoring and flagging
- `src/pipeline.py` → end-to-end workflow
- `run_pipeline.py` → project runner
- `data/sample_hourly_kpi.csv` → anonymised sample hourly KPI data
- `outputs/` → generated outputs

## Input Data

The sample dataset contains hourly KPI counters for anonymised telecom cells.

Example columns:

- `timestamp`
- `cell_id`
- `rrc_attempts`
- `rrc_success`
- `e_rab_attempts`
- `e_rab_success`
- `dl_prb_utilization`
- `dl_throughput_mbps`

## Output Files

The pipeline generates:

- `hourly_kpi_anomaly_output.csv`
- `anomaly_summary.csv`

## How to Run

```bash
pip install -r requirements.txt
python run_pipeline.py
