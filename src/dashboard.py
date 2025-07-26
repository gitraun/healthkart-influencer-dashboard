"""
Dashboard visualization functions for HealthKart Influencer Campaign ROI Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.calculations import (
    calculate_engagement_rates, calculate_roi_metrics, 
    calculate_platform_metrics, calculate_brand_metrics,
    calculate_time_series_metrics, calculate_influencer_performance_scores
)

def create_performance_dashboard(influencers_df, posts_df, tracking_df, payouts_df):
    """Create the main performance dashboard"""
    
    st.header("📊 Campaign Performance Dashboard")
    
    # Calculate metrics
    posts_with_engagement = calculate_engagement_rates(posts_df)
    platform_metrics = calculate_platform_metrics(posts_df, tracking_df, influencers_df)
    brand_metrics = calculate_brand_metrics(tracking_df)
    time_series = calculate_time_series_metrics(tracking_df, posts_df)
    
    # Sidebar filters
    st.sidebar.subheader("Filters")
    
    # Platform filter
    platforms = ['All'] + list(influencers_df['platform'].unique())
    selected_platform = st.sidebar.selectbox("Platform", platforms)
    
    # Category filter
    categories = ['All'] + list(influencers_df['category'].unique())
    selected_category = st.sidebar.selectbox("Category", categories)
    
    # Brand filter (if available in tracking data)
    if 'brand' in tracking_df.columns:
        brands = ['All'] + list(tracking_df['brand'].unique())
        selected_brand = st.sidebar.selectbox("Brand", brands)
    else:
        selected_brand = 'All'
    
    # Apply filters
    filtered_influencers = influencers_df.copy()
    
    if selected_platform != 'All':
        filtered_influencers = filtered_influencers[filtered_influencers['platform'] == selected_platform]
    
    if selected_category != 'All':
        filtered_influencers = filtered_influencers[filtered_influencers['category'] == selected_category]
    
    filtered_influencer_ids = filtered_influencers['influencer_id'].tolist()
    
    # Filter other dataframes
    filtered_posts = posts_df[posts_df['influencer_id'].isin(filtered_influencer_ids)]
    filtered_tracking = tracking_df[tracking_df['influencer_id'].isin(filtered_influencer_ids)]
    
    if selected_brand != 'All' and 'brand' in tracking_df.columns:
        filtered_tracking = filtered_tracking[filtered_tracking['brand'] == selected_brand]
    
    # Key Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_revenue = filtered_tracking['revenue'].sum()
        st.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    
    with col2:
        total_orders = filtered_tracking['orders'].sum()
        st.metric("Total Orders", f"{total_orders:,}")
    
    with col3:
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        st.metric("Avg Order Value", f"₹{avg_order_value:.0f}")
    
    with col4:
        total_reach = filtered_posts['reach'].sum()
        st.metric("Total Reach", f"{total_reach:,}")
    
    with col5:
        active_influencers = len(filtered_influencers)
        st.metric("Active Influencers", active_influencers)
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue by Platform")
        if not filtered_tracking.empty:
            # Merge with influencer data to get platform info
            tracking_with_platform = filtered_tracking.merge(
                filtered_influencers[['influencer_id', 'platform']], 
                on='influencer_id', 
                how='left'
            )
            platform_revenue = tracking_with_platform.groupby('platform')['revenue'].sum().reset_index()
            
            fig = px.bar(
                platform_revenue, 
                x='platform', 
                y='revenue',
                title="Revenue by Platform",
                labels={'revenue': 'Revenue (₹)', 'platform': 'Platform'}
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for selected filters")
    
    with col2:
        st.subheader("Orders by Category")
        if not filtered_tracking.empty:
            tracking_with_category = filtered_tracking.merge(
                filtered_influencers[['influencer_id', 'category']], 
                on='influencer_id', 
                how='left'
            )
            category_orders = tracking_with_category.groupby('category')['orders'].sum().reset_index()
            
            fig = px.pie(
                category_orders, 
                values='orders', 
                names='category',
                title="Orders Distribution by Category"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for selected filters")
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Engagement Rate by Platform")
        if not filtered_posts.empty:
            posts_with_engagement_filtered = calculate_engagement_rates(filtered_posts)
            posts_with_platform = posts_with_engagement_filtered.merge(
                filtered_influencers[['influencer_id', 'platform']], 
                on='influencer_id', 
                how='left'
            )
            # Since all data is Instagram now, create simple engagement data
            platform_engagement = pd.DataFrame({
                'platform': ['Instagram'],
                'engagement_rate': [posts_with_platform['engagement_rate'].mean()]
            })
            
            fig = px.bar(
                platform_engagement, 
                x='platform', 
                y='engagement_rate',
                title="Average Engagement Rate by Platform",
                labels={'engagement_rate': 'Engagement Rate', 'platform': 'Platform'}
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for selected filters")
    
    with col2:
        st.subheader("Revenue Trend Over Time")
        if not filtered_tracking.empty:
            daily_revenue = filtered_tracking.groupby('date')['revenue'].sum().reset_index()
            daily_revenue['date'] = pd.to_datetime(daily_revenue['date'])
            daily_revenue = daily_revenue.sort_values('date')
            
            fig = px.line(
                daily_revenue, 
                x='date', 
                y='revenue',
                title="Daily Revenue Trend",
                labels={'revenue': 'Revenue (₹)', 'date': 'Date'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for selected filters")
    
    # Top Performers Table
    st.subheader("Top Performing Influencers")
    if not filtered_tracking.empty:
        influencer_performance = filtered_tracking.groupby('influencer_id').agg({
            'revenue': 'sum',
            'orders': 'sum'
        }).reset_index()
        
        influencer_performance = influencer_performance.merge(
            filtered_influencers[['influencer_id', 'name', 'category', 'platform', 'follower_count']], 
            on='influencer_id', 
            how='left'
        )
        
        # Calculate revenue per follower
        influencer_performance['revenue_per_follower'] = (
            influencer_performance['revenue'] / influencer_performance['follower_count']
        ).round(4)
        
        top_performers = influencer_performance.nlargest(10, 'revenue')[
            ['name', 'category', 'platform', 'revenue', 'orders', 'revenue_per_follower']
        ]
        
        st.dataframe(
            top_performers,
            column_config={
                "revenue": st.column_config.NumberColumn(
                    "Revenue",
                    format="₹%.0f"
                ),
                "revenue_per_follower": st.column_config.NumberColumn(
                    "Revenue per Follower",
                    format="₹%.4f"
                )
            },
            use_container_width=True
        )
    else:
        st.info("No performance data available for selected filters")

def create_roi_dashboard(influencers_df, posts_df, tracking_df, payouts_df):
    """Create ROI analysis dashboard"""
    
    st.header("💰 ROI & ROAS Analysis")
    
    # Calculate ROI metrics
    roi_data = calculate_roi_metrics(tracking_df, payouts_df, influencers_df)
    performance_data = calculate_influencer_performance_scores(roi_data, posts_df)
    
    # Sidebar filters
    st.sidebar.subheader("ROI Filters")
    
    # Minimum ROAS filter
    min_roas = st.sidebar.slider("Minimum ROAS", 0.0, 10.0, 0.0, 0.1)
    filtered_roi = performance_data[performance_data['roas'] >= min_roas]
    
    # Platform filter for ROI
    platforms = ['All'] + list(influencers_df['platform'].unique())
    selected_platform = st.sidebar.selectbox("Platform (ROI)", platforms)
    
    if selected_platform != 'All':
        filtered_roi = filtered_roi[filtered_roi['platform'] == selected_platform]
    
    # Key ROI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_roas = filtered_roi['roas'].mean()
        st.metric("Average ROAS", f"{avg_roas:.2f}x")
    
    with col2:
        avg_incremental_roas = filtered_roi['incremental_roas'].mean()
        st.metric("Avg Incremental ROAS", f"{avg_incremental_roas:.2f}x")
    
    with col3:
        total_cost = filtered_roi['total_payout'].sum()
        st.metric("Total Marketing Cost", f"₹{total_cost:,.0f}")
    
    with col4:
        avg_performance_score = filtered_roi['performance_score'].mean()
        st.metric("Avg Performance Score", f"{avg_performance_score:.1f}/100")
    
    # ROAS Distribution Chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("ROAS Distribution")
        if not filtered_roi.empty:
            fig = px.histogram(
                filtered_roi, 
                x='roas', 
                nbins=20,
                title="ROAS Distribution",
                labels={'roas': 'ROAS', 'count': 'Number of Influencers'}
            )
            fig.add_vline(x=1, line_dash="dash", line_color="red", 
                         annotation_text="Break-even (ROAS = 1)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for selected filters")
    
    with col2:
        st.subheader("ROAS vs Cost")
        if not filtered_roi.empty:
            fig = px.scatter(
                filtered_roi, 
                x='total_payout', 
                y='roas',
                size='orders',
                color='category',
                hover_data=['name'],
                title="ROAS vs Marketing Cost",
                labels={'total_payout': 'Marketing Cost (₹)', 'roas': 'ROAS'}
            )
            fig.add_hline(y=1, line_dash="dash", line_color="red")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for selected filters")
    
    # Platform ROI Comparison
    st.subheader("ROI by Platform")
    if not filtered_roi.empty:
        platform_roi = filtered_roi.groupby('platform').agg({
            'roas': 'mean',
            'incremental_roas': 'mean',
            'total_payout': 'sum',
            'revenue': 'sum',
            'orders': 'sum'
        }).round(2).reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='ROAS',
            x=platform_roi['platform'],
            y=platform_roi['roas'],
            yaxis='y',
            offsetgroup=1
        ))
        
        fig.add_trace(go.Bar(
            name='Incremental ROAS',
            x=platform_roi['platform'],
            y=platform_roi['incremental_roas'],
            yaxis='y',
            offsetgroup=2
        ))
        
        fig.update_layout(
            title='Average ROAS by Platform',
            xaxis_title='Platform',
            yaxis_title='ROAS',
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ROI Performance Table
    st.subheader("Detailed ROI Analysis")
    if not filtered_roi.empty:
        roi_table = filtered_roi[
            ['name', 'category', 'platform', 'roas', 'incremental_roas', 
             'revenue', 'total_payout', 'orders', 'performance_score']
        ].sort_values('roas', ascending=False)
        
        st.dataframe(
            roi_table,
            column_config={
                "roas": st.column_config.NumberColumn(
                    "ROAS",
                    format="%.2fx"
                ),
                "incremental_roas": st.column_config.NumberColumn(
                    "Incremental ROAS",
                    format="%.2fx"
                ),
                "revenue": st.column_config.NumberColumn(
                    "Revenue",
                    format="₹%.0f"
                ),
                "total_payout": st.column_config.NumberColumn(
                    "Cost",
                    format="₹%.0f"
                ),
                "performance_score": st.column_config.NumberColumn(
                    "Score",
                    format="%.1f"
                )
            },
            use_container_width=True
        )
    
    # ROI Insights
    st.subheader("ROI Insights")
    if not filtered_roi.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**High Performers (ROAS > 3.0):**")
            high_performers = filtered_roi[filtered_roi['roas'] > 3.0]
            if not high_performers.empty:
                for _, performer in high_performers.head(5).iterrows():
                    st.write(f"• {performer['name']} ({performer['platform']}) - {performer['roas']:.2f}x ROAS")
            else:
                st.write("No influencers with ROAS > 3.0")
        
        with col2:
            st.write("**Improvement Opportunities (ROAS < 1.0):**")
            low_performers = filtered_roi[filtered_roi['roas'] < 1.0]
            if not low_performers.empty:
                for _, performer in low_performers.head(5).iterrows():
                    st.write(f"• {performer['name']} ({performer['platform']}) - {performer['roas']:.2f}x ROAS")
            else:
                st.write("All influencers have positive ROI!")
