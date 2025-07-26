"""
File upload and data validation functions for HealthKart Influencer Dashboard
"""

import streamlit as st
import pandas as pd
import io

def validate_data_schema(df, expected_schema):
    """Validate if DataFrame matches expected schema"""
    
    missing_columns = set(expected_schema) - set(df.columns)
    extra_columns = set(df.columns) - set(expected_schema)
    
    issues = []
    
    if missing_columns:
        issues.append(f"Missing columns: {', '.join(missing_columns)}")
    
    if extra_columns:
        issues.append(f"Extra columns (will be ignored): {', '.join(extra_columns)}")
    
    return issues

def handle_file_upload(uploaded_files):
    """Handle multiple CSV file uploads and validation"""
    
    # Expected schemas for each file type
    schemas = {
        'influencers': ['influencer_id', 'name', 'category', 'gender', 'follower_count', 'platform'],
        'posts': ['influencer_id', 'platform', 'date', 'url', 'caption', 'reach', 'likes', 'comments'],
        'tracking_data': ['source', 'campaign', 'influencer_id', 'user_id', 'product', 'date', 'orders', 'revenue'],
        'payouts': ['influencer_id', 'basis', 'rate', 'orders', 'total_payout']
    }
    
    uploaded_data = {}
    
    for uploaded_file in uploaded_files:
        try:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)
            
            # Determine file type based on filename
            file_type = None
            filename = uploaded_file.name.lower()
            
            if 'influencer' in filename:
                file_type = 'influencers'
            elif 'post' in filename:
                file_type = 'posts'
            elif 'tracking' in filename:
                file_type = 'tracking_data'
            elif 'payout' in filename:
                file_type = 'payouts'
            else:
                st.warning(f"Cannot determine file type for {uploaded_file.name}. Please ensure filename contains 'influencer', 'post', 'tracking', or 'payout'.")
                continue
            
            # Validate schema
            if file_type in schemas:
                issues = validate_data_schema(df, schemas[file_type])
                
                if issues:
                    st.warning(f"Schema issues in {uploaded_file.name}:")
                    for issue in issues:
                        st.write(f"- {issue}")
                
                # Store the data even with minor issues (missing columns will be handled)
                uploaded_data[file_type] = df
                st.success(f"✅ {uploaded_file.name} uploaded successfully ({len(df)} rows)")
            
        except Exception as e:
            st.error(f"Error reading {uploaded_file.name}: {str(e)}")
    
    # Update session state with uploaded data
    if uploaded_data:
        if 'influencers' in uploaded_data:
            st.session_state.influencers_df = uploaded_data['influencers']
        if 'posts' in uploaded_data:
            st.session_state.posts_df = uploaded_data['posts']
        if 'tracking_data' in uploaded_data:
            st.session_state.tracking_df = uploaded_data['tracking_data']
        if 'payouts' in uploaded_data:
            st.session_state.payouts_df = uploaded_data['payouts']
        
        # Check if we have all required data
        required_data = ['influencers_df', 'posts_df', 'tracking_df', 'payouts_df']
        if all(getattr(st.session_state, attr, None) is not None for attr in required_data):
            st.session_state.data_loaded = True
            st.success("🎉 All data files uploaded successfully! You can now view the dashboard.")
        else:
            missing = [attr.replace('_df', '') for attr in required_data 
                      if getattr(st.session_state, attr, None) is None]
            st.info(f"Still need: {', '.join(missing)} data files")

def show_data_preview(df, title):
    """Show a preview of the uploaded data"""
    
    with st.expander(f"Preview {title} Data"):
        st.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        st.dataframe(df.head())
        
        # Show basic statistics for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            st.write("Numeric Column Statistics:")
            st.dataframe(df[numeric_cols].describe())

def validate_data_quality(influencers_df, posts_df, tracking_df, payouts_df):
    """Perform comprehensive data quality checks"""
    
    issues = []
    
    # Check for missing required fields
    if influencers_df['influencer_id'].isnull().any():
        issues.append("Missing influencer IDs in influencers data")
    
    if posts_df['influencer_id'].isnull().any():
        issues.append("Missing influencer IDs in posts data")
    
    if tracking_df['influencer_id'].isnull().any():
        issues.append("Missing influencer IDs in tracking data")
    
    # Check for orphaned records
    influencer_ids = set(influencers_df['influencer_id'].unique())
    post_influencer_ids = set(posts_df['influencer_id'].unique())
    tracking_influencer_ids = set(tracking_df['influencer_id'].unique())
    payout_influencer_ids = set(payouts_df['influencer_id'].unique())
    
    orphaned_posts = post_influencer_ids - influencer_ids
    if orphaned_posts:
        issues.append(f"Posts exist for non-existent influencers: {len(orphaned_posts)} influencers")
    
    orphaned_tracking = tracking_influencer_ids - influencer_ids
    if orphaned_tracking:
        issues.append(f"Tracking data exists for non-existent influencers: {len(orphaned_tracking)} influencers")
    
    orphaned_payouts = payout_influencer_ids - influencer_ids
    if orphaned_payouts:
        issues.append(f"Payouts exist for non-existent influencers: {len(orphaned_payouts)} influencers")
    
    # Check for data consistency
    if tracking_df['revenue'].isnull().any():
        issues.append("Missing revenue values in tracking data")
    
    if tracking_df['orders'].isnull().any():
        issues.append("Missing order counts in tracking data")
    
    # Check date formats
    try:
        pd.to_datetime(posts_df['date'])
    except:
        issues.append("Invalid date format in posts data")
    
    try:
        pd.to_datetime(tracking_df['date'])
    except:
        issues.append("Invalid date format in tracking data")
    
    return issues

def export_data_summary(influencers_df, posts_df, tracking_df, payouts_df):
    """Generate a summary report of the uploaded data"""
    
    summary = {
        "Data Summary": {
            "Total Influencers": len(influencers_df),
            "Total Posts": len(posts_df),
            "Total Tracking Records": len(tracking_df),
            "Total Payout Records": len(payouts_df),
            "Date Range": f"{tracking_df['date'].min()} to {tracking_df['date'].max()}",
            "Total Revenue": f"₹{tracking_df['revenue'].sum():,.2f}",
            "Total Orders": int(tracking_df['orders'].sum()),
            "Total Payouts": f"₹{payouts_df['total_payout'].sum():,.2f}"
        },
        "Platform Distribution": influencers_df['platform'].value_counts().to_dict(),
        "Category Distribution": influencers_df['category'].value_counts().to_dict(),
        "Brand Distribution": tracking_df['brand'].value_counts().to_dict() if 'brand' in tracking_df.columns else {}
    }
    
    return summary
