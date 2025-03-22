import pandas as pd
from sqlalchemy import create_engine

# Database paths
DB_PATH = "sqlite:///data/bookings.db"
ANALYTICS_DB_PATH = "sqlite:///data/analytics.db"
CLEANED_DATA_PATH = "data/cleaned_bookings.csv"

# Load cleaned dataset from CSV or SQLite
def load_cleaned_data():
    """Load cleaned booking data from CSV or SQLite database."""
    # Option 1: Load from CSV
    df = pd.read_csv(CLEANED_DATA_PATH)

    # Option 2: Load from SQLite
    #engine = create_engine(DB_PATH)
    #df = pd.read_sql("SELECT * FROM bookings", engine)

    return df

# Load cleaned data
df = load_cleaned_data()

# Precompute revenue trends
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])
revenue_per_month = df.groupby(df['reservation_status_date'].dt.to_period("M"))['adr'].sum().reset_index()
revenue_per_month.columns = ['month', 'revenue']
revenue_per_month['last_updated'] = pd.Timestamp.now()

# Convert 'month' from Period to string
revenue_per_month['month'] = revenue_per_month['month'].astype(str)

# Store revenue trends in analytics database
analytics_engine = create_engine(ANALYTICS_DB_PATH)
revenue_per_month.to_sql('revenue_trends', analytics_engine, if_exists='replace', index=False)

# Precompute cancellation rate
total_bookings = len(df)
cancelled_bookings = len(df[df['is_canceled'] == 1])
cancellation_rate = (cancelled_bookings / total_bookings) * 100
cancellation_rate_df = pd.DataFrame({'cancellation_rate': [cancellation_rate], 'last_updated': [pd.Timestamp.now()]})

# Store cancellation rate in analytics database
cancellation_rate_df.to_sql('cancellation_rate', analytics_engine, if_exists='replace', index=False)

# Precompute geographical distribution
geo_distribution = df['country'].value_counts().reset_index()
geo_distribution.columns = ['country', 'booking_count']
geo_distribution['last_updated'] = pd.Timestamp.now()

# Store geographical distribution in analytics database
geo_distribution.to_sql('geo_distribution', analytics_engine, if_exists='replace', index=False)

# Precompute lead time distribution
lead_time_distribution = df['lead_time'].value_counts().reset_index()
lead_time_distribution.columns = ['lead_time', 'count']
lead_time_distribution['last_updated'] = pd.Timestamp.now()

# Store lead time distribution in analytics database
lead_time_distribution.to_sql('lead_time_distribution', analytics_engine, if_exists='replace', index=False)

print("Analytics precomputed and stored successfully.")
