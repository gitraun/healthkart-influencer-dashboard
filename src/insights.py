"""
Insights generation and analysis for HealthKart Influencer Dashboard
"""

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
    """Generate comprehensive insights from the data"""
    
    # Calculate all metrics
    roi_data = calculate_roi_metrics(tracking_df, payouts_df, influencers_df)
    performance_data = calculate_influencer_performance_scores(roi_data, posts_df)
    platform_metrics = calculate_platform_metrics(posts_df, tracking_df, influencers_df)
    
    insights = {
        'summary': {},
        'top_performers': {},
        'underperformers': {},
        'platform_insights': {},
        'recommendations': []
    }
    
    # Summary insights
    insights['summary'] = {
        'total_revenue': tracking_df['revenue'].sum(),
        'total_cost': payouts_df['total_payout'].sum(),
        'overall_roas': tracking_df['revenue'].sum() / payouts_df['total_payout'].sum() if payouts_df['total_payout'].sum() > 0 else 0,
        'avg_performance_score': performance_data['performance_score'].mean(),
        'profitable_influencers_pct': (performance_data['roas'] > 1).mean() * 100,
        'best_platform': platform_metrics.loc[platform_metrics['total_revenue'].idxmax(), 'platform'] if not platform_metrics.empty else 'N/A'
    }
    
    # Top performers
    insights['top_performers'] = {
        'by_roas': identify_top_performers(performance_data, 'roas', 5),
        'by_revenue': identify_top_performers(performance_data, 'revenue', 5),
        'by_performance_score': identify_top_performers(performance_data, 'performance_score', 5)
    }
    
    # Underperformers
    insights['underperformers'] = identify_underperformers(performance_data, 25)
    
    # Platform insights
    insights['platform_insights'] = platform_metrics.sort_values('total_revenue', ascending=False)
    
    # Generate recommendations
    insights['recommendations'] = generate_recommendations(performance_data, platform_metrics, tracking_df)
    
    return insights

def generate_recommendations(performance_data, platform_metrics, tracking_df):
    """Generate actionable recommendations based on analysis"""
    
    recommendations = []
    
    # Budget allocation recommendations
    if not performance_data.empty:
        top_roas_platform = performance_data.groupby('platform')['roas'].mean().idxmax()
        recommendations.append({
            'type': 'Budget Allocation',
            'priority': 'High',
            'recommendation': f"Increase budget allocation to {top_roas_platform} influencers",
            'reason': f"{top_roas_platform} shows highest average ROAS",
            'action': f"Reallocate 20% of budget from underperforming platforms to {top_roas_platform}"
        })
    
    # Underperformer optimization
    underperformers = performance_data[performance_data['roas'] < 1.0]
    if len(underperformers) > 0:
        recommendations.append({
            'type': 'Performance Optimization',
            'priority': 'High',
            'recommendation': f"Review and optimize {len(underperformers)} underperforming influencers",
            'reason': f"{len(underperformers)} influencers have ROAS < 1.0",
            'action': "Renegotiate rates, improve content strategy, or discontinue partnerships"
        })
    
    # Content strategy recommendations
    if 'brand' in tracking_df.columns:
        best_brand = tracking_df.groupby('brand')['revenue'].sum().idxmax()
        recommendations.append({
            'type': 'Content Strategy',
            'priority': 'Medium',
            'recommendation': f"Focus content creation on {best_brand} products",
            'reason': f"{best_brand} generates highest revenue",
            'action': f"Create dedicated content campaigns highlighting {best_brand} benefits"
        })
    
    # Engagement optimization
    high_engagement_low_conversion = performance_data[
        (performance_data['avg_engagement_rate'] > performance_data['avg_engagement_rate'].quantile(0.75)) &
        (performance_data['roas'] < performance_data['roas'].median())
    ]
    
    if len(high_engagement_low_conversion) > 0:
        recommendations.append({
            'type': 'Conversion Optimization',
            'priority': 'Medium',
            'recommendation': "Optimize conversion funnel for high-engagement influencers",
            'reason': f"{len(high_engagement_low_conversion)} influencers have high engagement but low ROAS",
            'action': "Improve call-to-action, landing pages, and discount strategies"
        })
    
    # Scaling opportunities
    top_performers = performance_data[performance_data['roas'] > 3.0]
    if len(top_performers) > 0:
        recommendations.append({
            'type': 'Scaling',
            'priority': 'High',
            'recommendation': f"Scale successful partnerships with {len(top_performers)} high-performing influencers",
            'reason': f"These influencers show ROAS > 3.0",
            'action': "Increase post frequency, longer-term contracts, or exclusive partnerships"
        })
    
    return recommendations

def create_insights_dashboard(influencers_df, posts_df, tracking_df, payouts_df):
    """Create the insights dashboard"""
    
    st.header("🔍 Campaign Insights & Recommendations")
    
    # Generate insights
    insights = generate_insights(influencers_df, posts_df, tracking_df, payouts_df)
    
    # Executive Summary
    st.subheader("📈 Executive Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Overall ROAS", 
            f"{insights['summary']['overall_roas']:.2f}x",
            delta=f"{insights['summary']['overall_roas'] - 1:.2f}x vs break-even"
        )
    
    with col2:
        st.metric(
            "Profitable Influencers", 
            f"{insights['summary']['profitable_influencers_pct']:.0f}%"
        )
    
    with col3:
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
    st.subheader("📱 Platform Performance Analysis")
    
    if not insights['platform_insights'].empty:
        platform_data = insights['platform_insights']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                platform_data, 
                x='platform', 
                y='total_revenue',
                title="Revenue by Platform",
                labels={'total_revenue': 'Revenue (₹)', 'platform': 'Platform'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                platform_data, 
                x='platform', 
                y='engagement_rate',
                title="Engagement Rate by Platform",
                labels={'engagement_rate': 'Engagement Rate', 'platform': 'Platform'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Platform comparison table
        st.dataframe(
            platform_data,
            column_config={
                "total_revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f"),
                "avg_order_value": st.column_config.NumberColumn("AOV", format="₹%.0f"),
                "engagement_rate": st.column_config.NumberColumn("Engagement", format="%.3f")
            },
            use_container_width=True
        )
    
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
    
    # Persona Analysis
    st.subheader("👥 Influencer Persona Analysis")
    
    roi_data = calculate_roi_metrics(tracking_df, payouts_df, influencers_df)
    
    if not roi_data.empty:
        # Analyze performance by category and gender
        persona_analysis = roi_data.groupby(['category', 'gender']).agg({
            'roas': 'mean',
            'revenue': 'sum',
            'orders': 'sum',
            'influencer_id': 'count'
        }).round(2).reset_index()
        persona_analysis.columns = ['Category', 'Gender', 'Avg ROAS', 'Total Revenue', 'Total Orders', 'Count']
        
        # Create heatmap for ROAS by persona
        persona_pivot = persona_analysis.pivot(index='Category', columns='Gender', values='Avg ROAS')
        
        fig = px.imshow(
            persona_pivot,
            title="Average ROAS by Influencer Persona (Category × Gender)",
            labels=dict(x="Gender", y="Category", color="Avg ROAS"),
            aspect="auto"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Best performing personas
        st.write("**Best Performing Personas:**")
        best_personas = persona_analysis.nlargest(5, 'Avg ROAS')
        st.dataframe(
            best_personas,
            column_config={
                "Avg ROAS": st.column_config.NumberColumn("ROAS", format="%.2fx"),
                "Total Revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f")
            },
            use_container_width=True
        )

def export_insights_report(insights):
    """Export insights as a downloadable report"""
    
    report_data = []
    
    # Summary section
    report_data.append({
        'Section': 'Executive Summary',
        'Metric': 'Overall ROAS',
        'Value': f"{insights['summary']['overall_roas']:.2f}x",
        'Notes': 'Total revenue divided by total marketing cost'
    })
    
    report_data.append({
        'Section': 'Executive Summary',
        'Metric': 'Profitable Influencers',
        'Value': f"{insights['summary']['profitable_influencers_pct']:.0f}%",
        'Notes': 'Percentage of influencers with ROAS > 1.0'
    })
    
    # Top performers
    for i, performer in insights['top_performers']['by_roas'].head(3).iterrows():
        report_data.append({
            'Section': 'Top Performers',
            'Metric': f"Top ROAS: {performer['name']}",
            'Value': f"{performer['roas']:.2f}x",
            'Notes': f"{performer['platform']} - {performer['category']}"
        })
    
    # Recommendations
    for i, rec in enumerate(insights['recommendations'][:5], 1):
        report_data.append({
            'Section': 'Recommendations',
            'Metric': f"Rec {i}: {rec['type']}",
            'Value': rec['priority'],
            'Notes': rec['recommendation']
        })
    
    return pd.DataFrame(report_data)
