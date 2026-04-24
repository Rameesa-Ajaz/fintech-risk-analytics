import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

def clean_data():
    # Define paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    input_path = os.path.join(base_dir, 'data', 'creditcard.csv')
    output_path = os.path.join(base_dir, 'data', 'cleaned_transactions.csv')
    
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    print("Converting 'Time' column to relative hours...")
    # 'Time' is originally in seconds
    df['Time'] = df['Time'] / 3600.0
    
    print("Scaling 'Amount' column using StandardScaler...")
    scaler = StandardScaler()
    df['Amount'] = scaler.fit_transform(df[['Amount']])
    
    print(f"Saving cleaned data to {output_path}...")
    df.to_csv(output_path, index=False)
    print("Data cleaning complete! File saved successfully.")

if __name__ == "__main__":
    clean_data()
