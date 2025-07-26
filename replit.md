# HealthKart Influencer Campaign ROI Dashboard

## Overview

This is a comprehensive web-based dashboard built with Streamlit for tracking, analyzing, and optimizing influencer campaigns across multiple platforms (Instagram, YouTube, Twitter, TikTok) and brands (MuscleBlaze, HKVitals, Gritzo). The application enables marketing teams to calculate ROI, track performance metrics, and generate actionable insights for campaign optimization.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application
- **Visualization**: Plotly (Express and Graph Objects) for interactive charts and graphs
- **Layout**: Wide layout with expandable sidebar for filtering options
- **State Management**: Streamlit session state for data persistence across interactions

### Backend Architecture
- **Language**: Python 3.x
- **Structure**: Modular design with separate modules for:
  - Data generation (`src/data_generator.py`)
  - Calculations (`src/calculations.py`) 
  - File uploads (`src/upload.py`)
  - Dashboard visualization (`src/dashboard.py`)
  - Insights generation (`src/insights.py`)

### Data Storage Solutions
- **Primary Storage**: CSV files stored in `/data` directory
- **File Types**: 
  - `influencers.csv` - Influencer profiles and metadata
  - `posts.csv` - Social media post data and engagement metrics
  - `tracking_data.csv` - Campaign tracking and conversion data
  - `payouts.csv` - Influencer payment information
- **Session Storage**: In-memory DataFrames using Streamlit session state
- **No Database**: Currently file-based, but architecture allows for easy database integration

## Key Components

### Data Management Layer
- **Mock Data Generator**: Creates realistic sample datasets for testing and demonstration
- **File Upload Handler**: Processes CSV uploads with schema validation
- **Data Validation**: Ensures uploaded data matches expected schemas

### Analytics Engine
- **ROI Calculations**: ROAS and incremental ROAS with baseline assumptions
- **Engagement Analytics**: Calculates engagement rates, reach metrics
- **Performance Scoring**: Multi-dimensional performance evaluation
- **Time Series Analysis**: Trend analysis and temporal patterns

### Visualization Layer
- **Performance Dashboard**: Multi-dimensional filtering and campaign overview
- **ROI Analysis Dashboard**: Comprehensive cost-benefit analysis
- **Insights Dashboard**: Automated insights and recommendations
- **Interactive Filters**: Platform, category, brand, and time-based filtering

### Insights Engine
- **Top Performer Identification**: Automated detection of high-performing influencers
- **Underperformer Analysis**: Identification of campaigns needing optimization
- **Platform Comparison**: Cross-platform performance analysis
- **Recommendation System**: Data-driven optimization suggestions

## Data Flow

1. **Data Ingestion**: CSV files uploaded or mock data generated
2. **Data Validation**: Schema validation and quality checks
3. **Data Processing**: Calculation of engagement rates, ROI metrics, and performance scores
4. **Data Analysis**: Generation of insights, identification of patterns and trends
5. **Data Visualization**: Interactive dashboards and charts
6. **Data Export**: Download capabilities for reports and filtered data

### Key Metrics Calculated
- Return on Ad Spend (ROAS)
- Incremental ROAS (accounting for baseline conversions)
- Engagement rates (likes + comments / reach)
- Performance scores (composite metric)
- Cost per order
- Platform-specific metrics
- Brand performance metrics

## External Dependencies

### Python Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualization library
- **numpy**: Numerical computing
- **datetime**: Date and time handling
- **os**: Operating system interface
- **io**: Input/output operations
- **random**: Random data generation

### No External APIs
- Currently self-contained with no external API dependencies
- Designed for internal use with uploaded data
- Architecture supports future integration with social media APIs

## Deployment Strategy

### Current Deployment
- **Platform**: Designed for Replit deployment
- **Environment**: Python runtime environment
- **Storage**: Local file system for CSV data storage
- **Access**: Web-based interface accessible via Replit URL

### Scalability Considerations
- **Database Migration**: Architecture supports easy migration from CSV to database storage
- **Multi-user Support**: Session state management allows for multiple concurrent users
- **Data Volume**: Current design suitable for medium-scale datasets (thousands of records)
- **Performance**: In-memory processing with caching capabilities

### Future Enhancements
- Integration with PostgreSQL or other databases
- Real-time data sync with social media platforms
- Advanced machine learning models for predictive analytics
- User authentication and role-based access control
- Automated report generation and scheduling

The application follows a clean separation of concerns with modular architecture, making it easy to extend functionality, add new data sources, or integrate with external systems as requirements evolve.