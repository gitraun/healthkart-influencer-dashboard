# Instagram Dashboard Testing Guide

## Current Status: Instagram-Only Data Generated ✅

All data is now Instagram-only. Here's how to test each feature:

## 1. Campaign Performance Testing

### Step-by-Step Instructions:
1. **Navigate**: Go to "Campaign Performance" page
2. **Check KPI Cards**: Should show Instagram metrics:
   - Total Revenue: ~₹50,000-150,000
   - Total Orders: 50-150 orders  
   - Active Influencers: All 50 (Instagram only)
   - Total Reach: Combined Instagram reach

3. **Platform Charts**: All charts should show "Instagram" only
   - Revenue by Platform: Single Instagram bar
   - Orders by Category: Distribution across Fitness, Nutrition, etc.
   - Engagement Rate: Instagram engagement rates (2-8%)

4. **Top Performers Table**: Shows top Instagram influencers by revenue

### What You Should See:
- No platform dropdown (all Instagram)
- Realistic Instagram engagement rates
- Revenue distributed across HealthKart brands

## 2. Incremental ROAS Testing  

### Step-by-Step Instructions:
1. **Navigate**: Go to "ROI Analysis" page
2. **Check ROI Metrics**:
   - Average ROAS: 1.5x - 4.0x (realistic range)
   - Incremental ROAS: 1.2x - 3.2x (80% of regular ROAS)
   - Marketing Cost: Total payouts to Instagram influencers

3. **ROAS Distribution Chart**: 
   - Histogram showing ROAS spread
   - Break-even line at 1.0x
   - Most influencers between 1x-5x ROAS

4. **ROAS vs Cost Scatter Plot**:
   - Each dot = Instagram influencer
   - X-axis = Marketing cost (payout)
   - Y-axis = ROAS value
   - Bubble size = number of orders

### What Incremental ROAS Means:
- **Regular ROAS**: Total Revenue ÷ Marketing Cost
- **Incremental ROAS**: (Revenue - Baseline) ÷ Marketing Cost
- **Baseline**: 20% of revenue (assumed would happen anyway)
- **Example**: ₹10,000 revenue, ₹3,000 cost → Regular ROAS = 3.3x, Incremental ROAS = 2.7x

## 3. Influencer Insights Testing

### Step-by-Step Instructions:
1. **Navigate**: Go to "Insights" page
2. **Executive Summary**: Check overall Instagram performance metrics

3. **Top Performers Tabs**:
   - **By ROAS**: Instagram influencers ranked by return on investment
   - **By Revenue**: Instagram influencers ranked by total sales generated  
   - **By Overall Score**: Composite performance metric

4. **Platform Performance**: Should show Instagram-only analysis

5. **Improvement Opportunities**: 
   - Low ROAS Instagram influencers 
   - Suggestions for optimization

6. **Actionable Recommendations**:
   - Specific advice for Instagram campaigns
   - Priority levels (High/Medium/Low)

### What You Should See:
- All analysis focused on Instagram
- Clear performance rankings
- Specific improvement suggestions

## 4. Payout Tracking Testing

### Step-by-Step Instructions:
1. **Navigate**: Go to "Export" page
2. **Download Payout Data**: Click to download CSV

3. **Check Payout Structure**:
   - **Post-based**: Fixed amount per Instagram post (₹5,000-50,000)
   - **Revenue-based**: Percentage of sales (5-15%)
   - Most micro-influencers paid per post
   - Larger influencers often revenue-sharing

4. **Analyze Cost Efficiency**:
   - Compare total_payout vs revenue generated
   - Calculate cost per order: payout ÷ orders
   - Identify most cost-effective Instagram influencers

### Expected Payout Data:
- **Influencer ID**: INF_001, INF_002, etc.
- **Basis**: "post" or "order" 
- **Rate**: Amount per post or percentage
- **Orders**: Total orders generated
- **Total Payout**: Final payment amount

## Quick Verification Checklist

### Data Upload Page:
- [ ] "Generate Sample Dataset" works
- [ ] Shows 50 Instagram influencers
- [ ] Data summary displays correctly

### Campaign Performance Page:
- [ ] KPI cards show realistic numbers
- [ ] Charts display Instagram data
- [ ] Top performers table loads

### ROI Analysis Page:
- [ ] ROAS calculations work
- [ ] Charts display without errors
- [ ] Individual influencer data shows

### Insights Page:
- [ ] Top performer tabs work
- [ ] Recommendations generate
- [ ] Platform analysis shows Instagram

### Export Page:
- [ ] CSV downloads work
- [ ] Data contains Instagram influencers only
- [ ] File format is correct

## Troubleshooting

### If Charts Don't Load:
1. Check browser console for JavaScript errors
2. Refresh the page
3. Try regenerating sample data

### If Calculations Seem Wrong:
- ROAS should be mostly between 0.5x - 8.0x
- Very high ROAS (>10x) indicates data issues
- Negative values indicate calculation errors

### If No Data Shows:
1. Ensure sample data was generated
2. Check all influencers are Instagram platform
3. Verify CSV files exist in data/ folder

This focused approach eliminates platform complexity and ensures we can validate the core functionality with Instagram influencers only.