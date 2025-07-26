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
from src.insights import generate_insights, create_insights_dashboard

# Page configuration
st.set_page_config(
    page_title="HealthKart Influencer ROI Dashboard",
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
            if st.button("Download Influencers CSV"):
                csv = st.session_state.influencers_df.to_csv(index=False)
                st.download_button(
                    label="Download influencers.csv",
                    data=csv,
                    file_name="influencers.csv",
                    mime="text/csv"
                )
            
            if st.button("Download Posts CSV"):
                csv = st.session_state.posts_df.to_csv(index=False)
                st.download_button(
                    label="Download posts.csv",
                    data=csv,
                    file_name="posts.csv",
                    mime="text/csv"
                )
        
        with col2:
            st.subheader("Download Analysis Reports")
            if st.button("Generate ROI Report"):
                # Generate comprehensive ROI report
                roi_data = calculate_roi_metrics(
                    st.session_state.tracking_df,
                    st.session_state.payouts_df,
                    st.session_state.influencers_df
                )
                csv = roi_data.to_csv(index=False)
                st.download_button(
                    label="Download ROI Report",
                    data=csv,
                    file_name=f"roi_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
