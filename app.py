"""
STREAMLIT APP - Main User Interface
This is what users see and interact with
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_generator import generate_mock_accounts, get_sample_accounts_for_demo
from risk_engine import calculate_risk_score, analyze_batch_accounts, get_risk_distribution

# Page configuration
st.set_page_config(
    page_title="Social Account Risk Assessment",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .risk-high {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #f44336;
    }
    .risk-moderate {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ff9800;
    }
    .risk-low {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #4caf50;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<p class="main-header">🛡️ Social Account Risk Assessment Platform</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; color: #666; margin-bottom: 2rem;'>
    <b>Ethical AI for Online Safety</b> | Probabilistic risk assessment, not definitive judgment
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Analysis Options")
        
        analysis_mode = st.radio(
            "Select Mode:",
            ["🎯 Demo Accounts", "📊 Generate Random Batch", "🔍 Single Account Analysis"]
        )
        
        st.markdown("---")
        st.markdown("""
        ### About This Tool
        This system provides **risk levels**, not labels.
        
        **Risk Categories:**
        - 🟢 **Low Risk**: Likely legitimate
        - 🟡 **Moderate Risk**: Needs review
        - 🔴 **High Risk**: Suspicious patterns
        
        **Note:** Results assist human decision-making, they don't replace it.
        """)
    
    # Main content based on mode
    if analysis_mode == "🎯 Demo Accounts":
        show_demo_analysis()
    elif analysis_mode == "📊 Generate Random Batch":
        show_batch_analysis()
    else:
        show_single_account_analysis()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #999; font-size: 0.9rem;'>
    ⚖️ This tool provides probabilistic risk assessment, not definitive judgment.<br>
    Results are intended to assist moderation, not replace human decision-making.
    </div>
    """, unsafe_allow_html=True)


def show_demo_analysis():
    """Show analysis of pre-made demo accounts"""
    
    st.header("🎯 Demo Account Analysis")
    st.write("Analyzing 3 sample accounts showcasing different risk levels")
    
    # Get demo accounts
    demo_df = get_sample_accounts_for_demo()
    results = analyze_batch_accounts(demo_df)
    
    # Show each account in detail
    for idx, account in results.iterrows():
        display_account_card(account)
        st.markdown("---")
    
    # Show summary
    show_risk_summary(results)


def show_batch_analysis():
    """Analyze a batch of randomly generated accounts"""
    
    st.header("📊 Batch Analysis")
    
    num_accounts = st.slider("Number of accounts to generate:", 10, 100, 50)
    
    if st.button("🔄 Generate and Analyze", type="primary"):
        with st.spinner("Generating accounts and calculating risk scores..."):
            # Generate accounts
            accounts_df = generate_mock_accounts(num_accounts)
            
            # Analyze them
            results = analyze_batch_accounts(accounts_df)
            
            # Store in session state
            st.session_state['results'] = results
    
    # Display results if available
    if 'results' in st.session_state:
        results = st.session_state['results']
        
        # Summary statistics
        show_risk_summary(results)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Risk Distribution")
            fig = px.pie(
                results,
                names='risk_level',
                title="Accounts by Risk Level",
                color='risk_level',
                color_discrete_map={
                    'LOW RISK': '#4caf50',
                    'MODERATE RISK': '#ff9800',
                    'HIGH RISK': '#f44336'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Risk Score Distribution")
            fig = px.histogram(
                results,
                x='risk_score',
                nbins=20,
                title="Distribution of Risk Scores",
                labels={'risk_score': 'Risk Score'},
                color_discrete_sequence=['#1f77b4']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.subheader("📋 Detailed Results")
        
        # Filter options
        risk_filter = st.multiselect(
            "Filter by risk level:",
            options=['LOW RISK', 'MODERATE RISK', 'HIGH RISK'],
            default=['LOW RISK', 'MODERATE RISK', 'HIGH RISK']
        )
        
        filtered_results = results[results['risk_level'].isin(risk_filter)]
        
        # Display table
        display_df = filtered_results[['account_id', 'account_type', 'risk_score', 'risk_level', 'followers', 'following', 'posts_per_day']]
        st.dataframe(display_df, use_container_width=True)
        
        # Allow detailed view
        st.subheader("🔍 View Detailed Analysis")
        selected_account = st.selectbox(
            "Select account to view details:",
            options=filtered_results['account_id'].tolist()
        )
        
        if selected_account:
            account_data = filtered_results[filtered_results['account_id'] == selected_account].iloc[0]
            display_account_card(account_data)


def show_single_account_analysis():
    """Allow manual input of account data"""
    
    st.header("🔍 Single Account Analysis")
    st.write("Enter account details manually to assess risk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        account_id = st.text_input("Account ID", "custom_account_001")
        followers = st.number_input("Followers", min_value=0, value=500)
        following = st.number_input("Following", min_value=0, value=300)
        posts = st.number_input("Total Posts", min_value=0, value=100)
        account_age = st.number_input("Account Age (days)", min_value=1, value=180)
    
    with col2:
        posts_per_day = posts / account_age if account_age > 0 else 0
        st.metric("Posts per Day", f"{posts_per_day:.2f}")
        
        messages_per_day = st.number_input("Messages Sent per Day", min_value=0, value=5)
        repetitive_content = st.slider("Repetitive Content (%)", 0, 100, 20)
        suspicious_links = st.slider("Suspicious Links (%)", 0, 100, 5)
        network_flags = st.number_input("Connected Flagged Accounts", min_value=0, value=0)
    
    if st.button("🔍 Analyze Account", type="primary"):
        from datetime import datetime, timedelta
        
        # Create account dictionary
        account = {
            'account_id': account_id,
            'account_type': 'Custom',
            'created_date': datetime.now() - timedelta(days=account_age),
            'followers': followers,
            'following': following,
            'posts': posts,
            'posts_per_day': posts_per_day,
            'bio_length': 100,
            'has_profile_pic': True,
            'verified': False,
            'avg_likes_per_post': 50,
            'messages_sent_per_day': messages_per_day,
            'repetitive_content': repetitive_content,
            'suspicious_links': suspicious_links,
            'network_flags': network_flags
        }
        
        # Calculate risk
        result = calculate_risk_score(account)
        
        # Display result
        display_account_card({**account, **result})


def display_account_card(account):
    """Display detailed account analysis in a card format"""
    
    # Determine card style based on risk
    if account['risk_level'] == 'HIGH RISK':
        card_class = 'risk-high'
        emoji = '🔴'
    elif account['risk_level'] == 'MODERATE RISK':
        card_class = 'risk-moderate'
        emoji = '🟡'
    else:
        card_class = 'risk-low'
        emoji = '🟢'
    
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.subheader(f"{emoji} {account['account_id']}")
        st.caption(f"Type: {account.get('account_type', 'Unknown')}")
    with col2:
        st.metric("Risk Score", f"{account['risk_score']}/100")
    with col3:
        st.metric("Risk Level", account['risk_level'])
    
    # Recommendation
    st.info(f"**Recommendation:** {account['recommendation']}")
    
    # Account metrics
    st.markdown("### 📊 Account Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Followers", f"{account['followers']:,}")
    with col2:
        st.metric("Following", f"{account['following']:,}")
    with col3:
        st.metric("Posts/Day", f"{account['posts_per_day']:.2f}")
    with col4:
        account_age = (pd.Timestamp.now() - pd.Timestamp(account['created_date'])).days
        st.metric("Age (days)", account_age)
    
    # Risk factors
    st.markdown("### 🔍 Risk Factors & Explanations")
    for explanation in account['explanations']:
        st.markdown(f"- {explanation}")
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_risk_summary(results):
    """Display summary statistics"""
    
    st.subheader("📈 Summary Statistics")
    
    dist = get_risk_distribution(results)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Accounts", dist['total'])
    with col2:
        st.metric("🟢 Low Risk", dist['low_risk'])
    with col3:
        st.metric("🟡 Moderate Risk", dist['moderate_risk'])
    with col4:
        st.metric("🔴 High Risk", dist['high_risk'])
    
    st.metric("Average Risk Score", f"{dist['avg_score']:.1f}/100")


if __name__ == "__main__":
    main()