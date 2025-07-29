"""
HealthKart Influencer Campaign ROI Dashboard
Main Streamlit application entry point
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Import custom modules
from src.data_generator import generate_mock_data
from src.calculations import calculate_roi_metrics, calculate_engagement_rates
from src.upload import handle_file_upload, validate_data_schema
from src.dashboard import create_performance_dashboard, create_roi_dashboard
from src.insights_fixed import create_insights_dashboard

# Page configuration
st.set_page_config(
    page_title="Campaign Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'influencers_df' not in st.session_state:
    st.session_state.influencers_df = None
if 'posts_df' not in st.session_state:
    st.session_state.posts_df = None
if 'tracking_df' not in st.session_state:
    st.session_state.tracking_df = None
if 'payouts_df' not in st.session_state:
    st.session_state.payouts_df = None

def load_default_data():
    """Load default mock data if available"""
    try:
        # Check if mock data files exist
        data_files = {
            'influencers': 'data/influencers.csv',
            'posts': 'data/posts.csv',
            'tracking': 'data/tracking_data.csv',
            'payouts': 'data/payouts.csv'
        }
        
        if all(os.path.exists(file) for file in data_files.values()):
            st.session_state.influencers_df = pd.read_csv(data_files['influencers'])
            st.session_state.posts_df = pd.read_csv(data_files['posts'])
            st.session_state.tracking_df = pd.read_csv(data_files['tracking'])
            st.session_state.payouts_df = pd.read_csv(data_files['payouts'])
            st.session_state.data_loaded = True
            return True
    except Exception as e:
        st.error(f"Error loading default data: {str(e)}")
    return False

def main():
    """Main application function"""
    
    # Header
    st.title("📈 HealthKart Influencer Campaign ROI Dashboard")
    st.markdown("Track, analyze and optimize influencer campaigns across platforms and brands")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        ["Data Upload", "Campaign Performance", "ROI Analysis", "Insights", "Export Data"]
    )
    
    # Load default data if not already loaded
    if not st.session_state.data_loaded:
        if load_default_data():
            st.sidebar.success("✅ Default data loaded")
        else:
            st.sidebar.warning("⚠️ No default data found. Please upload data.")
    
    # Data Upload Page
    if page == "Data Upload":
        st.header("📁 Data Upload & Management")
        
        # Option to generate mock data
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Generate Mock Data")
            if st.button("Generate Sample Dataset", type="primary"):
                with st.spinner("Generating mock data..."):
                    try:
                        generate_mock_data()
                        load_default_data()
                        st.success("Mock data generated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating mock data: {str(e)}")
        
        with col2:
            st.subheader("Upload Custom Data")
            uploaded_files = st.file_uploader(
                "Upload CSV files",
                type=['csv'],
                accept_multiple_files=True,
                help="Upload influencers.csv, posts.csv, tracking_data.csv, and payouts.csv"
            )
            
            if uploaded_files:
                handle_file_upload(uploaded_files)
        
        # Display current data status
        if st.session_state.data_loaded:
            st.subheader("📊 Current Data Summary")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Influencers", len(st.session_state.influencers_df) if st.session_state.influencers_df is not None else 0)
            with col2:
                st.metric("Posts", len(st.session_state.posts_df) if st.session_state.posts_df is not None else 0)
            with col3:
                st.metric("Tracking Records", len(st.session_state.tracking_df) if st.session_state.tracking_df is not None else 0)
            with col4:
                st.metric("Payout Records", len(st.session_state.payouts_df) if st.session_state.payouts_df is not None else 0)
    
    # Campaign Performance Page
    elif page == "Campaign Performance":
        if not st.session_state.data_loaded:
            st.warning("Please upload data first to view campaign performance.")
            return
        
        create_performance_dashboard(
            st.session_state.influencers_df,
            st.session_state.posts_df,
            st.session_state.tracking_df,
            st.session_state.payouts_df
        )
    
    # ROI Analysis Page
    elif page == "ROI Analysis":
        if not st.session_state.data_loaded:
            st.warning("Please upload data first to view ROI analysis.")
            return
        
        create_roi_dashboard(
            st.session_state.influencers_df,
            st.session_state.posts_df,
            st.session_state.tracking_df,
            st.session_state.payouts_df
        )
    
    # Insights Page
    elif page == "Insights":
        if not st.session_state.data_loaded:
            st.warning("Please upload data first to view insights.")
            return
        
        create_insights_dashboard(
            st.session_state.influencers_df,
            st.session_state.posts_df,
            st.session_state.tracking_df,
            st.session_state.payouts_df
        )
    
    # Export Data Page
    elif page == "Export Data":
        if not st.session_state.data_loaded:
            st.warning("Please upload data first to export reports.")
            return
        
        st.header("📤 Export Data & Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Download Raw Data")
            
            # Influencers data
            influencers_csv = st.session_state.influencers_df.to_csv(index=False)
            st.download_button(
                label="📱 Download Instagram Influencers",
                data=influencers_csv,
                file_name="instagram_influencers.csv",
                mime="text/csv"
            )
            
            # Posts data
            posts_csv = st.session_state.posts_df.to_csv(index=False)
            st.download_button(
                label="📝 Download Instagram Posts",
                data=posts_csv,
                file_name="instagram_posts.csv",
                mime="text/csv"
            )
            
            # Tracking data
            tracking_csv = st.session_state.tracking_df.to_csv(index=False)
            st.download_button(
                label="📊 Download Campaign Tracking",
                data=tracking_csv,
                file_name="instagram_tracking.csv",
                mime="text/csv"
            )
            
            # Payouts data
            payouts_csv = st.session_state.payouts_df.to_csv(index=False)
            st.download_button(
                label="💰 Download Payout Data",
                data=payouts_csv,
                file_name="instagram_payouts.csv",
                mime="text/csv"
            )
        
        with col2:
            st.subheader("Download Analysis Reports")
            
            # ROI Analysis Report
            try:
                roi_data = calculate_roi_metrics(
                    st.session_state.tracking_df,
                    st.session_state.payouts_df,
                    st.session_state.influencers_df
                )
                roi_csv = roi_data.to_csv(index=False)
                st.download_button(
                    label="📈 Download ROI Analysis",
                    data=roi_csv,
                    file_name=f"instagram_roi_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error generating ROI report: {str(e)}")
            
            # Campaign Summary Report
            summary_data = {
                'Metric': ['Total Revenue', 'Total Orders', 'Instagram Influencers', 'Average ROAS', 'Total Marketing Cost'],
                'Value': [
                    f"₹{st.session_state.tracking_df['revenue'].sum():,.2f}",
                    f"{st.session_state.tracking_df['orders'].sum():,}",
                    f"{len(st.session_state.influencers_df):,}",
                    f"{st.session_state.tracking_df['revenue'].sum() / st.session_state.payouts_df['total_payout'].sum():.2f}x" if st.session_state.payouts_df['total_payout'].sum() > 0 else "N/A",
                    f"₹{st.session_state.payouts_df['total_payout'].sum():,.2f}"
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_csv = summary_df.to_csv(index=False)
            st.download_button(
                label="📋 Download Campaign Summary",
                data=summary_csv,
                file_name=f"instagram_campaign_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        # Display current data overview
        st.subheader("📊 Current Data Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Instagram Influencers", len(st.session_state.influencers_df))
        with col2:
            st.metric("Total Posts", len(st.session_state.posts_df))
        with col3:
            st.metric("Total Orders", st.session_state.tracking_df['orders'].sum())
        with col4:
            st.metric("Total Revenue", f"₹{st.session_state.tracking_df['revenue'].sum():,.0f}")

if __name__ == "__main__":
    main()
