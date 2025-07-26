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

The tool is developed in a modular fashion, deployed via Replit, and version‑controlled in a GitHub repository.

## Tech Stack

- **Language:** Python  
- **Framework:** Streamlit  
- **Data processing:** Pandas  
- **Visualizations:** Plotly
- **Hosting:** Replit  
- **Version control:** GitHub  

## Complete Development Plan

### Phase 1: Project Setup & Data Foundation (Week 1)

#### Module 1.1: Environment & Version Control Setup
**Duration: 1-2 days**

**Tasks:**
- Create Replit project with Python template
- Set up complete folder structure (src/, data/, config/, tests/, docs/)
- Configure requirements.txt with all dependencies
- Create .env file structure for future configurations
- Initialize GitHub repository and connect to Replit
- Set up .gitignore and initial documentation
- Configure git branching strategy (main, develop, feature branches)

**Deliverables:**
- Fully structured project repository
- GitHub integration with proper version control
- Development environment ready for coding

#### Module 1.2: Mock Dataset Creation & Data Modeling
**Duration: 2-3 days**

**Tasks:**
- Generate realistic influencers.csv (25-30 records across Fitness, Beauty, Health categories)
- Create posts.csv (150+ records with platform-specific engagement patterns)
- Build tracking_data.csv (500+ records with order attribution)
- Generate payouts.csv (100+ records with mixed compensation models)
- Ensure relational consistency across all datasets
- Document data assumptions and business rules
- Create data validation schemas

**Deliverables:**
- 4 interconnected CSV datasets with realistic HealthKart scenarios
- Data dictionary and relationship documentation
- Basic data validation framework

### Phase 2: Core Data Infrastructure (Week 2)

#### Module 2.1: Data Ingestion System
**Duration: 2-3 days**

**Tasks:**
- Build CSV upload functionality with Streamlit file uploader
- Implement data validation (schema checking, relationship integrity)
- Create data preprocessing pipeline (cleaning, standardization)
- Set up error handling for malformed data
- Implement data storage in session state
- Add support for multiple file formats (CSV, XLSX)

#### Module 2.2: Data Processing Engine
**Duration: 2-3 days**

**Tasks:**
- Build pandas-based data aggregation functions
- Create influencer-level performance calculations
- Implement campaign-level metrics aggregation
- Set up time-series data processing
- Build data relationship management system
- Add data caching for performance optimization

### Phase 3: Analytics & Calculations Engine (Week 3)

#### Module 3.1: Core Metrics Calculator
**Duration: 3-4 days**

**Key Formulas:**
```python
Engagement Rate = (Likes + Comments) / Reach * 100
Revenue per Influencer = Sum(attributed_orders * product_price)
Conversion Rate = Orders / Reach * 100
Cost per Acquisition = Total_Cost / Total_Orders
```

#### Module 3.2: ROI & ROAS Analysis Engine
**Duration: 2-3 days**

**Tasks:**
- Implement ROAS calculation: Revenue / Cost
- Build Incremental ROAS: (Revenue - Baseline) / Cost
- Create ROI trend analysis functions
- Add cost allocation logic across campaigns

### Phase 4: Dashboard Interface & Visualizations (Week 4)

#### Module 4.1: Main Dashboard Architecture
**Dashboard Pages:**
- **Overview**: High-level KPIs and summary metrics
- **Influencer Performance**: Individual influencer deep-dive
- **Campaign Analysis**: ROI trends and comparative analysis
- **Platform Insights**: Platform-specific performance
- **Brand Analysis**: Brand-wise campaign effectiveness

#### Module 4.2: Interactive Visualizations
**Visualization Types:**
- KPI cards with trend indicators
- Interactive line charts for performance over time
- Bar charts for influencer comparisons
- Scatter plots for ROI vs. engagement analysis
- Heatmaps for platform/brand performance matrix

### Phase 5: Advanced Features & Insights (Week 5)

#### Module 5.1: Multi-Dimensional Filtering System
**Filter Categories:**
- **Brand**: MuscleBlaze, HKVitals, Gritzo
- **Platform**: Instagram, YouTube, Twitter, etc.
- **Product Category**: Supplements, Vitamins, Kids nutrition
- **Influencer Type**: Macro, Micro, Nano influencers
- **Demographics**: Gender, age group, follower count
- **Time Period**: Custom date ranges, predefined periods

#### Module 5.2: Insights Engine & Recommendations
**Insight Categories:**
- **Top Performers**: Best ROI influencers by category
- **Optimization Opportunities**: Underperforming campaigns
- **Budget Allocation**: Optimal spend distribution
- **Platform Strategy**: Best performing platform combinations

### Phase 6: Export, Documentation & Deployment (Week 6)

#### Module 6.1: Export & Reporting System
**Export Features:**
- **Data Export**: Filtered datasets in CSV/XLSX format
- **Insight Reports**: PDF summaries with key findings
- **Dashboard Snapshots**: Visual report generation

#### Module 6.2: Final Polish & Deployment
**Documentation:**
- **README.md**: Setup, installation, and usage guide
- **API Documentation**: Function and module documentation
- **User Guide**: Step-by-step dashboard usage instructions

## Development Timeline Summary

| Week | Phase | Key Deliverables | Focus Area |
|------|-------|------------------|------------|
| 1 | Setup & Foundation | Project structure, Mock data, GitHub integration | Infrastructure |
| 2 | Data Infrastructure | Upload system, Data processing pipeline | Data Management |
| 3 | Analytics Engine | Metrics calculation, ROI analysis | Core Analytics |
| 4 | Dashboard & Visualizations | Multi-page app, Interactive charts | User Interface |
| 5 | Advanced Features | Filtering system, Insights engine | Intelligence Layer |
| 6 | Polish & Deployment | Export features, Documentation, Deployment | Production Ready |

## Project Structure

```
influencer-roi-dashboard/
├── .env                          # Environment variables
├── .gitignore                    # Git ignore file
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
├── app.py                       # Main Streamlit app entry point
├── data/
│   ├── influencers.csv          # Influencer profiles
│   ├── posts.csv                # Social media posts
│   ├── tracking_data.csv        # Campaign tracking
│   └── payouts.csv              # Payment information
├── src/
│   ├── __init__.py
│   ├── data_generator.py        # Mock data generation
│   ├── calculations.py          # ROI, ROAS, metrics
│   ├── upload.py                # File upload handling
│   ├── dashboard.py             # Dashboard components
│   └── insights.py              # Analysis & recommendations
├── .streamlit/
│   └── config.toml              # Streamlit configuration
└── replit.md                    # Project documentation
```

## Data Models

### Influencers Dataset
- `influencer_id`: Unique influencer identifier
- `name`: Influencer name
- `category`: Content category (Fitness, Beauty, Health)
- `gender`: M/F
- `follower_count`: Number of followers
- `platform`: Primary platform

### Posts Dataset
- `post_id`: Unique post identifier
- `influencer_id`: Links to influencers table
- `platform`: Social media platform
- `date`: Post date
- `url`: Post URL
- `caption`: Post caption
- `reach`: Post reach
- `likes`: Number of likes
- `comments`: Number of comments

### Tracking Data
- `tracking_id`: Unique tracking identifier
- `source`: Traffic source
- `campaign`: Campaign identifier
- `influencer_id`: Links to influencers table
- `user_id`: User identifier
- `brand`: Product brand
- `product`: Product name
- `date`: Transaction date
- `orders`: Number of orders
- `revenue`: Revenue generated

### Payouts
- `influencer_id`: Links to influencers table
- `basis`: Payment basis (post/order)
- `rate`: Payment rate
- `orders`: Number of orders (if applicable)
- `total_payout`: Total payment amount

## Key Features Implemented

### 🚀 Dashboard Features
- **Multi-page Navigation**: Data Upload, Campaign Performance, ROI Analysis, Insights, Export
- **Interactive Filtering**: Platform, category, brand, and demographic filters
- **Real-time Analytics**: Live calculation of engagement rates, ROAS, and performance scores
- **Visual Analytics**: Plotly charts for trends, comparisons, and distributions

### 📊 Analytics Capabilities
- **Engagement Metrics**: Reach, likes, comments, engagement rates
- **ROI Calculations**: ROAS and incremental ROAS with baseline assumptions
- **Performance Scoring**: Composite scores based on multiple factors
- **Time Series Analysis**: Trend analysis and temporal patterns

### 🔍 Insights Engine
- **Top Performer Identification**: Automated detection of high-performing influencers
- **Underperformer Analysis**: Identification of campaigns needing optimization
- **Platform Comparison**: Cross-platform performance analysis
- **Recommendation System**: Data-driven optimization suggestions

### 📈 Key Metrics Calculated
- Return on Ad Spend (ROAS)
- Incremental ROAS (accounting for baseline conversions)
- Engagement rates (likes + comments / reach)
- Performance scores (composite metric)
- Cost per order
- Platform-specific metrics
- Brand performance metrics

## Multi-Influencer Data Handling

The system efficiently handles datasets with multiple influencers through:

### Relational Data Model
- Each dataset linked by `influencer_id` as primary key
- Maintains data integrity across all influencer records
- Handles hundreds of influencers efficiently through pandas DataFrames

### Multi-Influencer Processing
- Aggregation across all influencers for campaign-level insights
- Individual influencer performance tracking and comparison
- Cross-influencer analytics for optimization opportunities

### Comparative Analysis
- Rank influencers by ROI, engagement rate, and revenue generated
- Group analysis by influencer categories (Fitness, Beauty, Sports)
- Platform-wise performance comparison across influencers
- Multi-dimensional filtering for targeted analysis

## Getting Started

### Prerequisites
- Python 3.8+
- Replit account
- GitHub account (optional)

### Installation
1. Open in Replit
2. Dependencies are automatically installed
3. Run the application: `streamlit run app.py`

### Usage
1. **Data Upload**: Generate sample data or upload your own CSV files
2. **Campaign Performance**: View key metrics and performance charts
3. **ROI Analysis**: Analyze ROAS and cost effectiveness
4. **Insights**: Get automated recommendations and top performer analysis
5. **Export**: Download reports and filtered data

### Sample Data Generation
The dashboard includes a mock data generator that creates realistic datasets with:
- 50 influencers across different categories and platforms
- 400+ posts with realistic engagement patterns
- 1000+ tracking records with order attribution
- Comprehensive payout records with mixed compensation models

## Development Approach

### Multi-Influencer Architecture
The dashboard handles multiple influencers through:
- **Efficient Data Structures**: pandas DataFrames optimized for multi-influencer operations
- **Scalable Aggregations**: Group-by operations for campaign and platform analysis
- **Interactive Filtering**: Real-time filtering across large influencer datasets
- **Performance Optimization**: Caching and efficient calculations for responsive user experience

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
MIT License

## Contact
For questions or support, please reach out to the development team.
