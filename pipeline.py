import pandas as pd
from edu_pipeline import SchoolRiskPipeline

DATA_PATH = r"data/passos_treino.csv"

DESIRED_FEATURES = ['fase', 'ano_ingresso', 'ipv', 'ian', 'ipp', 'matematica', 'portugues', 'defasagem']

if __name__ == '__main__':
    df = pd.read_csv(DATA_PATH)
    FEATURE_COLS = [c for c in DESIRED_FEATURES if c in df.columns]
    missing = [c for c in DESIRED_FEATURES if c not in FEATURE_COLS]
    print(f"Using features: {FEATURE_COLS}")
    if missing:
        print(f"Missing features from CSV (will be excluded): {missing}")

    pipeline = SchoolRiskPipeline(n_components=4)
    pipeline.fit_from_df(df, feature_cols=FEATURE_COLS)
    print('Retraining complete. Pipeline saved to school_risk_pipeline.pkl')
