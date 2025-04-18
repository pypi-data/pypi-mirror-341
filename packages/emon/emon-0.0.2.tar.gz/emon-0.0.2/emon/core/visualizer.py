import matplotlib.pyplot as plt
import seaborn as sns
from emon.core.cleaner import get_cleaned_df

def visualiser():
    df = get_cleaned_df()
    if df is None:
        raise RuntimeError("[emon.visualiser] Please run emon.clean() first.")

    print("[emon.visualiser] Showing dataset heatmap and class distribution.")
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
    plt.title("Feature Correlation Heatmap")
    plt.show()

    plt.figure(figsize=(8, 4))
    sns.countplot(x=df.columns[-1], data=df)
    plt.title("Target Class Distribution")
    plt.show()
