import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add project root to path
repo_root = Path(__file__).parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# Set page config
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .growth-positive {
        color: #28a745;
        font-weight: bold;
    }
    .growth-negative {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load all necessary data for the dashboard"""
    try:
        # Historical data
        df = pd.read_csv(repo_root / 'data' / 'processed' / 'ethiopia_fi_unified_data_enriched.csv')
        observations = df[df['record_type'] == 'observation'].copy()
        observations['observation_date'] = pd.to_datetime(observations['observation_date'], errors='coerce')

        # Event impact matrix
        matrix = pd.read_csv(repo_root / 'outputs' / 'event_indicator_matrix.csv', index_col=0)

        # Forecasts
        forecasts = pd.read_csv(repo_root / 'outputs' / 'financial_inclusion_forecasts_2025_2027.csv')

        return observations, matrix, forecasts
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

# Load data
observations, matrix, forecasts = load_data()

if observations is None:
    st.error("Failed to load data. Please ensure all previous tasks are completed.")
    st.stop()

# Sidebar navigation
st.sidebar.title("📊 Ethiopia Financial Inclusion Dashboard")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Overview", "📈 Trends", "🔮 Forecasts", "🎯 Inclusion Projections"],
    help="Select a page to explore"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Data Sources")
st.sidebar.markdown("- Historical: Findex Surveys")
st.sidebar.markdown("- Forecasts: 2025-2027 Projections")
st.sidebar.markdown("- Events: Policy & Product Launches")

# Main content
if page == "🏠 Overview":
    st.title("🏠 Financial Inclusion Overview")
    st.markdown("Key metrics and trends for Ethiopia's digital financial transformation")

    # Current metrics
    col1, col2, col3, col4 = st.columns(4)

    # Get latest values
    latest_access = observations[observations['indicator_code'] == 'ACC_OWNERSHIP']['value_numeric'].max()
    latest_usage = observations[observations['indicator_code'] == 'ACC_MM_ACCOUNT']['value_numeric'].max()

    # Calculate growth rates
    access_data = observations[observations['indicator_code'] == 'ACC_OWNERSHIP'].sort_values('observation_date')
    if len(access_data) >= 2:
        access_growth = (access_data['value_numeric'].iloc[-1] - access_data['value_numeric'].iloc[-2]) / access_data['value_numeric'].iloc[-2] * 100
    else:
        access_growth = 0

    usage_data = observations[observations['indicator_code'] == 'ACC_MM_ACCOUNT'].sort_values('observation_date')
    if len(usage_data) >= 2:
        usage_growth = (usage_data['value_numeric'].iloc[-1] - usage_data['value_numeric'].iloc[-2]) / usage_data['value_numeric'].iloc[-2] * 100
    else:
        usage_growth = 0

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Account Ownership", f"{latest_access:.1f}%", f"{access_growth:+.1f}pp")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Mobile Money Accounts", f"{latest_usage:.1f}%", f"{usage_growth:+.1f}pp")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        # P2P vs ATM ratio (simplified)
        p2p_data = observations[observations['indicator_code'].str.contains('P2P', na=False)]
        atm_data = observations[observations['indicator_code'].str.contains('ATM', na=False)]
        if not p2p_data.empty and not atm_data.empty:
            p2p_latest = p2p_data['value_numeric'].max()
            atm_latest = atm_data['value_numeric'].max()
            ratio = p2p_latest / atm_latest if atm_latest > 0 else 0
        else:
            ratio = 0
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("P2P/ATM Ratio", f"{ratio:.2f}", help="Person-to-person transfers vs ATM withdrawals")
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        # Digital payments adoption
        digital_data = observations[observations['indicator_code'] == 'USG_DIGITAL_PAYMENT']
        if not digital_data.empty:
            digital_latest = digital_data['value_numeric'].max()
        else:
            digital_latest = 0
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Digital Payments", f"{digital_latest:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    # Growth highlights
    st.markdown("---")
    st.subheader("📈 Growth Highlights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Account Ownership Growth")
        fig = px.line(access_data, x='observation_date', y='value_numeric',
                     title='Account Ownership Trend', markers=True)
        fig.update_layout(xaxis_title='Year', yaxis_title='Ownership Rate (%)')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Mobile Money Growth")
        fig = px.line(usage_data, x='observation_date', y='value_numeric',
                     title='Mobile Money Accounts Trend', markers=True)
        fig.update_layout(xaxis_title='Year', yaxis_title='Account Rate (%)')
        st.plotly_chart(fig, use_container_width=True)

    # Key insights
    st.markdown("---")
    st.subheader("💡 Key Insights")
    st.markdown("""
    - **Rapid Digital Adoption**: Mobile money accounts grew from 4.7% (2021) to 9.5% (2024)
    - **Account Ownership Stagnation**: Despite mobile growth, overall account ownership only increased from 46% to 49%
    - **P2P Dominance**: Digital person-to-person transfers now exceed ATM cash withdrawals
    - **Infrastructure Impact**: 4G coverage and mobile penetration are key enablers
    """)

elif page == "📈 Trends":
    st.title("📈 Financial Inclusion Trends")
    st.markdown("Interactive exploration of historical trends and patterns")

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        indicators = observations['indicator_code'].unique()
        selected_indicators = st.multiselect(
            "Select Indicators",
            options=indicators,
            default=['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'USG_DIGITAL_PAYMENT'],
            help="Choose which indicators to display"
        )

    with col2:
        date_range = st.date_input(
            "Date Range",
            value=(observations['observation_date'].min(), observations['observation_date'].max()),
            help="Filter data by date range"
        )

    with col3:
        sources = observations['source_name'].unique()
        selected_sources = st.multiselect(
            "Data Sources",
            options=sources,
            default=sources[:2] if len(sources) > 2 else sources,
            help="Filter by data source"
        )

    # Filter data
    filtered_data = observations[
        (observations['indicator_code'].isin(selected_indicators)) &
        (observations['observation_date'] >= pd.to_datetime(date_range[0])) &
        (observations['observation_date'] <= pd.to_datetime(date_range[1])) &
        (observations['source_name'].isin(selected_sources))
    ]

    # Interactive time series
    st.subheader("📊 Interactive Time Series")
    if not filtered_data.empty:
        fig = px.line(filtered_data, x='observation_date', y='value_numeric',
                     color='indicator_code', line_group='source_name',
                     title='Financial Inclusion Indicators Over Time',
                     markers=True)
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Value (%)',
            legend_title='Indicator'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for selected filters")

    # Channel comparison
    st.markdown("---")
    st.subheader("🏦 Channel Comparison")

    # Group by indicator and source
    channel_data = filtered_data.groupby(['indicator_code', 'source_name']).agg({
        'value_numeric': 'mean'
    }).reset_index()

    if not channel_data.empty:
        fig = px.bar(channel_data, x='indicator_code', y='value_numeric',
                    color='source_name', barmode='group',
                    title='Channel Performance Comparison')
        fig.update_layout(xaxis_title='Indicator', yaxis_title='Average Value (%)')
        st.plotly_chart(fig, use_container_width=True)

    # Data download
    st.markdown("---")
    st.subheader("📥 Download Data")
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_financial_inclusion_data.csv',
        mime='text/csv',
        help="Download the filtered dataset for further analysis"
    )

elif page == "🔮 Forecasts":
    st.title("🔮 Financial Inclusion Forecasts")
    st.markdown("Explore future projections for Access and Usage indicators")

    if forecasts is None:
        st.error("Forecast data not available. Please ensure Task 4 is completed.")
    else:
        # Model selection
        model_type = st.selectbox(
            "Select Forecast Model",
            ["Event-Augmented", "Trend Only"],
            help="Choose between models with or without event impacts"
        )

        # Forecast visualization
        st.subheader("📈 Forecast Projections (2025-2027)")

        # Create forecast plot
        fig = go.Figure()

        # Base forecast
        fig.add_trace(go.Scatter(
            x=forecasts['Year'],
            y=forecasts['Access_Base'],
            mode='lines+markers',
            name='Access - Base',
            line=dict(color='blue', width=3)
        ))

        fig.add_trace(go.Scatter(
            x=forecasts['Year'],
            y=forecasts['Usage_Base'],
            mode='lines+markers',
            name='Usage - Base',
            line=dict(color='green', width=3)
        ))

        # Uncertainty bands
        fig.add_trace(go.Scatter(
            x=forecasts['Year'].tolist() + forecasts['Year'].tolist()[::-1],
            y=forecasts['Access_Optimistic'].tolist() + forecasts['Access_Pessimistic'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(0,0,255,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Access Uncertainty'
        ))

        fig.add_trace(go.Scatter(
            x=forecasts['Year'].tolist() + forecasts['Year'].tolist()[::-1],
            y=forecasts['Usage_Optimistic'].tolist() + forecasts['Usage_Pessimistic'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(0,255,0,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Usage Uncertainty'
        ))

        fig.update_layout(
            title='Financial Inclusion Forecasts with Uncertainty',
            xaxis_title='Year',
            yaxis_title='Rate (%)',
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # Key milestones
        st.markdown("---")
        st.subheader("🎯 Key Milestones")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Access Milestones")
            for _, row in forecasts.iterrows():
                st.markdown(f"**{int(row['Year'])}**: {row['Access_Base']:.1f}% (Range: {row['Access_Pessimistic']:.1f}% - {row['Access_Optimistic']:.1f}%)")

        with col2:
            st.markdown("### Usage Milestones")
            for _, row in forecasts.iterrows():
                st.markdown(f"**{int(row['Year'])}**: {row['Usage_Base']:.1f}% (Range: {row['Usage_Pessimistic']:.1f}% - {row['Usage_Optimistic']:.1f}%)")

        # Forecast table
        st.markdown("---")
        st.subheader("📊 Forecast Data Table")
        st.dataframe(forecasts.style.format({
            'Access_Base': '{:.1f}%',
            'Access_Optimistic': '{:.1f}%',
            'Access_Pessimistic': '{:.1f}%',
            'Usage_Base': '{:.1f}%',
            'Usage_Optimistic': '{:.1f}%',
            'Usage_Pessimistic': '{:.1f}%'
        }))

        # Download forecasts
        csv = forecasts.to_csv(index=False)
        st.download_button(
            label="Download Forecast Data as CSV",
            data=csv,
            file_name='financial_inclusion_forecasts.csv',
            mime='text/csv',
            help="Download the forecast data for further analysis"
        )

elif page == "🎯 Inclusion Projections":
    st.title("🎯 Financial Inclusion Projections")
    st.markdown("Progress toward targets and scenario planning")

    if forecasts is None:
        st.error("Forecast data not available. Please ensure Task 4 is completed.")
    else:
        # Scenario selector
        scenario = st.selectbox(
            "Select Scenario",
            ["Base Case", "Optimistic", "Pessimistic"],
            help="Choose forecast scenario to display"
        )

        # Map scenario to columns
        if scenario == "Base Case":
            access_col = "Access_Base"
            usage_col = "Usage_Base"
        elif scenario == "Optimistic":
            access_col = "Access_Optimistic"
            usage_col = "Usage_Optimistic"
        else:  # Pessimistic
            access_col = "Access_Pessimistic"
            usage_col = "Usage_Pessimistic"

        # Progress toward 60% target
        st.subheader("🎯 Progress Toward 60% Financial Inclusion Target")

        # Create progress visualization
        target = 60
        current_access = observations[observations['indicator_code'] == 'ACC_OWNERSHIP']['value_numeric'].max()
        current_usage = observations[observations['indicator_code'] == 'ACC_MM_ACCOUNT']['value_numeric'].max()

        # Project when target will be reached
        access_years = forecasts[forecasts[access_col] >= target]['Year']
        usage_years = forecasts[forecasts[usage_col] >= target]['Year']

        access_target_year = access_years.min() if not access_years.empty else "Beyond 2027"
        usage_target_year = usage_years.min() if not usage_years.empty else "Beyond 2027"

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Account Ownership Progress")
            fig = go.Figure()

            # Current progress
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=current_access,
                title={'text': f"Current: {current_access:.1f}%"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': 'blue'},
                    'steps': [
                        {'range': [0, target], 'color': 'lightgray'},
                        {'range': [target, 100], 'color': 'lightblue'}
                    ],
                    'threshold': {
                        'line': {'color': 'red', 'width': 4},
                        'thickness': 0.75,
                        'value': target
                    }
                }
            ))

            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"**Target Reach**: {access_target_year}")

        with col2:
            st.markdown("### Digital Usage Progress")
            fig = go.Figure()

            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=current_usage,
                title={'text': f"Current: {current_usage:.1f}%"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': 'green'},
                    'steps': [
                        {'range': [0, target], 'color': 'lightgray'},
                        {'range': [target, 100], 'color': 'lightgreen'}
                    ],
                    'threshold': {
                        'line': {'color': 'red', 'width': 4},
                        'thickness': 0.75,
                        'value': target
                    }
                }
            ))

            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"**Target Reach**: {usage_target_year}")

        # Scenario comparison
        st.markdown("---")
        st.subheader("📊 Scenario Comparison")

        fig = go.Figure()

        # Access scenarios
        fig.add_trace(go.Scatter(
            x=forecasts['Year'],
            y=forecasts['Access_Base'],
            mode='lines+markers',
            name='Access - Base',
            line=dict(color='blue', dash='solid')
        ))

        fig.add_trace(go.Scatter(
            x=forecasts['Year'],
            y=forecasts['Access_Optimistic'],
            mode='lines',
            name='Access - Optimistic',
            line=dict(color='blue', dash='dot')
        ))

        fig.add_trace(go.Scatter(
            x=forecasts['Year'],
            y=forecasts['Access_Pessimistic'],
            mode='lines',
            name='Access - Pessimistic',
            line=dict(color='blue', dash='dash')
        ))

        # Usage scenarios
        fig.add_trace(go.Scatter(
            x=forecasts['Year'],
            y=forecasts['Usage_Base'],
            mode='lines+markers',
            name='Usage - Base',
            line=dict(color='green', dash='solid')
        ))

        fig.add_trace(go.Scatter(
            x=forecasts['Year'],
            y=forecasts['Usage_Optimistic'],
            mode='lines',
            name='Usage - Optimistic',
            line=dict(color='green', dash='dot')
        ))

        fig.add_trace(go.Scatter(
            x=forecasts['Year'],
            y=forecasts['Usage_Pessimistic'],
            mode='lines',
            name='Usage - Pessimistic',
            line=dict(color='green', dash='dash')
        ))

        # Add target line
        fig.add_hline(y=target, line_dash="dash", line_color="red",
                     annotation_text="60% Target", annotation_position="bottom right")

        fig.update_layout(
            title='Scenario Projections vs 60% Target',
            xaxis_title='Year',
            yaxis_title='Inclusion Rate (%)',
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # Consortium questions
        st.markdown("---")
        st.subheader("❓ Consortium Key Questions")

        st.markdown("**What drives financial inclusion in Ethiopia?**")
        st.markdown("""
        - **Mobile Money Innovation**: Telebirr and M-Pesa have driven rapid adoption
        - **Infrastructure Development**: 4G coverage and agent networks enable access
        - **Policy Support**: NFIS-II and regulatory frameworks provide enabling environment
        - **Economic Factors**: Urbanization and digital literacy trends
        """)

        st.markdown("**How do events affect inclusion outcomes?**")
        st.markdown("""
        - **Product Launches**: Telebirr (+5pp), M-Pesa (+2pp) drive account growth
        - **Policy Changes**: NFIS-II provides +5pp boost to ownership
        - **Infrastructure**: EthSwitch integration could add +10pp to digital payments
        - **Market Dynamics**: Competition accelerates innovation and adoption
        """)

        st.markdown("**What will inclusion look like in 2025-2027?**")
        st.markdown(f"""
        - **Base Case**: Access reaches {forecasts[access_col].iloc[-1]:.1f}%, Usage reaches {forecasts[usage_col].iloc[-1]:.1f}%
        - **60% Target**: Access target reached by {access_target_year}, Usage by {usage_target_year}
        - **Key Risks**: Economic slowdowns, regulatory changes, technology adoption barriers
        - **Opportunities**: Continued mobile innovation, infrastructure expansion, policy reforms
        """)

# Footer
st.markdown("---")
st.markdown("### 📊 Dashboard Information")
st.markdown("Built with Streamlit | Data from Global Findex & Ethiopian Financial Sector")
st.markdown("**Last Updated**: February 2026 | **Source**: 10 Academy AI Mastery Challenge")

if __name__ == "__main__":
    st.write("Run with: streamlit run src/dashboard/app.py")