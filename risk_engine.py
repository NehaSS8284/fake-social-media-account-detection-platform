"""
RISK ENGINE - The brain of the system
Calculates risk scores and provides explanations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_risk_score(account):
    """
    Calculate comprehensive risk score for an account
    
    Returns: dictionary with score, risk_level, and explanations
    """
    
    # Initialize scoring
    risk_score = 0
    max_score = 100
    explanations = []
    
    # FACTOR 1: Account Age (max 15 points)
    account_age_days = (datetime.now() - account['created_date']).days
    if account_age_days < 30:
        risk_score += 15
        explanations.append("🚩 Very new account (less than 1 month old)")
    elif account_age_days < 90:
        risk_score += 8
        explanations.append("⚠️ Relatively new account (less than 3 months)")
    elif account_age_days < 180:
        risk_score += 3
        explanations.append("ℹ️ Account is less than 6 months old")
    
    # FACTOR 2: Follower/Following Ratio (max 20 points)
    if account['following'] > 0:
        ff_ratio = account['followers'] / account['following']
        
        if account['following'] > 2000 and account['followers'] < 100:
            risk_score += 20
            explanations.append("🚩 Suspicious follow pattern: Following many, very few followers (bot-like)")
        elif ff_ratio < 0.1:
            risk_score += 12
            explanations.append("⚠️ Low follower-to-following ratio (potential spam behavior)")
        elif ff_ratio > 10 and account['followers'] > 5000:
            risk_score += 0
            explanations.append("✅ High influence: Many followers, selective following (typical influencer/business)")
    
    # FACTOR 3: Posting Frequency (max 20 points)
    if account['posts_per_day'] > 10:
        risk_score += 20
        explanations.append(f"🚩 Extremely high posting frequency ({account['posts_per_day']:.1f} posts/day - likely automated)")
    elif account['posts_per_day'] > 5:
        risk_score += 12
        explanations.append(f"⚠️ High posting frequency ({account['posts_per_day']:.1f} posts/day)")
    elif account['posts_per_day'] > 3:
        risk_score += 5
        explanations.append(f"ℹ️ Active posting ({account['posts_per_day']:.1f} posts/day - could be legitimate business)")
    
    # FACTOR 4: Content Repetition (max 15 points)
    if account['repetitive_content'] > 70:
        risk_score += 15
        explanations.append(f"🚩 Very repetitive content ({account['repetitive_content']}% similar posts)")
    elif account['repetitive_content'] > 50:
        risk_score += 8
        explanations.append(f"⚠️ Moderately repetitive content ({account['repetitive_content']}% - could be marketing)")
    elif account['repetitive_content'] > 30:
        risk_score += 3
        explanations.append(f"ℹ️ Some content repetition ({account['repetitive_content']}% - possibly promotional)")
    
    # FACTOR 5: Messaging Behavior (max 15 points)
    if account['messages_sent_per_day'] > 50:
        risk_score += 15
        explanations.append(f"🚩 Mass messaging activity ({account['messages_sent_per_day']} messages/day)")
    elif account['messages_sent_per_day'] > 20:
        risk_score += 8
        explanations.append(f"⚠️ High messaging volume ({account['messages_sent_per_day']} messages/day)")
    
    # FACTOR 6: Suspicious Links (max 10 points)
    if account['suspicious_links'] > 40:
        risk_score += 10
        explanations.append(f"🚩 Many suspicious links ({account['suspicious_links']}% of posts)")
    elif account['suspicious_links'] > 20:
        risk_score += 6
        explanations.append(f"⚠️ Moderate suspicious links ({account['suspicious_links']}% of posts)")
    elif account['suspicious_links'] > 10:
        risk_score += 2
        explanations.append(f"ℹ️ Some external links ({account['suspicious_links']}% - possibly promotional)")
    
    # FACTOR 7: Network Connections (max 5 points)
    if account['network_flags'] > 3:
        risk_score += 5
        explanations.append(f"🚩 Connected to {account['network_flags']} flagged accounts (coordinated behavior)")
    elif account['network_flags'] > 0:
        risk_score += 2
        explanations.append(f"⚠️ Connected to {account['network_flags']} flagged account(s)")
    
    # Normalize score to 0-100
    risk_score = min(risk_score, max_score)
    
    # Determine risk level
    if risk_score >= 70:
        risk_level = "HIGH RISK"
        risk_color = "🔴"
        recommendation = "Strong indicators of malicious activity. Recommend immediate review and possible restriction."
    elif risk_score >= 40:
        risk_level = "MODERATE RISK"
        risk_color = "🟡"
        recommendation = "Unusual patterns detected. May be legitimate but warrants human review."
    else:
        risk_level = "LOW RISK"
        risk_color = "🟢"
        recommendation = "Activity appears normal. Account likely legitimate."
    
    # Add positive signals if low risk
    if risk_score < 40:
        if account.get('verified', False):
            explanations.append("✅ Verified account")
        if account.get('has_profile_pic', False):
            explanations.append("✅ Has profile picture")
        if account.get('bio_length', 0) > 50:
            explanations.append("✅ Complete profile with bio")
        if account_age_days > 365:
            explanations.append("✅ Established account (over 1 year old)")
    
    return {
        'risk_score': risk_score,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'recommendation': recommendation,
        'explanations': explanations,
        'account_id': account['account_id']
    }


def analyze_batch_accounts(df):
    """
    Analyze multiple accounts and return results DataFrame
    """
    results = []
    
    for idx, account in df.iterrows():
        result = calculate_risk_score(account)
        
        # Combine account data with risk assessment
        full_result = {**account.to_dict(), **result}
        results.append(full_result)
    
    return pd.DataFrame(results)


def get_risk_distribution(results_df):
    """
    Get statistics about risk distribution
    """
    distribution = results_df['risk_level'].value_counts().to_dict()
    
    return {
        'high_risk': distribution.get('HIGH RISK', 0),
        'moderate_risk': distribution.get('MODERATE RISK', 0),
        'low_risk': distribution.get('LOW RISK', 0),
        'total': len(results_df),
        'avg_score': results_df['risk_score'].mean()
    }


# Test the engine
if __name__ == "__main__":
    from data_generator import generate_mock_accounts
    
    print("Testing Risk Engine...")
    accounts = generate_mock_accounts(10)
    results = analyze_batch_accounts(accounts)
    
    print("\nRisk Distribution:")
    print(get_risk_distribution(results))
    
    print("\nSample Results:")
    print(results[['account_id', 'risk_score', 'risk_level']].head())