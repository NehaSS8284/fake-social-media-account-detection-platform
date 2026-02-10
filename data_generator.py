"""
DATA GENERATOR - Creates realistic fake social media accounts for testing
This generates different types of accounts: normal users, businesses, bots, scammers
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_mock_accounts(num_accounts=50):
    """
    Generate realistic social media account data
    
    Returns: DataFrame with account information
    """
    
    accounts = []
    
    # Account types and their proportions
    account_types = [
        ('normal', 0.4),      # 40% normal users
        ('business', 0.15),   # 15% businesses
        ('bot', 0.25),        # 25% bots
        ('scammer', 0.20)     # 20% scammers
    ]
    
    for i in range(num_accounts):
        # Randomly select account type based on proportions
        account_type = random.choices(
            [t[0] for t in account_types],
            weights=[t[1] for t in account_types]
        )[0]
        
        # Generate account based on type
        if account_type == 'normal':
            account = generate_normal_user(i)
        elif account_type == 'business':
            account = generate_business_account(i)
        elif account_type == 'bot':
            account = generate_bot_account(i)
        else:  # scammer
            account = generate_scammer_account(i)
        
        accounts.append(account)
    
    return pd.DataFrame(accounts)


def generate_normal_user(id_num):
    """Generate a normal, legitimate user account"""
    
    # Random account age (1 month to 5 years)
    days_old = random.randint(30, 1825)
    created_date = datetime.now() - timedelta(days=days_old)
    
    # Normal follower patterns
    followers = random.randint(50, 2000)
    following = random.randint(100, 1500)
    
    # Realistic posting
    posts = random.randint(20, 500)
    posts_per_day = posts / days_old
    
    return {
        'account_id': f'user_{id_num}',
        'account_type': 'Normal User',
        'created_date': created_date,
        'followers': followers,
        'following': following,
        'posts': posts,
        'posts_per_day': round(posts_per_day, 2),
        'bio_length': random.randint(50, 200),
        'has_profile_pic': True,
        'verified': random.choice([True, False]),
        'avg_likes_per_post': random.randint(10, 100),
        'messages_sent_per_day': random.randint(0, 10),
        'repetitive_content': random.randint(0, 20),  # % of posts that are similar
        'suspicious_links': 0,
        'network_flags': 0
    }


def generate_business_account(id_num):
    """Generate a legitimate business account (often flagged incorrectly)"""
    
    # Usually newer accounts
    days_old = random.randint(30, 365)
    created_date = datetime.now() - timedelta(days=days_old)
    
    # High follower count but low following (business pattern)
    followers = random.randint(500, 10000)
    following = random.randint(50, 300)
    
    # Regular posting (marketing)
    posts = random.randint(100, 1000)
    posts_per_day = posts / days_old
    
    return {
        'account_id': f'biz_{id_num}',
        'account_type': 'Business',
        'created_date': created_date,
        'followers': followers,
        'following': following,
        'posts': posts,
        'posts_per_day': round(posts_per_day, 2),
        'bio_length': random.randint(100, 300),
        'has_profile_pic': True,
        'verified': random.choice([True, False]),
        'avg_likes_per_post': random.randint(50, 500),
        'messages_sent_per_day': random.randint(5, 20),  # Customer service
        'repetitive_content': random.randint(30, 50),  # Marketing messages
        'suspicious_links': random.randint(0, 10),  # Product links
        'network_flags': 0
    }


def generate_bot_account(id_num):
    """Generate a bot/spam account"""
    
    # Very new accounts
    days_old = random.randint(1, 60)
    created_date = datetime.now() - timedelta(days=days_old)
    
    # Bot patterns: high following, low followers
    followers = random.randint(0, 100)
    following = random.randint(1000, 5000)
    
    # Excessive posting
    posts = random.randint(100, 2000)
    posts_per_day = posts / days_old
    
    return {
        'account_id': f'bot_{id_num}',
        'account_type': 'Bot',
        'created_date': created_date,
        'followers': followers,
        'following': following,
        'posts': posts,
        'posts_per_day': round(posts_per_day, 2),
        'bio_length': random.randint(0, 50),  # Minimal bio
        'has_profile_pic': random.choice([True, False]),
        'verified': False,
        'avg_likes_per_post': random.randint(0, 5),  # Low engagement
        'messages_sent_per_day': random.randint(20, 100),  # Spam messages
        'repetitive_content': random.randint(70, 95),  # Very repetitive
        'suspicious_links': random.randint(10, 50),
        'network_flags': random.randint(1, 5)  # Connected to other bots
    }


def generate_scammer_account(id_num):
    """Generate a scam/impersonation account"""
    
    # New accounts
    days_old = random.randint(1, 90)
    created_date = datetime.now() - timedelta(days=days_old)
    
    # Trying to appear legitimate
    followers = random.randint(100, 1000)
    following = random.randint(500, 2000)
    
    posts = random.randint(10, 200)
    posts_per_day = posts / days_old
    
    return {
        'account_id': f'scam_{id_num}',
        'account_type': 'Scammer',
        'created_date': created_date,
        'followers': followers,
        'following': following,
        'posts': posts,
        'posts_per_day': round(posts_per_day, 2),
        'bio_length': random.randint(50, 150),
        'has_profile_pic': True,  # Often stolen pics
        'verified': False,
        'avg_likes_per_post': random.randint(5, 30),
        'messages_sent_per_day': random.randint(30, 100),  # Mass messaging
        'repetitive_content': random.randint(60, 85),
        'suspicious_links': random.randint(20, 80),  # Phishing links
        'network_flags': random.randint(2, 8)  # Part of scam networks
    }


def get_sample_accounts_for_demo():
    """
    Generate specific interesting accounts for demo purposes
    Returns accounts that showcase different risk levels
    """
    
    demo_accounts = [
        # LOW RISK: New legitimate business
        {
            'account_id': 'demo_coffee_shop',
            'account_type': 'Business',
            'created_date': datetime.now() - timedelta(days=45),
            'followers': 250,
            'following': 150,
            'posts': 60,
            'posts_per_day': 1.33,
            'bio_length': 180,
            'has_profile_pic': True,
            'verified': False,
            'avg_likes_per_post': 45,
            'messages_sent_per_day': 8,
            'repetitive_content': 35,
            'suspicious_links': 5,
            'network_flags': 0
        },
        
        # MODERATE RISK: Unusual but potentially legitimate
        {
            'account_id': 'demo_influencer',
            'account_type': 'Normal User',
            'created_date': datetime.now() - timedelta(days=90),
            'followers': 5000,
            'following': 200,
            'posts': 300,
            'posts_per_day': 3.33,
            'bio_length': 150,
            'has_profile_pic': True,
            'verified': False,
            'avg_likes_per_post': 200,
            'messages_sent_per_day': 15,
            'repetitive_content': 40,
            'suspicious_links': 15,
            'network_flags': 1
        },
        
        # HIGH RISK: Clear scam pattern
        {
            'account_id': 'demo_scammer',
            'account_type': 'Scammer',
            'created_date': datetime.now() - timedelta(days=10),
            'followers': 50,
            'following': 3000,
            'posts': 150,
            'posts_per_day': 15.0,
            'bio_length': 80,
            'has_profile_pic': True,
            'verified': False,
            'avg_likes_per_post': 2,
            'messages_sent_per_day': 80,
            'repetitive_content': 85,
            'suspicious_links': 60,
            'network_flags': 5
        }
    ]
    
    return pd.DataFrame(demo_accounts)


# Test the generator
if __name__ == "__main__":
    print("Generating mock accounts...")
    df = generate_mock_accounts(20)
    print(df.head())
    print(f"\nGenerated {len(df)} accounts")
    print(f"Account types: {df['account_type'].value_counts()}")
