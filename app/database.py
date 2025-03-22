import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Path to dataset
DATA_PATH = "data/hotel_bookings.csv"
CLEANED_DATA_PATH = "data/cleaned_bookings.csv"

def load_and_clean_data():
    """Loads and cleans hotel booking data."""
    try:
        df = pd.read_csv(DATA_PATH)

        # Display basic info
        print("Data Overview:\n")
        print(df.info())
        print("\nMissing Values:\n", df.isnull().sum())
        print("\nFirst 5 Rows:\n", df.head())

        # Handle missing values
        df.fillna({
            'lead_time': df['lead_time'].median(),
            'adr': df['adr'].mean(),
            'country': 'Unknown',
        }, inplace=True)
        df.dropna(inplace=True)  # Drop any remaining NaNs

        # Convert date column to datetime format
        if 'reservation_status_date' in df.columns:
            df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])

        # Save cleaned dataset
        df.to_csv(CLEANED_DATA_PATH, index=False)
        print(f"✅ Data preprocessing complete! Cleaned dataset saved as '{CLEANED_DATA_PATH}'")

        return df

    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

# Store data in SQLite for further use
def save_to_db(df):
    """Saves cleaned data to SQLite database."""
    engine = create_engine("sqlite:///data/bookings.db")
    df.to_sql("bookings", engine, if_exists="replace", index=False)
    print("✅ Data saved to SQLite database!")

if __name__ == "__main__":
    df = load_and_clean_data()
    if df is not None:
        save_to_db(df)
