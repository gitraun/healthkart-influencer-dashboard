"""
ROI and performance calculation functions for HealthKart Influencer Dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_engagement_rates(posts_df):
    """Calculate engagement rates for posts"""
    posts_df = posts_df.copy()
    
    # Calculate engagement rate: (likes + comments) / reach
    posts_df['engagement_rate'] = (posts_df['likes'] + posts_df['comments']) / posts_df['reach']
    posts_df['engagement_rate'] = posts_df['engagement_rate'].fillna(0)
    
    return posts_df

def calculate_roi_metrics(tracking_df, payouts_df, influencers_df):
    """Calculate ROI and ROAS metrics"""
    
    # Merge tracking data with payouts and influencers
    roi_data = tracking_df.groupby('influencer_id').agg({
        'revenue': 'sum',
        'orders': 'sum'
    }).reset_index()
    
    # Merge with payouts data
    roi_data = roi_data.merge(payouts_df, on='influencer_id', how='left')
    
    # Merge with influencer data
    roi_data = roi_data.merge(influencers_df, on='influencer_id', how='left')
    
    # Calculate metrics
    roi_data['total_payout'] = roi_data['total_payout'].fillna(0)
    roi_data['revenue'] = roi_data['revenue'].fillna(0)
    
    # ROAS = Revenue / Cost (total_payout is the cost)
    roi_data['roas'] = roi_data.apply(
        lambda row: row['revenue'] / row['total_payout'] if row['total_payout'] > 0 else 0,
        axis=1
    )
    
    # Calculate baseline revenue (assume 20% would have purchased anyway)
    roi_data['baseline_revenue'] = roi_data['revenue'] * 0.2
    
    # Incremental ROAS = (Revenue - Baseline) / Cost
    roi_data['incremental_roas'] = roi_data.apply(
        lambda row: (row['revenue'] - row['baseline_revenue']) / row['total_payout'] 
        if row['total_payout'] > 0 else 0,
        axis=1
    )
    
    # Revenue per order
    roi_data['revenue_per_order'] = roi_data.apply(
        lambda row: row['revenue'] / row['orders'] if row['orders'] > 0 else 0,
        axis=1
    )
    
    # Cost per order
    roi_data['cost_per_order'] = roi_data.apply(
        lambda row: row['total_payout'] / row['orders'] if row['orders'] > 0 else 0,
        axis=1
    )
    
    return roi_data

def calculate_platform_metrics(posts_df, tracking_df, influencers_df):
    """Calculate performance metrics by platform"""
    
    # Since posts now have platform field, use it directly
    # Calculate platform engagement metrics
    platform_metrics = posts_df.groupby('platform').agg({
        'reach': ['sum', 'mean'],
        'likes': ['sum', 'mean'], 
        'comments': ['sum', 'mean'],
        'influencer_id': 'nunique'
    }).round(2)
    
    platform_metrics.columns = [
        'total_reach', 'avg_reach', 'total_likes', 'avg_likes',
        'total_comments', 'avg_comments', 'unique_influencers'
    ]
    
    # Calculate platform revenue metrics from tracking data
    # Merge tracking with influencers to get platform info
    tracking_with_influencers = tracking_df.merge(influencers_df[['influencer_id', 'platform']], on='influencer_id', how='left')
    platform_revenue = tracking_with_influencers.groupby('platform').agg({
        'revenue': 'sum',
        'orders': 'sum'
    }).round(2)
    
    # Merge engagement and revenue metrics
    platform_metrics = platform_metrics.merge(platform_revenue, left_index=True, right_index=True, how='left')
    platform_metrics = platform_metrics.fillna(0)
    
    # Calculate engagement rate by platform
    platform_metrics['engagement_rate'] = (
        (platform_metrics['total_likes'] + platform_metrics['total_comments']) / 
        platform_metrics['total_reach']
    ).fillna(0)
    
    return platform_metrics.reset_index()

def calculate_brand_metrics(tracking_df):
    """Calculate performance metrics by brand"""
    
    brand_metrics = tracking_df.groupby('brand').agg({
        'revenue': 'sum',
        'orders': 'sum',
        'influencer_id': 'nunique'
    }).round(2)
    
    brand_metrics.columns = ['total_revenue', 'total_orders', 'unique_influencers']
    
    # Calculate average order value by brand
    brand_metrics['avg_order_value'] = (
        brand_metrics['total_revenue'] / brand_metrics['total_orders']
    ).fillna(0).round(2)
    
    return brand_metrics.reset_index()

def calculate_time_series_metrics(tracking_df, posts_df):
    """Calculate time series metrics for trend analysis"""
    
    # Convert date columns
    tracking_df['date'] = pd.to_datetime(tracking_df['date'])
    posts_df['date'] = pd.to_datetime(posts_df['date'])
    
    # Daily revenue trends
    daily_revenue = tracking_df.groupby('date').agg({
        'revenue': 'sum',
        'orders': 'sum'
    }).reset_index()
    
    # Daily posting activity
    daily_posts = posts_df.groupby('date').agg({
        'post_id': 'count',
        'reach': 'sum',
        'likes': 'sum',
        'comments': 'sum'
    }).reset_index()
    daily_posts.columns = ['date', 'posts_count', 'total_reach', 'total_likes', 'total_comments']
    
    # Merge posting and revenue data
    time_series = daily_posts.merge(daily_revenue, on='date', how='outer')
    time_series = time_series.fillna(0)
    
    # Calculate 7-day rolling averages
    time_series['revenue_7d_avg'] = time_series['revenue'].rolling(window=7, min_periods=1).mean()
    time_series['orders_7d_avg'] = time_series['orders'].rolling(window=7, min_periods=1).mean()
    time_series['posts_7d_avg'] = time_series['posts_count'].rolling(window=7, min_periods=1).mean()
    
    return time_series.sort_values('date')

def calculate_influencer_performance_scores(roi_data, posts_df):
    """Calculate composite performance scores for influencers"""
    
    # Merge with posts data to get engagement metrics
    posts_engagement = calculate_engagement_rates(posts_df)
    influencer_engagement = posts_engagement.groupby('influencer_id').agg({
        'engagement_rate': 'mean',
        'reach': 'sum',
        'post_id': 'count'
    }).reset_index()
    influencer_engagement.columns = ['influencer_id', 'avg_engagement_rate', 'total_reach', 'posts_count']
    
    # Merge with ROI data
    performance_data = roi_data.merge(influencer_engagement, on='influencer_id', how='left')
    
    # Normalize metrics for scoring (0-100 scale)
    def normalize_score(series, reverse=False):
        if series.max() == series.min():
            return pd.Series([50] * len(series), index=series.index)
        
        normalized = (series - series.min()) / (series.max() - series.min()) * 100
        if reverse:
            normalized = 100 - normalized
        return normalized
    
    # Calculate component scores
    performance_data['roas_score'] = normalize_score(performance_data['roas'].fillna(0))
    performance_data['engagement_score'] = normalize_score(performance_data['avg_engagement_rate'].fillna(0))
    performance_data['volume_score'] = normalize_score(performance_data['orders'].fillna(0))
    performance_data['efficiency_score'] = normalize_score(performance_data['cost_per_order'].fillna(0), reverse=True)
    
    # Calculate composite performance score
    performance_data['performance_score'] = (
        performance_data['roas_score'] * 0.3 +
        performance_data['engagement_score'] * 0.25 +
        performance_data['volume_score'] * 0.25 +
        performance_data['efficiency_score'] * 0.2
    ).round(1)
    
    return performance_data

def identify_top_performers(performance_data, metric='performance_score', top_n=10):
    """Identify top performing influencers based on specified metric"""
    
    return performance_data.nlargest(top_n, metric)[
        ['influencer_id', 'name', 'category', 'platform', metric, 'roas', 'orders', 'revenue']
    ]

def identify_underperformers(performance_data, threshold_percentile=25):
    """Identify underperforming influencers based on performance score"""
    
    threshold = performance_data['performance_score'].quantile(threshold_percentile / 100)
    
    underperformers = performance_data[
        performance_data['performance_score'] <= threshold
    ][['influencer_id', 'name', 'category', 'platform', 'performance_score', 'roas', 'orders', 'revenue']]
    
    return underperformers.sort_values('performance_score')
