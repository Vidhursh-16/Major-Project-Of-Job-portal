import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time

# Page config
st.set_page_config(page_title="Job Portal Analytics", page_icon="📊", layout="wide")

# Title
st.title("🚀 Live Job Application Analytics")
st.markdown("### Real-time crowd rush visualization for top companies")

# Generate fake data for companies
companies = ['Figma', 'Twitter', 'Facebook', 'LinkedIn', 'YouTube']
roles = {
    'Figma': 'UI/UX Designer',
    'Twitter': 'ReactJS Developer',
    'Facebook': 'Frontend Engineer',
    'LinkedIn': 'Full Stack Developer',
    'YouTube': 'Video Content Strategist'
}

# Generate realistic fake data
np.random.seed(42)
base_applicants = {
    'Figma': 450,
    'Twitter': 680,
    'Facebook': 920,
    'LinkedIn': 1150,
    'YouTube': 580
}

# Create columns for metrics
col1, col2, col3, col4, col5 = st.columns(5)
columns = [col1, col2, col3, col4, col5]

for idx, company in enumerate(companies):
    with columns[idx]:
        applicants = base_applicants[company] + np.random.randint(-50, 100)
        st.metric(
            label=f"**{company}**",
            value=f"{applicants} applicants",
            delta=f"+{np.random.randint(10, 50)} today"
        )
        st.caption(roles[company])

st.markdown("---")

# Tab layout
tab1, tab2, tab3 = st.tabs(["📈 Application Trend", "🔥 Live Rush", "📊 Role Breakdown"])

with tab1:
    st.subheader("Application Trend - Last 7 Days")
    
    # Generate time series data
    dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
    data = []
    
    for company in companies:
        base = base_applicants[company]
        for date in dates:
            applications = base + np.random.randint(-100, 200)
            data.append({
                'Date': date,
                'Company': company,
                'Applications': applications
            })
    
    df = pd.DataFrame(data)
    
    # Line chart
    fig = px.line(df, x='Date', y='Applications', color='Company',
                  title='Daily Application Volume',
                  markers=True,
                  color_discrete_sequence=px.colors.qualitative.Bold)
    
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("🔥 Live Application Rush")
    st.markdown("*Simulated real-time applicant flow*")
    
    # Create animated bar chart
    chart_placeholder = st.empty()
    
    # Simulate live updates
    for i in range(20):
        current_data = []
        for company in companies:
            rush_count = base_applicants[company] + np.random.randint(-200, 300)
            current_data.append({
                'Company': company,
                'Live Applicants': max(0, rush_count),
                'Role': roles[company]
            })
        
        df_live = pd.DataFrame(current_data)
        df_live = df_live.sort_values('Live Applicants', ascending=True)
        
        # Create horizontal bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df_live['Company'],
            x=df_live['Live Applicants'],
            orientation='h',
            text=df_live['Live Applicants'],
            textposition='outside',
            marker=dict(
                color=df_live['Live Applicants'],
                colorscale='Viridis',
                showscale=False
            ),
            hovertemplate='<b>%{y}</b><br>Applicants: %{x}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Current Application Volume (Updating Live)",
            xaxis_title="Number of Applicants",
            yaxis_title="",
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.5)  # Update every 0.5 seconds

with tab3:
    st.subheader("📊 Job Role Distribution")
    
    # Pie chart for role popularity
    role_data = []
    for company in companies:
        role_data.append({
            'Company': company,
            'Role': roles[company],
            'Total Applications': base_applicants[company] + np.random.randint(100, 500)
        })
    
    df_roles = pd.DataFrame(role_data)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        fig_pie = px.pie(df_roles, values='Total Applications', names='Company',
                         title='Application Share by Company',
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_right:
        fig_bar = px.bar(df_roles, x='Company', y='Total Applications',
                         color='Company',
                         title='Total Applications by Company',
                         text='Total Applications',
                         color_discrete_sequence=px.colors.qualitative.Set2)
        fig_bar.update_traces(textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

# Footer stats
st.markdown("---")
st.markdown("### 📌 Platform Statistics")
col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    st.metric("Total Jobs Posted", "1,247", "+42 this week")
with col_b:
    st.metric("Active Applicants", "12,458", "+1,205 today")
with col_c:
    st.metric("Companies Listed", "87", "+5 new")
with col_d:
    st.metric("Avg. Response Time", "2.3 days", "-0.4 days")

st.success("✅ Analytics Dashboard - All systems operational")
