import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from dsproject.config import FIGURE_DIR
import os

def basic_eda(df: pd.DataFrame, target: str = None):
    print("[INFO] Summary Statistics:")
    print(df.describe(include='all'))

    print("\n[INFO] Null Values:")
    print(df.isnull().sum())

def plot_distributions(df: pd.DataFrame, output_dir=FIGURE_DIR):
    os.makedirs(output_dir, exist_ok=True)
    for col in df.select_dtypes(include=['number']).columns:
        plt.figure(figsize=(8, 4))
        sns.histplot(df[col], kde=True, color='skyblue')
        plt.title(f'Distribution: {col}')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/{col}_dist.png")
        plt.close()
