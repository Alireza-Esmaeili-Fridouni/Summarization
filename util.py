import pandas as pd
import os

def read_csv(file_path):
    if not os.path.exists(file_path):
        print("Error: File not found.")
        return None
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def save_dataframe(df, directory, filename):
    try:
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"{filename}.csv")
        df.to_csv(file_path, index=False, encoding='utf-8')
        print(f"DataFrame saved successfully at: {file_path}")
    except PermissionError:
        print("Error: Permission denied. Try saving to a different location.")
    except Exception as e:
        print(f"Error: {e}")