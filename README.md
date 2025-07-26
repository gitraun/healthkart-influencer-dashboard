# HealthKart Influencer Campaign ROI Dashboard

A comprehensive web-based dashboard for tracking, analyzing, and optimizing influencer campaigns across multiple platforms and brands including MuscleBlaze, HKVitals, and Gritzo.

## 🎯 Objective

This dashboard enables HealthKart's marketing teams to:
- Track influencer campaign performance across Instagram, YouTube, Twitter, and TikTok
- Calculate ROI and incremental ROAS with proper attribution
- Filter and analyze metrics by brand, influencer, platform, and product
- Identify top performers and optimization opportunities
- Generate actionable insights for campaign optimization

## 🚀 Features

### Data Management
- CSV file upload for influencers, posts, tracking data, and payouts
- Mock data generation for testing and demonstration
- Data validation and quality checks
- Real-time data processing and analysis

### Analytics & Metrics
- **Engagement Analytics**: Reach, likes, comments, and engagement rates
- **ROI Calculations**: ROAS and incremental ROAS with baseline assumptions
- **Performance Tracking**: Revenue attribution per influencer and post
- **Payout Management**: Cost tracking based on post volume or order generation

### Interactive Dashboard
- **Campaign Performance**: Multi-dimensional filtering and visualization
- **ROI Analysis**: Comprehensive ROAS analysis and cost optimization
- **Insights Engine**: Automated identification of top performers and improvement opportunities
- **Export Capabilities**: Download reports and data in CSV format

### Key Metrics
- Total Revenue and Orders
- Average Order Value (AOV)
- Return on Ad Spend (ROAS)
- Incremental ROAS
- Cost per Order
- Performance Scores
- Platform and Brand Performance

## 📊 Data Model

The dashboard works with four core datasets:

### Influencers (`influencers.csv`)
- `influencer_id`: Unique identifier
- `name`: Influencer name
- `category`: Content category (Fitness, Nutrition, Health, etc.)
- `gender`: Gender classification
- `follower_count`: Number of followers
- `platform`: Social media platform

### Posts (`posts.csv`)
- `post_id`: Unique post identifier
- `influencer_id`: Reference to influencer
- `platform`: Social media platform
- `date`: Post publication date
- `url`: Post URL
- `caption`: Post caption/description
- `reach`: Post reach metrics
- `likes`: Number of likes
- `comments`: Number of comments

### Tracking Data (`tracking_data.csv`)
- `tracking_id`: Unique tracking identifier
- `source`: Traffic source
- `campaign`: Campaign identifier
- `influencer_id`: Reference to influencer
- `user_id`: Customer identifier
- `brand`: Product brand (MuscleBlaze, HKVitals, Gritzo)
- `product`: Specific product name
- `date`: Order date
- `orders`: Number of orders
- `revenue`: Revenue amount

### Payouts (`payouts.csv`)
- `influencer_id`: Reference to influencer
- `basis`: Payment basis (post/order)
- `rate`: Payment rate
- `orders`: Number of orders attributed
- `total_payout`: Total payment amount

## 🔧 Technical Setup

### Prerequisites
- Python 3.8+
- Streamlit
- Pandas, NumPy
- Plotly for visualizations

### Installation & Running

1. **Clone the repository**
```bash
git clone <repository-url>
cd influencer-roi-dashboard
