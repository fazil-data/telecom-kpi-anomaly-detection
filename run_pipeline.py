from src.pipeline import run_anomaly_pipeline, save_outputs


def main():
    result_df, anomaly_summary = run_anomaly_pipeline()
    save_outputs(result_df, anomaly_summary)

    print("Pipeline completed successfully.")
    print(f"Total rows processed: {len(result_df)}")
    print(f"Total anomalies flagged: {len(anomaly_summary)}")

    if not anomaly_summary.empty:
        print("\nTop anomaly counts by KPI:")
        print(anomaly_summary["kpi_name"].value_counts().to_string())
    else:
        print("\nNo anomalies flagged.")


if __name__ == "__main__":
    main()
