"""
Global Health Analytics Dashboard
Capstone Project - MSIT 5910
Developer: Hazem Alahmad
University of the People
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ============================================
# PAGE CONFIGURATION
# ============================================
st.image("https://www.who.int/images/default-source/maps/logo-who.png", 
         width=150, caption="Data Source: World Health Organization")

st.markdown("""
<style>
    .stPlotlyChart {
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="WHO Global Health Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.who.int/data/gho',
        'Report a bug': None,
        'About': "Capstone Project - MSIT 5910 - Interactive Public Data Dashboard"
    }
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .sidebar-section {
        background-color: #1E40AF;
        color: white;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: 600;
    }
    .footer {
        text-align: center;
        color: #6B7280;
        font-size: 0.9rem;
        margin-top: 2rem;
        padding-top: 1.2rem;
        border-top: 2px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING FUNCTIONS
# ============================================

@st.cache_data
def load_who_data():
    """
    Load WHO data from CSV file - FIXED VERSION
    """
    who_file = "data/raw/who_life_expectancy.csv"
    
    if not os.path.exists(who_file):
        st.sidebar.error("WHO data file not found!")
        return create_fallback_data()
    
    try:
        # Read WHO CSV
        df_who = pd.read_csv(who_file)
        
        # Debug info
        st.sidebar.info(f"📊 WHO File: {len(df_who)} records")
        st.sidebar.info(f"🌍 Countries in file: {df_who['COUNTRY'].nunique()}")
        
        # Simple transformation
        df_who = df_who.rename(columns={
            'COUNTRY': 'Country',
            'YEAR': 'Year',
            'Numeric': 'Value',
            'GHO (DISPLAY)': 'Metric'
        })
        
        # Select only needed columns
        df_who = df_who[['Country', 'Year', 'Metric', 'Value']]
        
        # Add required columns
        df_who['Unit'] = 'years'
        df_who['Data_Quality'] = 'High'
        
        # Add WHO Region mapping
        df_who['WHO_Region'] = df_who['Country'].map({
            'Afghanistan': 'EMRO',
            'Japan': 'WPRO',
            'United States of America': 'AMRO',
            'Germany': 'EURO',
            'Brazil': 'AMRO',
            'India': 'SEARO'
        }).fillna('Global')
        
        # Add Development Level
        df_who['Development_Level'] = df_who['Country'].map({
            'Afghanistan': 'Low',
            'Japan': 'High',
            'United States of America': 'High',
            'Germany': 'High',
            'Brazil': 'Upper-Middle',
            'India': 'Lower-Middle'
        }).fillna('Mixed')
        
        # Add other metrics
        other_metrics = create_other_metrics(df_who['Country'].unique())
        df_combined = pd.concat([df_who, other_metrics], ignore_index=True)
        
        # Calculate indexed values
        df_combined['Value_Indexed'] = df_combined.groupby(['Country', 'Metric'])['Value'].transform(
            lambda x: (x / x.iloc[0] * 100) if len(x) > 0 and x.iloc[0] != 0 else 100
        )
        
        st.session_state.data_source = "WHO Life Expectancy + Synthetic"
        return df_combined
        
    except Exception as e:
        st.sidebar.error(f"Error: {str(e)[:100]}")
        return create_fallback_data()

def create_other_metrics(countries):
    """Create synthetic data for other health metrics - ENHANCED VERSION"""
    np.random.seed(42)
    
    # جميع المؤشرات الأصلية مع قيم واقعية
    metrics_config = {
        'Life Expectancy': {'unit': 'years', 'range': (50, 85), 'trend': 0.15},
        'Under-5 Mortality Rate': {'unit': 'per 1000', 'range': (2, 150), 'trend': -0.8},
        'Maternal Mortality Ratio': {'unit': 'per 100000', 'range': (5, 500), 'trend': -2.5},
        'Vaccination Coverage (DTP3)': {'unit': '%', 'range': (40, 99), 'trend': 0.3},
        'Hospital Beds per 1000': {'unit': 'beds', 'range': (0.5, 15), 'trend': 0.05},
        'Physicians per 10000': {'unit': 'doctors', 'range': (1, 40), 'trend': 0.2},
        'Health Expenditure (% of GDP)': {'unit': '%', 'range': (2, 12), 'trend': 0.1},
        'Adult Obesity Rate': {'unit': '%', 'range': (5, 40), 'trend': 0.1},
        'Smoking Prevalence': {'unit': '%', 'range': (10, 50), 'trend': -0.2},
        'Access to Clean Water': {'unit': '%', 'range': (50, 100), 'trend': 0.25}
    }
    
    # سنوات متعددة لبيانات واقعية
    years = list(range(2000, 2024, 2))  # كل سنتين: 2000, 2002, 2004, ..., 2022
    
    records = []
    
    for country in countries:
        # تحديد مستوى تنمية الدولة
        dev_level = get_development_level(country)
        
        for metric_name, config in metrics_config.items():
            # تخطي Life Expectancy لأن لدينا بيانات WHO الأصلية لها
            if metric_name == 'Life Expectancy':
                continue
                
            # مضاعفات حسب مستوى التنمية
            level_multiplier = {
                'High': 0.9,
                'Upper-Middle': 0.7, 
                'Lower-Middle': 0.5,
                'Low': 0.3
            }.get(dev_level, 0.5)
            
            min_val, max_val = config['range']
            base_value = min_val + (max_val - min_val) * level_multiplier
            
            for year in years:
                # حساب عامل الزمن
                year_progress = year - 2000
                trend_value = config['trend'] * year_progress
                
                # عامل عشوائي واقعي
                random_factor = np.random.normal(0, max_val * 0.02)
                
                # حساب القيمة النهائية
                value = base_value + trend_value + random_factor
                
                # التأكد من حدود واقعية
                value = max(min_val * 0.8, min(max_val * 1.1, value))
                
                # تحديد جودة البيانات
                data_quality = 'High' if dev_level in ['High', 'Upper-Middle'] else 'Medium'
                
                records.append({
                    'Country': country,
                    'Year': year,
                    'Metric': metric_name,
                    'Value': round(value, 2),
                    'Unit': config['unit'],
                    'WHO_Region': get_who_region(country),
                    'Development_Level': dev_level,
                    'Data_Quality': data_quality
                })
    
    return pd.DataFrame(records)
    
def get_development_level(country):
    """تحديد مستوى تنمية الدولة"""
    development_map = {
        'Afghanistan': 'Low',
        'Japan': 'High',
        'United States of America': 'High',
        'Germany': 'High',
        'Brazil': 'Upper-Middle',
        'India': 'Lower-Middle'
    }
    return development_map.get(country, 'Mixed')

def get_who_region(country):
    """تحديد منطقة WHO للدولة"""
    region_map = {
        'Afghanistan': 'EMRO',
        'Japan': 'WPRO',
        'United States of America': 'AMRO',
        'Germany': 'EURO',
        'Brazil': 'AMRO',
        'India': 'SEARO'
    }
    return region_map.get(country, 'Global')


def create_fallback_data():
    """Fallback data if WHO loading fails"""
    np.random.seed(42)
    
    countries = ['United States', 'Japan', 'Germany', 'Brazil', 'India', 'China']
    years = list(range(2000, 2024))
    
    data = []
    for country in countries:
        base_life = np.random.uniform(70, 85)
        base_mortality = np.random.uniform(5, 50)
        
        for year in years:
            year_factor = (year - 2000) * 0.15
            
            # Life Expectancy
            life_value = base_life + year_factor + np.random.normal(0, 0.5)
            life_value = max(65, min(90, life_value))
            
            # Mortality Rate
            mortality_value = base_mortality - year_factor * 0.3 + np.random.normal(0, 1)
            mortality_value = max(2, min(100, mortality_value))
            
            data.extend([
                {
                    'Country': country,
                    'Year': year,
                    'Metric': 'Life Expectancy',
                    'Value': round(life_value, 1),
                    'Unit': 'years',
                    'WHO_Region': 'Global',
                    'Development_Level': 'Mixed',
                    'Data_Quality': 'Synthetic'
                },
                {
                    'Country': country,
                    'Year': year,
                    'Metric': 'Under-5 Mortality Rate',
                    'Value': round(mortality_value, 1),
                    'Unit': 'per 1000',
                    'WHO_Region': 'Global',
                    'Development_Level': 'Mixed',
                    'Data_Quality': 'Synthetic'
                }
            ])
    
    df = pd.DataFrame(data)
    df['Value_Indexed'] = df.groupby(['Country', 'Metric'])['Value'].transform(
        lambda x: (x / x.iloc[0] * 100) if len(x) > 0 and x.iloc[0] != 0 else 100
    )
    
    st.session_state.data_source = "Synthetic Data (Fallback)"
    return df

# ============================================
# INITIALIZE DATA
# ============================================
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.df = None
    st.session_state.data_source = "Loading..."

# Load data
df = load_who_data()
st.session_state.df = df
st.session_state.data_loaded = True

# ============================================
# SIDEBAR - CONTROLS
# ============================================
with st.sidebar:
    st.markdown('<div class="sidebar-section">🌍 DASHBOARD CONTROLS</div>', unsafe_allow_html=True)
    
    # Data source info
    st.info(f"Data: {st.session_state.data_source}")
    
    st.markdown("---")
    
    # Metric selection
    available_metrics = df['Metric'].unique()
    selected_metric = st.selectbox(
        "Select Health Indicator:",
        available_metrics,
        index=0
    )
    
    # Country selection
    available_countries = sorted(df['Country'].unique())
    st.sidebar.info(f"Total countries: {len(available_countries)}")
    
    selected_countries = st.multiselect(
        "Select Countries:",
        available_countries,
        default=available_countries[:3] if len(available_countries) >= 3 else available_countries
    )
    
    # Year range
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    
    year_range = st.slider(
        "Select Year Range:",
        min_year, max_year,
        (max_year - 10, max_year)
    )
    
    # Region filter
    available_regions = ['All'] + sorted(df['WHO_Region'].unique().tolist())
    selected_region = st.selectbox("Filter by Region:", available_regions)
    
    st.markdown("---")
    
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()

# ============================================
# MAIN DASHBOARD
# ============================================

# HEADER
st.markdown('<h1 class="main-header">🏥 WHO Global Health Dashboard</h1>', unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align: center; color: #4B5563; margin-bottom: 2rem;'>
Interactive analysis of global health indicators | {len(selected_countries) if selected_countries else 'No'} countries selected
</div>
""", unsafe_allow_html=True)

# FILTER DATA
if selected_countries:
    filtered_df = df[
        (df['Country'].isin(selected_countries)) &
        (df['Year'].between(year_range[0], year_range[1])) &
        (df['Metric'] == selected_metric)
    ]
    
    if not filtered_df.empty:
        # KPI METRICS
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_value = filtered_df['Value'].mean()
            st.metric("Average Value", f"{avg_value:.1f} {filtered_df['Unit'].iloc[0]}")
        
        with col2:
            top_country = filtered_df.loc[filtered_df['Value'].idxmax(), 'Country']
            st.metric("Highest Value", top_country)
        
        with col3:
            improvement = filtered_df[filtered_df['Year'] == year_range[1]]['Value'].mean() - \
                         filtered_df[filtered_df['Year'] == year_range[0]]['Value'].mean()
            st.metric("Improvement", f"{improvement:+.1f}")
        
        with col4:
            st.metric("Countries", len(selected_countries))
        
        st.markdown("---")
        
        # CHART 1: TIME SERIES
        st.subheader(f"📈 {selected_metric} Trends")
        
        fig1 = px.line(
            filtered_df,
            x='Year',
            y='Value',
            color='Country',
            title=f'{selected_metric} ({year_range[0]}-{year_range[1]})',
            labels={'Value': f'{selected_metric} ({filtered_df["Unit"].iloc[0]})'},
            markers=True
        )
        
        fig1.update_layout(height=500)
        st.plotly_chart(fig1, width='stretch')

        
        # CHART 2: COUNTRY COMPARISON
        st.subheader("🌐 Country Comparison")
        
        col_chart, col_info = st.columns([3, 1])
        
        with col_chart:
            latest_data = filtered_df[filtered_df['Year'] == year_range[1]]
            if not latest_data.empty:
                fig2 = px.bar(
                    latest_data.sort_values('Value', ascending=False),
                    x='Country',
                    y='Value',
                    color='WHO_Region',
                    title=f'{selected_metric} in {year_range[1]}',
                    text='Value'
                )
                fig2.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                st.plotly_chart(fig2, width='stretch')

        
        with col_info:
            st.markdown("**Selected Countries**")
            for country in selected_countries:
                country_data = filtered_df[filtered_df['Country'] == country]
                if not country_data.empty:
                    # البحث عن بيانات السنة المطلوبة بأمان
                    year_data = country_data[country_data['Year'] == year_range[1]]
                    if not year_data.empty:
                        latest = year_data['Value'].iloc[0]
                        st.write(f"✅ **{country}**: {latest:.1f}")
                    else:
                        # إذا لم توجد بيانات لهذه السنة، نأخذ آخر سنة متاحة
                        latest_year = country_data['Year'].max()
                        latest_value = country_data[country_data['Year'] == latest_year]['Value'].iloc[0]
                        st.write(f"⚠️ **{country}**: {latest_value:.1f} ({latest_year})")
                else:
                    st.write(f"❌ **{country}**: No data")
        
        # DATA TABLE
        st.subheader("📋 Data Table")
        st.dataframe(
            filtered_df[['Country', 'Year', 'Metric', 'Value', 'Unit', 'WHO_Region']]
            .sort_values(['Country', 'Year']),
            width='stretch'
        )
        
    else:
        st.warning("No data available for selected filters.")
        
else:
    st.info("👈 Please select countries from the sidebar to begin analysis.")

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown('<div class="footer">', unsafe_allow_html=True)

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**📚 Data Sources**")
    st.markdown("""
    - World Health Organization
    - Global Health Observatory
    - Synthetic Data for Demonstration
    """)

with footer_col2:
    st.markdown("**🔬 Methodology**")
    st.markdown("""
    - Data Cleaning & Processing
    - Statistical Analysis
    - Interactive Visualization
    """)

with footer_col3:
    st.markdown("**📝 Project Info**")
    st.markdown(f"""
    **Capstone Project - MSIT 5910**  
    University of the People  
    **Developer:** Hazem Alahmad  
    **Date:** {datetime.now().strftime("%B %d, %Y")}
    """)

st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# DEBUG INFO
# ============================================
if st.sidebar.checkbox("Show Debug Info", value=False):
    with st.expander("Debug Information"):
        st.write(f"Total records: {len(df)}")
        st.write(f"Countries in data: {df['Country'].nunique()}")
        st.write(f"Available countries: {available_countries}")
        st.write(f"Data source: {st.session_state.data_source}")