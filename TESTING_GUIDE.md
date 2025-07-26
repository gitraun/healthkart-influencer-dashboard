# Testing Guide: HealthKart Influencer Campaign ROI Dashboard

## Current Phase Status: Phase 1 Complete ✅

This guide outlines what has been implemented, what works, and what to test in the current version of the dashboard.

## ✅ What Works in Current Version

### 1. Project Setup & Infrastructure
- **Complete folder structure** with organized modules
- **Streamlit configuration** properly set up
- **Multi-page navigation** working between dashboard sections
- **Session state management** for data persistence
- **Error handling** for data loading and validation

### 2. Data Layer (Fully Functional)
- **Mock data generation** with realistic HealthKart scenarios
- **50 influencers** across Fitness, Nutrition, Health, Lifestyle, Sports, Wellness categories
- **400+ posts** with platform-specific engagement patterns
- **500+ tracking records** with proper order attribution
- **Complete payout records** with mixed compensation models (post-based and revenue-sharing)

### 3. Core Analytics Engine (Fully Implemented)
- **Engagement rate calculations**: (Likes + Comments) / Reach
- **ROI metrics**: ROAS and Incremental ROAS
- **Performance scoring**: Composite metrics across multiple factors
- **Platform analysis**: Cross-platform performance comparison
- **Brand metrics**: MuscleBlaze, HKVitals, Gritzo performance tracking

### 4. Dashboard Interface (Complete)
- **Data Upload page**: Generate sample data or upload custom CSV files
- **Campaign Performance**: KPI cards, charts, and top performer tables
- **ROI Analysis**: ROAS distributions, cost analysis, and profitability metrics
- **Insights page**: Automated recommendations and persona analysis
- **Export functionality**: Download filtered data and reports

### 5. Interactive Features (Working)
- **Multi-dimensional filtering**: Platform, category, brand, influencer type
- **Real-time chart updates** based on filter selections
- **Interactive Plotly visualizations** with hover details and zoom
- **Data validation** with clear error messaging
- **Responsive layout** that works on different screen sizes

## 🧪 Testing Checklist

### Basic Functionality Tests

#### Data Upload & Generation
- [ ] Click "Generate Sample Dataset" button
- [ ] Verify data summary shows: 50 influencers, 400+ posts, 500+ tracking records
- [ ] Check that all 4 datasets load without errors
- [ ] Test CSV file upload with custom data files

#### Navigation & UI
- [ ] Navigate between all 5 pages: Data Upload, Campaign Performance, ROI Analysis, Insights, Export
- [ ] Verify sidebar filters work and update data in real-time
- [ ] Test responsive layout on different browser window sizes
- [ ] Check that all charts and tables render correctly

#### Campaign Performance Page
- [ ] Verify KPI cards show: Total Revenue, Orders, AOV, Reach, Active Influencers
- [ ] Test "Revenue by Platform" bar chart displays data
- [ ] Check "Orders by Category" pie chart shows distribution
- [ ] Verify "Engagement Rate by Platform" chart updates with filters
- [ ] Test "Revenue Trend Over Time" line chart shows temporal patterns
- [ ] Check "Top Performing Influencers" table displays ranked results

#### ROI Analysis Page
- [ ] Verify ROI metrics: Average ROAS, Incremental ROAS, Marketing Cost, Performance Score
- [ ] Test ROAS distribution histogram shows break-even line
- [ ] Check ROAS vs Cost scatter plot with bubble sizes for orders
- [ ] Verify platform ROI comparison bar chart shows grouped data
- [ ] Test detailed ROI table with sortable columns
- [ ] Check high performers and improvement opportunities sections

#### Insights Page
- [ ] Verify executive summary shows overall metrics
- [ ] Test top performers tabs: By ROAS, By Revenue, By Overall Score
- [ ] Check platform performance analysis charts and table
- [ ] Verify improvement opportunities section identifies underperformers
- [ ] Test actionable recommendations with priority levels
- [ ] Check influencer persona analysis heatmap

#### Export Functionality
- [ ] Test raw data downloads for all 4 datasets
- [ ] Verify ROI report generation with current date
- [ ] Check CSV file downloads work properly
- [ ] Test data exports include filtered results when filters are applied

### Advanced Feature Tests

#### Filtering System
- [ ] Test Platform filter: Select Instagram only, verify data updates
- [ ] Test Category filter: Select Fitness only, check filtered results
- [ ] Test Brand filter: Select MuscleBlaze only, verify tracking data filters
- [ ] Test combined filters: Platform + Category, verify intersection works
- [ ] Test filter reset functionality

#### Data Validation
- [ ] Upload malformed CSV file, verify error handling
- [ ] Upload CSV with missing columns, check validation messages
- [ ] Test with empty data files, verify graceful degradation
- [ ] Check orphaned record detection (posts without influencers)

#### Performance & Responsiveness
- [ ] Test dashboard with full dataset (50 influencers), verify loading speed
- [ ] Apply multiple filters rapidly, check for lag or errors
- [ ] Test chart interactions: hover, zoom, pan
- [ ] Verify memory usage remains stable during extended use

## 🔧 Known Limitations & Future Enhancements

### Current Limitations
- **File-based storage**: Uses CSV files, not database
- **No user authentication**: Single-user application
- **Limited export formats**: CSV only, no PDF reports yet
- **Basic insights**: Rule-based recommendations, no ML predictions
- **No real-time data**: Static datasets, no API integrations

### Phase 2+ Features (Not Yet Implemented)
- **Advanced filtering**: Date range pickers, follower count ranges
- **Machine learning insights**: Predictive analytics and trend forecasting
- **Real-time data sync**: Social media API integrations
- **User management**: Multi-user support with role-based access
- **Automated reporting**: Scheduled report generation and email delivery

## 🚨 Error Scenarios to Test

### Data Quality Issues
- [ ] Upload CSV with duplicate influencer IDs
- [ ] Test with negative revenue or engagement values
- [ ] Upload posts without corresponding influencer records
- [ ] Test with malformed date formats

### UI Edge Cases
- [ ] No data loaded state for each page
- [ ] Filter combinations that return empty results
- [ ] Very large numbers in revenue fields
- [ ] Special characters in influencer names or captions

### Performance Edge Cases
- [ ] Apply all filters simultaneously
- [ ] Generate multiple reports rapidly
- [ ] Navigate quickly between pages while data is loading
- [ ] Test with browser JavaScript disabled

## 📊 Expected Test Results

### Sample Data Metrics (After "Generate Sample Dataset")
- **Influencers**: 50 across 6 categories
- **Posts**: 400+ with realistic engagement (2-8% engagement rates)
- **Revenue**: ₹500K+ total across all campaigns
- **ROAS Range**: 0.5x to 8.0x (some profitable, some not)
- **Top Platforms**: Instagram and YouTube typically highest revenue
- **Performance Score Range**: 0-100 scale with normal distribution

### Validation Success Criteria
- ✅ All pages load without errors
- ✅ Charts display data and update with filters
- ✅ Tables show sortable, formatted data
- ✅ Export downloads work correctly
- ✅ Insights generate actionable recommendations
- ✅ No broken functionality across different browsers

## 🔍 Debugging Common Issues

### CSV Loading Errors
- **Issue**: "Error tokenizing data" or field count mismatch
- **Solution**: Check for commas in caption fields, regenerate sample data

### Chart Display Problems
- **Issue**: Empty charts or visualization errors
- **Solution**: Verify data is loaded, check filter combinations

### Filter Not Working
- **Issue**: Selections don't update displayed data
- **Solution**: Clear browser cache, regenerate sample data

### Performance Issues
- **Issue**: Slow loading or unresponsive interface
- **Solution**: Reduce dataset size, clear session state, restart application

## 📝 Test Report Template

```markdown
## Test Session: [Date]
**Tester**: [Name]
**Browser**: [Chrome/Firefox/Safari + Version]
**Dataset**: [Sample/Custom]

### Functionality Tests
- [ ] Data Upload: Pass/Fail - [Notes]
- [ ] Campaign Performance: Pass/Fail - [Notes]
- [ ] ROI Analysis: Pass/Fail - [Notes]
- [ ] Insights: Pass/Fail - [Notes]
- [ ] Export: Pass/Fail - [Notes]

### Issues Found
1. [Description] - [Severity: High/Medium/Low]
2. [Description] - [Severity: High/Medium/Low]

### Overall Assessment
[Summary of testing session and recommendations]
```

This testing guide ensures comprehensive validation of the current dashboard implementation while setting clear expectations for what works and what's planned for future phases.