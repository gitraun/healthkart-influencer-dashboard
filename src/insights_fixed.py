import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.calculations import (
    calculate_roi_metrics, calculate_influencer_performance_scores,
    identify_top_performers, identify_underperformers,
    calculate_platform_metrics, calculate_brand_metrics
)

def generate_insights(influencers_df, posts_df, tracking_df, payouts_df):
    """Generate comprehensive insights from the data with robust error handling"""
    
    # Calculate all metrics with error handling
    try:
        roi_data = calculate_roi_metrics(tracking_df, payouts_df, influencers_df)
        performance_data = calculate_influencer_performance_scores(roi_data, posts_df)
        platform_metrics = calculate_platform_metrics(posts_df, tracking_df, influencers_df)
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        return None
    
    insights = {
        'summary': {},
        'top_performers': {},
        'underperformers': {},
        'platform_insights': {},
        'recommendations': []
    }
    
    # Summary insights
    total_revenue = tracking_df['revenue'].sum() if not tracking_df.empty else 0
    total_cost = payouts_df['total_payout'].sum() if not payouts_df.empty else 0
    overall_roas = total_revenue / total_cost if total_cost > 0 else 0
    
    insights['summary'] = {
        'total_revenue': total_revenue,
        'total_cost': total_cost,
        'overall_roas': overall_roas,
        'avg_performance_score': performance_data['performance_score'].mean() if not performance_data.empty and 'performance_score' in performance_data.columns else 0,
        'profitable_influencers_pct': (performance_data['roas'] > 1).mean() * 100 if not performance_data.empty and 'roas' in performance_data.columns else 0,
        'best_platform': platform_metrics.loc[platform_metrics['total_revenue'].idxmax(), 'platform'] if not platform_metrics.empty and len(platform_metrics) > 0 else 'Instagram'
    }
    
    # Top performers with error handling
    try:
        insights['top_performers'] = {
            'by_roas': identify_top_performers(performance_data, 'roas', 5) if not performance_data.empty else pd.DataFrame(),
            'by_revenue': identify_top_performers(performance_data, 'revenue', 5) if not performance_data.empty else pd.DataFrame(),
            'by_performance_score': identify_top_performers(performance_data, 'performance_score', 5) if not performance_data.empty else pd.DataFrame()
        }
    except Exception as e:
        insights['top_performers'] = {
            'by_roas': pd.DataFrame(),
            'by_revenue': pd.DataFrame(),
            'by_performance_score': pd.DataFrame()
        }
    
    # Underperformers
    try:
        insights['underperformers'] = identify_underperformers(performance_data, 25) if not performance_data.empty else pd.DataFrame()
    except Exception as e:
        insights['underperformers'] = pd.DataFrame()
    
    # Platform insights
    insights['platform_insights'] = platform_metrics
    
    # Generate recommendations
    insights['recommendations'] = generate_recommendations(performance_data, platform_metrics, tracking_df)
    
    return insights

def generate_recommendations(performance_data, platform_metrics, tracking_df):
    """Generate actionable recommendations based on analysis"""
    
    recommendations = []
    
    try:
        # Budget allocation recommendations - multi-platform support
        if not performance_data.empty and 'roas' in performance_data.columns:
            # Find top performing influencers by platform
            top_performers = performance_data.nlargest(5, 'roas')
            if not top_performers.empty:
                avg_top_roas = top_performers['roas'].mean()
                # Identify best performing platform
                if not platform_metrics.empty and 'total_revenue' in platform_metrics.columns:
                    best_platform = platform_metrics.loc[platform_metrics['total_revenue'].idxmax(), 'platform']
                else:
                    best_platform = "the top performing platform"
                
                recommendations.append({
                    'type': 'Budget Allocation',
                    'priority': 'High',
                    'recommendation': f"Increase budget allocation to top 5 influencers across all platforms",
                    'reason': f"Top performers show {avg_top_roas:.2f}x average ROAS, with {best_platform} leading revenue generation",
                    'action': f"Reallocate 20% of budget to top performing influencers, prioritizing {best_platform}"
                })
        
        # Underperformer optimization
        if not performance_data.empty and 'roas' in performance_data.columns:
            underperformers = performance_data[performance_data['roas'] < 1.0]
            if len(underperformers) > 0:
                recommendations.append({
                    'type': 'Performance Optimization',
                    'priority': 'High',
                    'recommendation': f"Review and optimize {len(underperformers)} underperforming influencers",
                    'reason': f"{len(underperformers)} influencers have ROAS < 1.0",
                    'action': "Renegotiate rates, improve content strategy, or discontinue partnerships"
                })
        
        # Engagement optimization
        if not performance_data.empty and 'avg_engagement_rate' in performance_data.columns:
            low_engagement = performance_data[performance_data['avg_engagement_rate'] < 0.03]  # Below 3%
            if len(low_engagement) > 0:
                recommendations.append({
                    'type': 'Content Strategy',
                    'priority': 'Medium',
                    'recommendation': f"Improve content strategy for {len(low_engagement)} low-engagement influencers",
                    'reason': f"{len(low_engagement)} influencers have engagement rates below 3%",
                    'action': "Provide content guidelines, creative briefs, and engagement best practices"
                })
        
    except Exception as e:
        recommendations.append({
            'type': 'System',
            'priority': 'Low',
            'recommendation': "Review data quality and calculation methods",
            'reason': f"Error in recommendation generation: {str(e)}",
            'action': "Check data integrity and calculation functions"
        })
    
    return recommendations

def create_insights_dashboard(influencers_df, posts_df, tracking_df, payouts_df):
    """Create the insights dashboard with comprehensive error handling"""
    
    st.title("🔍 Campaign Insights & Analytics")
    
    # Generate insights
    with st.spinner("Analyzing campaign performance..."):
        insights = generate_insights(influencers_df, posts_df, tracking_df, payouts_df)
    
    if insights is None:
        st.error("Unable to generate insights. Please check your data.")
        return
    
    # Executive Summary
    st.subheader("📊 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Revenue", 
            f"₹{insights['summary']['total_revenue']:,.0f}"
        )
    
    with col2:
        st.metric(
            "Overall ROAS", 
            f"{insights['summary']['overall_roas']:.2f}x"
        )
    
    with col3:
        st.metric(
            "Profitable Influencers", 
            f"{insights['summary']['profitable_influencers_pct']:.0f}%"
        )
    
    with col4:
        st.metric(
            "Avg Performance Score", 
            f"{insights['summary']['avg_performance_score']:.1f}/100"
        )
    
    # Key Insights Cards
    st.subheader("🎯 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Best Performing Platform**: {insights['summary']['best_platform']}
        
        This platform generates the highest revenue and should be prioritized for future campaigns.
        """)
    
    with col2:
        roi_status = "✅ Positive" if insights['summary']['overall_roas'] > 1 else "⚠️ Negative"
        st.info(f"""
        **Overall ROI Status**: {roi_status}
        
        Total Revenue: ₹{insights['summary']['total_revenue']:,.0f}
        Total Cost: ₹{insights['summary']['total_cost']:,.0f}
        """)
    
    # Top Performers Analysis
    st.subheader("🏆 Top Performers")
    
    tab1, tab2, tab3 = st.tabs(["By ROAS", "By Revenue", "By Overall Score"])
    
    with tab1:
        if not insights['top_performers']['by_roas'].empty:
            st.dataframe(
                insights['top_performers']['by_roas'],
                column_config={
                    "roas": st.column_config.NumberColumn("ROAS", format="%.2fx"),
                    "revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f")
                },
                use_container_width=True
            )
        else:
            st.info("No ROAS data available")
    
    with tab2:
        if not insights['top_performers']['by_revenue'].empty:
            st.dataframe(
                insights['top_performers']['by_revenue'],
                column_config={
                    "revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f"),
                    "roas": st.column_config.NumberColumn("ROAS", format="%.2fx")
                },
                use_container_width=True
            )
        else:
            st.info("No revenue data available")
    
    with tab3:
        if not insights['top_performers']['by_performance_score'].empty:
            st.dataframe(
                insights['top_performers']['by_performance_score'],
                column_config={
                    "performance_score": st.column_config.NumberColumn("Score", format="%.1f"),
                    "roas": st.column_config.NumberColumn("ROAS", format="%.2fx"),
                    "revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f")
                },
                use_container_width=True
            )
        else:
            st.info("No performance data available")
    
    # Platform Performance Comparison
    st.subheader("📱 Multi-Platform Performance Analysis")
    
    if not insights['platform_insights'].empty:
        platform_data = insights['platform_insights']
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'total_revenue' in platform_data.columns:
                fig = px.bar(
                    platform_data, 
                    x='platform', 
                    y='total_revenue',
                    title="Revenue by Platform",
                    labels={'total_revenue': 'Revenue (₹)', 'platform': 'Platform'}
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Revenue data not available")
        
        with col2:
            # Use the correct column name for engagement rate
            engagement_col = None
            for col in ['avg_engagement_rate', 'engagement_rate']:
                if col in platform_data.columns:
                    engagement_col = col
                    break
            
            if engagement_col:
                fig = px.bar(
                    platform_data, 
                    x='platform', 
                    y=engagement_col,
                    title="Engagement Rate by Platform",
                    labels={engagement_col: 'Engagement Rate', 'platform': 'Platform'}
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Engagement data not available")
        
        # Platform comparison table with available columns only
        st.subheader("Platform Metrics Overview")
        st.dataframe(platform_data, use_container_width=True)
    else:
        st.info("No platform data available")
    
    # Underperformers Analysis
    st.subheader("⚠️ Improvement Opportunities")
    
    if not insights['underperformers'].empty:
        st.write(f"Found {len(insights['underperformers'])} influencers in bottom 25% performance:")
        
        st.dataframe(
            insights['underperformers'],
            column_config={
                "performance_score": st.column_config.NumberColumn("Score", format="%.1f"),
                "roas": st.column_config.NumberColumn("ROAS", format="%.2fx"),
                "revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f")
            },
            use_container_width=True
        )
    else:
        st.success("No underperforming influencers identified!")
    
    # Recommendations
    st.subheader("💡 Actionable Recommendations")
    
    if insights['recommendations']:
        for i, rec in enumerate(insights['recommendations'], 1):
            priority_color = {
                'High': '🔴',
                'Medium': '🟡', 
                'Low': '🟢'
            }.get(rec['priority'], '⚪')
            
            with st.expander(f"{priority_color} {rec['type']} - {rec['priority']} Priority"):
                st.write(f"**Recommendation:** {rec['recommendation']}")
                st.write(f"**Reason:** {rec['reason']}")
                st.write(f"**Suggested Action:** {rec['action']}")
    else:
        st.info("No specific recommendations generated at this time.")
    
    # Campaign Performance Summary
    st.subheader("📈 Campaign Performance Summary")
    
    if not tracking_df.empty:
        # Create performance summary with platform distribution
        platform_counts = influencers_df['platform'].value_counts() if not influencers_df.empty else {}
        platform_summary = " | ".join([f"{platform}: {count}" for platform, count in platform_counts.items()])
        
        summary_metrics = {
            'Total Influencers': len(influencers_df),
            'Platform Distribution': platform_summary,
            'Total Posts': len(posts_df),
            'Total Orders': tracking_df['orders'].sum(),
            'Total Revenue': f"₹{tracking_df['revenue'].sum():,.0f}",
            'Average Order Value': f"₹{tracking_df['revenue'].sum() / tracking_df['orders'].sum():.0f}" if tracking_df['orders'].sum() > 0 else "N/A",
            'Marketing Cost': f"₹{payouts_df['total_payout'].sum():,.0f}",
            'Overall ROAS': f"{tracking_df['revenue'].sum() / payouts_df['total_payout'].sum():.2f}x" if payouts_df['total_payout'].sum() > 0 else "N/A"
        }
        
        # Display as metrics
        cols = st.columns(4)
        metrics_list = list(summary_metrics.items())
        
        for i, (metric, value) in enumerate(metrics_list):
            with cols[i % 4]:
                st.metric(metric, value)
    else:
        st.info("No campaign data available for summary")