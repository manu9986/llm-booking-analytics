from fastapi import APIRouter, Response, HTTPException, Query
from pydantic import BaseModel
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from io import BytesIO

router = APIRouter()
ANALYTICS_DB_PATH = "sqlite:///data/analytics.db"

# Define request model
class AnalyticsRequest(BaseModel):
    report_type: str  # Can be "revenue", "cancellations", "geography", "lead_time"
    format: str = Query("json", description="Response format: 'image' or 'json'")

def get_precomputed_analytics(report_type):
    """Retrieve precomputed analytics from the database."""
    engine = create_engine(ANALYTICS_DB_PATH)
    if report_type == "revenue":
        return pd.read_sql("SELECT * FROM revenue_trends", engine)
    elif report_type == "cancellations":
        return pd.read_sql("SELECT * FROM cancellation_rate", engine)
    elif report_type == "geography":
        return pd.read_sql("SELECT * FROM geo_distribution", engine)
    elif report_type == "lead_time":
        return pd.read_sql("SELECT * FROM lead_time_distribution", engine)
    else:
        raise HTTPException(status_code=400, detail="Invalid report type.")

@router.post("/analytics")
def generate_analytics(request: AnalyticsRequest):
    """Returns analytics report based on the requested type and format."""
    df = get_precomputed_analytics(request.report_type)

    if request.format == "image":
        if request.report_type == "revenue":
            fig, ax = plt.subplots(figsize=(10,5))
            sns.lineplot(x='month', y='revenue', data=df, marker='o', color='b', ax=ax)
            ax.set_title("Revenue Trends Over Time")
            ax.set_xlabel("Month")
            ax.set_ylabel("Total Revenue")
            ax.grid()

        elif request.report_type == "geography":
            fig, ax = plt.subplots(figsize=(10,5))
            sns.barplot(x='country', y='booking_count', data=df, palette="viridis", ax=ax)
            ax.set_title("Top 10 Countries by Booking Count")
            ax.set_xlabel("Country")
            ax.set_ylabel("Number of Bookings")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

        elif request.report_type == "lead_time":
            fig, ax = plt.subplots(figsize=(10,5))
            sns.histplot(df['lead_time'], bins=30, kde=True, color='purple', ax=ax)
            ax.set_title("Booking Lead Time Distribution")
            ax.set_xlabel("Days Before Check-in")
            ax.set_ylabel("Frequency")

        # Convert plot to image response
        img_io = BytesIO()
        plt.savefig(img_io, format="png")
        img_io.seek(0)
        return Response(img_io.getvalue(), media_type="image/png")

    else:
        if request.report_type == "cancellations":
            return {"cancellation_rate": f"{df['cancellation_rate'][0]:.2f}%"}
        else:
            return {"data_source": "precomputed", "data": df.to_dict(orient="records")}
