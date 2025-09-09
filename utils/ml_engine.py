# utils/ml_engine.py
import pandas as pd
import numpy as np
import joblib
import streamlit as st
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    mean_squared_error, r2_score, silhouette_score
)
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.svm import SVC, SVR
from sklearn.cluster import KMeans, DBSCAN
import shap
import matplotlib.pyplot as plt

def run_ml(df: pd.DataFrame, target_col: str, problem_type: str = None, tune_hyperparams: bool = False):
    """
    Run ML pipeline for classification, regression, or clustering.
    Returns best model and a metrics summary DataFrame.
    """

    results = {}
    df = df.copy()
    
    if not problem_type:
        if df[target_col].dtype in [np.int64, np.float64] and df[target_col].nunique() > 20:
            problem_type = "regression"
        elif df[target_col].dtype in [np.object, np.bool_, np.int64] or df[target_col].nunique() <= 20:
            problem_type = "classification"
        else:
            problem_type = "clustering"

    if problem_type in ["classification", "regression"]:
        X = df.drop(columns=[target_col])
        y = df[target_col]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train.select_dtypes(include=np.number))
        X_test_scaled = scaler.transform(X_test.select_dtypes(include=np.number))

        if problem_type == "classification":
            models = {
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "Random Forest": RandomForestClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "SVM": SVC(probability=True)
            }
        else:  
            models = {
                "Linear Regression": LinearRegression(),
                "Ridge Regression": Ridge(),
                "Lasso Regression": Lasso(),
                "Random Forest Regressor": RandomForestRegressor(),
                "Gradient Boosting Regressor": GradientBoostingRegressor(),
                "SVR": SVR()
            }

        best_metric = None
        best_model = None

        for name, model in models.items():
            try:
                if tune_hyperparams:
                    param_grid = {} 
                    model = GridSearchCV(model, param_grid, cv=3, n_jobs=-1)
                
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                if problem_type == "classification":
                    acc = accuracy_score(y_test, y_pred)
                    results[name] = {
                        "accuracy": acc,
                        "r2": r2_score(y_test, y_pred)
                    }
                    if best_metric is None or acc > best_metric:
                        best_metric = acc
                        best_model = model
                else:  # regression
                    rmse = mean_squared_error(y_test, y_pred, squared=False)
                    r2 = r2_score(y_test, y_pred)
                    results[name] = {"rmse": rmse, "r2": r2}
                    if best_metric is None or rmse < best_metric:
                        best_metric = rmse
                        best_model = model

            except Exception as e:
                st.warning(f"Model {name} failed: {e}")

    elif problem_type == "clustering":
        X = df.select_dtypes(include=np.number)
        models = {
            "KMeans(k=3)": KMeans(n_clusters=3, random_state=42),
            "KMeans(k=5)": KMeans(n_clusters=5, random_state=42),
            "DBSCAN": DBSCAN()
        }
        best_score = -np.inf
        best_model = None
        for name, model in models.items():
            try:
                labels = model.fit_predict(X)
                score = silhouette_score(X, labels) if len(set(labels)) > 1 else -1
                results[name] = {"silhouette_score": score}
                if score > best_score:
                    best_score = score
                    best_model = model
            except Exception as e:
                st.warning(f"Clustering {name} failed: {e}")
    else:
        raise ValueError("Invalid problem_type")

    return best_model, pd.DataFrame(results).T

def explain_model(model, X: pd.DataFrame):
    """SHAP explainability"""
    try:
        explainer = shap.Explainer(model, X)
        shap_values = explainer(X)
        st.subheader("Feature Importance (SHAP)")
        shap.plots.bar(shap_values, show=False)
        st.pyplot(plt.gcf())
        plt.clf()
    except Exception as e:
        st.warning(f"Explainability not available: {e}")

def save_trained_model(model, path: str):
    """Save trained model to disk"""
    joblib.dump(model, f"{path}.pkl")
