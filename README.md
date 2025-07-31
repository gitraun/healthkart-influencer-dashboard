# HealthKart Influencer Campaign ROI Dashboard

## Overview

HealthKart runs influencer campaigns across various social platforms (Instagram, YouTube, Twitter, etc.) to promote a wide range of products across multiple brands such as MuscleBlaze, HKVitals, and Gritzo. This web application provides a centralized dashboard to simulate, track and analyze influencer campaign data.

## Objective

Build an open‑source, web‑based dashboard that allows internal marketing teams to:
- Upload and ingest influencer and campaign performance data
- Calculate and visualize ROI and incremental ROAS
- Filter and break down metrics by brand, influencer, platform, and product
- Track influencer payouts based on post or order volume
- Generate insights to optimize future campaigns

## Tech Stack
- **Language:** Python
- **Framework:** Streamlit
- **Data processing:** Pandas
- **Visualizations:** Plotly
- **Version control:** GitHub

## Getting Started

### Prerequisites
1. Python 3.8 or higher
2. Git (for cloning the repository)

### Installation
1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd healthkart-influencer-dashboard
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

### Usage
1. **Run the application:**
   ```sh
   streamlit run app.py
   ```
2. **Open your browser and go to:**
   [http://localhost:8501](http://localhost:8501)
3. **Upload your data or use the sample data generator.**
4. **Explore the dashboard tabs:**
   - Data Upload
   - Campaign Performance
   - ROI Analysis
   - Insights
   - Export
