import pandas as pd
import joblib
import os
from emon.utils.validator import validate_dataset

X = None
y = None
label_encoder = None
df_cleaned = None

def clean(filepath, target):
    global X, y, label_encoder, df_cleaned

    df = pd.read_csv(filepath)
    validate_dataset(df, target)  # run all validations

    if 'Blood Pressure' in df.columns:
        df[['Systolic_BP', 'Diastolic_BP']] = df['Blood Pressure'].str.split('/', expand=True).astype(float)
        df.drop('Blood Pressure', axis=1, inplace=True)

    df = df.dropna()

    from sklearn.preprocessing import LabelEncoder
    label_encoder = LabelEncoder()
    df[target] = label_encoder.fit_transform(df[target])

    # Save label encoder to current directory
    joblib.dump(label_encoder, os.path.join(os.getcwd(), 'label_encoder.joblib'))

    X = df.drop(target, axis=1)
    y = df[target]
    df_cleaned = df.copy()
    print("\n[emon.clean] Dataset cleaned successfully.")


def get_cleaned_df():
    global df_cleaned
    return df_cleaned