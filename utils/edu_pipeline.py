import numpy as np
import joblib
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder

class SchoolRiskPipeline:

    def __init__(self, n_components: int = 5, threshold: float = 0.5):
        """Initialize pipeline with PCA for dimensionality reduction.

        Parameters
        ----------
        n_components : int
            Number of PCA components to retain.
        threshold : float
            Decision threshold for binary classification (default 0.5).
        """
        self.n_components = n_components
        self.threshold = threshold
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=n_components, random_state=42)

        # encoder for any non-numeric columns passed via DataFrame helpers
        self.cat_encoder: OneHotEncoder | None = None
        self.categorical_cols_: list[str] = []
        self.numeric_cols_: list[str] = []  # track numeric columns
        # names of the original (pre‑encoded) features seen during fitting
        self.feature_names_: list[str] | None = None

        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            min_samples_leaf=8,
            class_weight='balanced',
            random_state=42
        )

    # ---------------- TRAIN ----------------
    def fit(self, X, y, save_path: str = "model/school_risk_pipeline.pkl"):
        """Fit the pipeline to the data and persist it.

        Accepts either a NumPy array or a ``pandas.DataFrame`` for ``X``.  When
        a DataFrame is provided the internal encoder will be used to convert any
        non-numeric columns to numeric values automatically before training.

        The pipeline is always saved once training completes. By default it is
        written to ``school_risk_pipeline.pkl``, but a different location can be
        provided via ``save_path``.

        Parameters
        ----------
        X : array-like or pandas.DataFrame
            Feature matrix.
        y : array-like or pandas.Series
            Target values.
        save_path : str, optional
            Path where the trained pipeline will be saved. Defaults to
            ``school_risk_pipeline.pkl``.
        """

        # if the user passed a DataFrame, apply the preprocessing step
        if isinstance(X, pd.DataFrame):
            # record the column order so we can validate during inference
            self.feature_names_ = list(X.columns)
            X = self._prepare_features(X, fit=True)
        # convert y if it is a Series
        if isinstance(y, pd.Series):
            y = y.values

        # 1) Padronizar
        X_scaled = self.scaler.fit_transform(X)

        # 2) Apply PCA for dimensionality reduction
        X_pca = self.pca.fit_transform(X_scaled)

        # 3) Treinar RandomForest on PCA-transformed features
        self.model.fit(X_pca, y)

        # save trained pipeline to disk
        self.save(save_path)

    # ---------------- RISCO ----------------
    def predict_risk(self, X):
        """Return the risk probability for each sample.

        ``X`` may be an array or a DataFrame; in the latter case non-numeric
        columns are encoded using the previously fitted encoder.
        """
        if isinstance(X, pd.DataFrame):
            X = self._prepare_features(X, fit=False)

        X_scaled = self.scaler.transform(X)

        # Apply PCA for dimensionality reduction
        X_pca = self.pca.transform(X_scaled)

        # probabilidade de piorar
        proba = self.model.predict_proba(X_pca)[:,1]

        return proba

    # ---------------- CLASSE (opcional) ----------------
    def predict(self, X, threshold: float | None = None):
        """Return binary labels based on a threshold.

        If ``threshold`` is not provided the pipeline's stored
        ``self.threshold`` value is used. ``X`` can be an array or DataFrame.
        """
        if threshold is None:
            threshold = self.threshold
        risk = self.predict_risk(X)
        return (risk >= threshold).astype(int)

    # ---------------- SAVE ----------------
    def save(self, path="model/school_risk_pipeline.pkl"):
        joblib.dump(self, path)

    # ---------------- UTILITY ----------------
    def set_threshold(self, value: float):
        """Update the decision threshold used by :meth:`predict`.

        Parameters
        ----------
        value : float
            New threshold between 0 and 1.
        """
        if not 0 <= value <= 1:
            raise ValueError("threshold must be between 0 and 1")
        self.threshold = value

    # ---------------- INTERNAL HELPERS ----------------
    def _prepare_features(
        self, X_df: pd.DataFrame, fit: bool = True
    ) -> np.ndarray:
        """Convert a DataFrame to numeric array, encoding categoricals.

        Parameters
        ----------
        X_df : pandas.DataFrame
            Input feature data.
        fit : bool
            Whether the method is being called during fitting. If ``True`` and
            categorical columns are present, the internal encoder is fitted.

        Returns
        -------
        np.ndarray
            Array suitable for passing to ``fit`` or ``predict``.
        """
        # identify categorical columns if this is the first call
        if fit:
            self.categorical_cols_ = X_df.select_dtypes(include=["object", "category"]).columns.tolist()
            self.numeric_cols_ = X_df.select_dtypes(exclude=["object", "category"]).columns.tolist()
            if self.categorical_cols_:
                self.cat_encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
                cat_arr = self.cat_encoder.fit_transform(X_df[self.categorical_cols_])
            else:
                cat_arr = None
        else:
            # during prediction, ensure all numeric columns are present in order
            if self.categorical_cols_ and self.cat_encoder is not None:
                # create a copy with all required categorical columns present
                X_temp = X_df.copy()
                for col in self.categorical_cols_:
                    if col not in X_temp.columns:
                        # fill missing column with a placeholder
                        X_temp[col] = "missing"
                cat_arr = self.cat_encoder.transform(X_temp[self.categorical_cols_])
            else:
                cat_arr = None

        # get numeric columns by dropping categoricals (fallback if numeric_cols_ is empty)
        if self.numeric_cols_:
            numeric_cols_to_use = [c for c in self.numeric_cols_ if c in X_df.columns]
            num_arr = X_df[numeric_cols_to_use].values if numeric_cols_to_use else np.array([]).reshape(X_df.shape[0], 0)
        else:
            # fallback: drop categorical columns to get numerics
            numeric_df = X_df.drop(columns=self.categorical_cols_, errors="ignore")
            num_arr = numeric_df.values

        if cat_arr is not None and num_arr.shape[1] > 0:
            return np.hstack([num_arr, cat_arr])
        elif cat_arr is not None:
            return cat_arr
        else:
            return num_arr

    # ---------------- DATAFRAME HELPERS ----------------
    def fit_from_df(
        self,
        df: pd.DataFrame,
        target_col: str = "piorou_defasagem",
        feature_cols: list | None = None,
        save_path: str = "model/school_risk_pipeline.pkl",
    ):
        """Convenience wrapper around :meth:`fit` that accepts a DataFrame.

        The method will pull features and the specified target column from the
        DataFrame.  By default the target used for the random forest is
        ``piorou_defasagem`` (as requested), but a different column name can be
        supplied.  If ``feature_cols`` is ``None`` all columns except the target
        are treated as predictors.

        Parameters
        ----------
        df : pandas.DataFrame
            Source data containing predictors and target.
        target_col : str, optional
            Name of the column to use as ``y``.  Defaults to
            ``"piorou_defasagem"``.
        feature_cols : list[str] or None, optional
            Names of columns to use as features.  If ``None`` every column
            except ``target_col`` is included.
        save_path : str, optional
            File path where the fitted pipeline will be saved.
        """
        if feature_cols is None:
            feature_cols = [c for c in df.columns if c != target_col]

        X_df = df[feature_cols]
        # remember feature order
        self.feature_names_ = feature_cols.copy()
        X = self._prepare_features(X_df, fit=True)
        y = df[target_col].values
        return self.fit(X, y, save_path=save_path)

    def predict_from_df(
        self,
        df: pd.DataFrame,
        feature_cols: list | None = None,
        threshold: float | None = None,
    ):
        """Predict class labels or risk probabilities from a DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            Data containing only the feature columns (the target should be
            absent or ignored).
        feature_cols : list[str] or None
            Columns to use as input.  Defaults to all columns in ``df``.
        threshold : float
            Decision threshold for converting probabilities into labels; used
            when the caller opts for class predictions via :meth:`predict`.
        """
        # if feature_names were recorded during training, use those
        if self.feature_names_ is not None:
            # ensure all required columns are present
            missing = [c for c in self.feature_names_ if c not in df.columns]
            if missing:
                raise ValueError(f"DataFrame is missing required features: {missing}")
            # use exact column order from training
            feature_cols = self.feature_names_
        elif feature_cols is None:
            feature_cols = list(df.columns)

        # extract and reorder columns
        X_df = df[feature_cols]
        X = self._prepare_features(X_df, fit=False)
        
        # verify that scaler will accept the prepared features
        if hasattr(self.scaler, "n_features_in_"):
            expected = self.scaler.n_features_in_
            if X.shape[1] != expected:
                raise ValueError(
                    f"After preprocessing, input has {X.shape[1]} features but scaler "
                    f"expected {expected}. Feature columns used: {feature_cols}. "
                    f"Expected: {self.feature_names_}"
                )
        return self.predict(X, threshold=threshold)

    # ---------------- LOAD ----------------
    @staticmethod
    def load(path="model/school_risk_pipeline.pkl"):
        """Load a pipeline from disk.

        Older pickles may not have newer attributes such as ``feature_names_`` or
        ``threshold``; in that case we add reasonable defaults so prediction
        logic continues to work.
        """
        pl = joblib.load(path)
        if not hasattr(pl, "feature_names_"):
            pl.feature_names_ = None
        if not hasattr(pl, "categorical_cols_"):
            pl.categorical_cols_ = []
        if not hasattr(pl, "numeric_cols_"):
            pl.numeric_cols_ = []
        if not hasattr(pl, "threshold"):
            pl.threshold = 0.5
        return pl



if __name__ == "__main__":
    # quick demonstration using the training data
    data_path = r"C:/Users/jenil/OneDrive/Documents/Faculdade/Tech Challenge 5/datathon/data/passos_treino.csv"
    df = pd.read_csv(data_path)

    # instantiate with desired number of clusters
    pipeline = SchoolRiskPipeline()

    # train using the DataFrame helper (target defaults to 'piorou_defasagem')
    pipeline.fit_from_df(df)

    print("Pipeline trained and saved at school_risk_pipeline.pkl")
