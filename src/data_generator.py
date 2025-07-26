"""
Mock data generation for HealthKart Influencer Campaign ROI Dashboard
Generates realistic sample datasets for testing and demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_mock_data():
    """Generate complete mock dataset for the dashboard"""
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Set random seed for reproducible data
    np.random.seed(42)
    random.seed(42)
    
    # Generate influencers data
    influencers_df = generate_influencers_data()
    
    # Generate posts data
    posts_df = generate_posts_data(influencers_df)
    
    # Generate tracking data
    tracking_df = generate_tracking_data(influencers_df, posts_df)
    
    # Generate payouts data
    payouts_df = generate_payouts_data(influencers_df, tracking_df)
    
    # Save to CSV files
    influencers_df.to_csv('data/influencers.csv', index=False)
    posts_df.to_csv('data/posts.csv', index=False)
    tracking_df.to_csv('data/tracking_data.csv', index=False)
    payouts_df.to_csv('data/payouts.csv', index=False)
    
    return influencers_df, posts_df, tracking_df, payouts_df

def generate_influencers_data(num_influencers=50):
    """Generate mock influencers dataset"""
    
    categories = ['Fitness', 'Nutrition', 'Lifestyle', 'Health', 'Sports', 'Wellness']
    platforms = ['Instagram', 'YouTube', 'Twitter', 'Facebook', 'TikTok']
    genders = ['Male', 'Female', 'Non-binary']
    
    # Indian influencer names for realism
    first_names = [
        'Arjun', 'Priya', 'Rahul', 'Sneha', 'Vikram', 'Kavya', 'Rohit', 'Ananya',
        'Aditya', 'Meera', 'Karan', 'Pooja', 'Siddharth', 'Riya', 'Akash', 'Divya',
        'Nikhil', 'Shreya', 'Varun', 'Ishita', 'Manish', 'Nisha', 'Rajesh', 'Tanya',
        'Sameer', 'Ritika', 'Gaurav', 'Simran', 'Deepak', 'Natasha'
    ]
    
    last_names = [
        'Sharma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Agarwal', 'Jain', 'Malhotra',
        'Chopra', 'Verma', 'Arora', 'Reddy', 'Nair', 'Iyer', 'Mehta', 'Shah',
        'Bansal', 'Sinha', 'Joshi', 'Kapoor', 'Saxena', 'Mishra', 'Pandey', 'Rao'
    ]
    
    data = []
    for i in range(num_influencers):
        # Generate follower count with realistic distribution
        follower_tier = random.choices(
            ['micro', 'mid', 'macro', 'mega'],
            weights=[40, 35, 20, 5]
        )[0]
        
        if follower_tier == 'micro':
            follower_count = random.randint(10000, 100000)
        elif follower_tier == 'mid':
            follower_count = random.randint(100000, 500000)
        elif follower_tier == 'macro':
            follower_count = random.randint(500000, 1000000)
        else:  # mega
            follower_count = random.randint(1000000, 5000000)
        
        data.append({
            'influencer_id': f'INF_{i+1:03d}',
            'name': f"{random.choice(first_names)} {random.choice(last_names)}",
            'category': random.choice(categories),
            'gender': random.choice(genders),
            'follower_count': follower_count,
            'platform': random.choice(platforms)
        })
    
    return pd.DataFrame(data)

def generate_posts_data(influencers_df, posts_per_influencer_range=(5, 15)):
    """Generate mock posts dataset"""
    
    data = []
    post_id = 1
    
    # Sample captions for different categories
    caption_templates = {
        'Fitness': [
            "Just crushed my workout with @MuscleBlaze protein! 💪 #fitness #protein",
            "Pre-workout fuel with @HKVitals supplements 🔥 #workout #energy",
            "Recovery day essentials from @Gritzo 💯 #recovery #nutrition"
        ],
        'Nutrition': [
            "Starting my day with @HKVitals multivitamins ☀️ #health #nutrition",
            "Post-workout nutrition with @MuscleBlaze 🥤 #protein #recovery",
            "Kids nutrition made easy with @Gritzo 👶 #kidshealth #nutrition"
        ],
        'Health': [
            "Daily wellness routine with @HKVitals 🌱 #wellness #health",
            "Supporting immunity with quality supplements 🛡️ #immunity #health",
            "Healthy lifestyle choices matter 💚 #health #lifestyle"
        ],
        'Lifestyle': [
            "Living my best life with proper nutrition 🌟 #lifestyle #health",
            "Balance is key - fitness, nutrition, wellness 🧘‍♀️ #balance #wellness",
            "Investing in my health daily 💪 #selfcare #health"
        ],
        'Sports': [
            "Game day preparation with @MuscleBlaze 🏆 #sports #performance",
            "Athletic performance through proper nutrition 🥇 #athletes #nutrition",
            "Training hard, recovering smart 💪 #training #recovery"
        ],
        'Wellness': [
            "Holistic wellness approach with @HKVitals 🌿 #wellness #holistic",
            "Mind, body, soul - complete wellness 🧘 #mindfulness #wellness",
            "Wellness journey continues 🌟 #wellnessjourney #health"
        ]
    }
    
    for _, influencer in influencers_df.iterrows():
        num_posts = random.randint(*posts_per_influencer_range)
        
        for _ in range(num_posts):
            # Generate post date within last 90 days
            post_date = datetime.now() - timedelta(days=random.randint(1, 90))
            
            # Generate engagement metrics based on follower count
            follower_count = influencer['follower_count']
            
            # Reach is typically 10-30% of followers
            reach = int(follower_count * random.uniform(0.1, 0.3))
            
            # Engagement rate varies by platform and influencer tier
            if follower_count < 100000:  # Micro influencers have higher engagement
                engagement_rate = random.uniform(0.03, 0.08)
            elif follower_count < 500000:  # Mid-tier
                engagement_rate = random.uniform(0.02, 0.05)
            else:  # Macro/mega influencers
                engagement_rate = random.uniform(0.01, 0.03)
            
            likes = int(reach * engagement_rate * random.uniform(0.8, 1.2))
            comments = int(likes * random.uniform(0.02, 0.05))
            
            # Get appropriate caption and ensure no commas to avoid CSV parsing issues
            category_captions = caption_templates.get(influencer['category'], caption_templates['Health'])
            caption = random.choice(category_captions).replace(',', ' -')
            
            data.append({
                'post_id': f'POST_{post_id:04d}',
                'influencer_id': influencer['influencer_id'],
                'platform': influencer['platform'],
                'date': post_date.strftime('%Y-%m-%d'),
                'url': f"https://{influencer['platform'].lower()}.com/post/{post_id}",
                'caption': caption,
                'reach': reach,
                'likes': likes,
                'comments': comments
            })
            post_id += 1
    
    return pd.DataFrame(data)

def generate_tracking_data(influencers_df, posts_df):
    """Generate mock tracking/attribution data"""
    
    brands = ['MuscleBlaze', 'HKVitals', 'Gritzo']
    products = {
        'MuscleBlaze': ['Whey Protein', 'BCAA', 'Pre-Workout', 'Mass Gainer', 'Creatine'],
        'HKVitals': ['Multivitamin', 'Vitamin D', 'Omega-3', 'Immunity Booster', 'Biotin'],
        'Gritzo': ['Kids Protein', 'Teen Nutrition', 'Growth Formula', 'DHA Supplement']
    }
    
    data = []
    tracking_id = 1
    
    # Generate tracking data for each post
    for _, post in posts_df.iterrows():
        # Not all posts generate orders (60% conversion rate)
        if random.random() < 0.6:
            continue
        
        influencer_id = post['influencer_id']
        post_date = datetime.strptime(post['date'], '%Y-%m-%d')
        
        # Generate orders for 1-14 days after post
        for day_offset in range(1, random.randint(2, 15)):
            order_date = post_date + timedelta(days=day_offset)
            
            # Probability decreases over time
            if random.random() < (0.5 ** (day_offset / 3)):
                brand = random.choice(brands)
                product = random.choice(products[brand])
                
                # Generate realistic order value based on product type
                if 'Protein' in product:
                    base_price = random.uniform(1500, 3000)
                elif 'Vitamin' in product or 'Supplement' in product:
                    base_price = random.uniform(500, 1500)
                else:
                    base_price = random.uniform(800, 2000)
                
                revenue = base_price * random.uniform(0.9, 1.1)  # Add some variance
                
                data.append({
                    'tracking_id': f'TRK_{tracking_id:05d}',
                    'source': f"{post['platform']}_influencer",
                    'campaign': f"{brand}_{influencer_id}_{post['date']}",
                    'influencer_id': influencer_id,
                    'user_id': f'USER_{random.randint(10000, 99999)}',
                    'brand': brand,
                    'product': product,
                    'date': order_date.strftime('%Y-%m-%d'),
                    'orders': 1,
                    'revenue': round(revenue, 2)
                })
                tracking_id += 1
    
    return pd.DataFrame(data)

def generate_payouts_data(influencers_df, tracking_df):
    """Generate mock payouts data"""
    
    data = []
    
    # Group tracking data by influencer
    influencer_revenue = tracking_df.groupby('influencer_id').agg({
        'orders': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    for _, influencer in influencers_df.iterrows():
        influencer_id = influencer['influencer_id']
        follower_count = influencer['follower_count']
        
        # Determine payout basis and rates based on influencer tier
        if follower_count < 100000:
            # Micro influencers often get paid per post
            basis = 'post'
            rate = random.uniform(5000, 15000)  # INR per post
        else:
            # Larger influencers often get revenue sharing
            basis = random.choice(['post', 'order'])
            if basis == 'post':
                rate = random.uniform(15000, 50000)  # INR per post
            else:
                rate = random.uniform(0.05, 0.15)  # Percentage of revenue
        
        # Calculate orders and payout
        influencer_orders = influencer_revenue[
            influencer_revenue['influencer_id'] == influencer_id
        ]
        
        if len(influencer_orders) > 0:
            orders = influencer_orders.iloc[0]['orders']
            revenue = influencer_orders.iloc[0]['revenue']
            
            if basis == 'post':
                # For post-based payment, assume average of 3 posts per influencer
                posts_count = 3  # Fixed number since we don't have access to posts_df here
                total_payout = rate * posts_count
            else:
                total_payout = revenue * rate
        else:
            orders = 0
            total_payout = 0
        
        data.append({
            'influencer_id': influencer_id,
            'basis': basis,
            'rate': round(rate, 4),
            'orders': int(orders),
            'total_payout': round(total_payout, 2)
        })
    
    return pd.DataFrame(data)
