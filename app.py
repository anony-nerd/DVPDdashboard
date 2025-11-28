import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="ECE Research Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
    <style>
    div.block-container {padding-top: 1rem;}
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4788;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f2f6 0%, #ffffff 50%, #f0f2f6 100%);
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f4788;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = {
        'S_No': list(range(1, 28)),
        'Name': [
            'Dr Binod Kumar Kanaujia', 'Dr Arun K Khosla', 'Dr B S Saini', 'Dr Mamta Khosla',
            'Dr Ashish Raman', 'Dr Asutosh Kar', 'Dr Balwinder Raj', 'Dr Deepti Kakkar',
            'Dr Indu Saini', 'Dr Neetu Sood', 'Dr Ramesh K Sunkaria', 'Dr Aijaz Mehdi Zaidi',
            'Dr. Manjeet Singh', 'Dr Nitesh Kashyap', 'Dr Pawan Kumar Verma',
            'Dr Sateesh Kumar Awasthi', 'Dr Sukwinder Singh', 'Dr Tarun Chaudhary',
            'Dr Amina Girdher', 'Dr Bodile Roshan Mukindrao', 'Dr. Kundan Kumar',
            'Dr Pheirojam Pooja', 'Dr Robin Kalyan', 'Dr Rohit Singh', 'Dr Sachchidanand',
            'Dr Sumon Modak', 'Dr. V Narasimha Nayak'
        ],
        'Designation': [
            'Director, NITJ', 'Professor', 'Professor', 'Professor', 'Associate Professor & Head',
            'Associate Professor', 'Associate Professor', 'Associate Professor', 'Associate Professor',
            'Associate Professor', 'Associate Professor', 'Assistant Professor (Grade-I)',
            'Assistant Professor (Grade-I)', 'Assistant Professor (Grade-I)', 'Assistant Professor (Grade-I)',
            'Assistant Professor (Grade-I)', 'Assistant Professor (Grade-I)', 'Assistant Professor (Grade-I)',
            'Assistant Professor Grade-II', 'Assistant Professor (Grade-II)', 'Assistant Professor (Grade-II)',
            'Assistant Professor Grade-II', 'Assistant Professor Grade-II', 'Assistant Professor (Grade-II)',
            'Assistant Professor Grade-II', 'Assistant Professor Grade-II', 'Assistant Professor Grade-II'
        ],
        'Journal_Publications': [
            347, 45, 61, 56, 84, 54, 107, 36, 38, 31, 83, 19, 18, 17, 15, 10, 12, 20, 7, 6, 13, 14, 5, 25, 0, 17, 8
        ],
        'Conference_Publications': [
            93, 31, 56, 35, 33, 50, 51, 41, 34, 43, 73, 8, 13, 16, 17, 18, 17, 21, 5, 8, 9, 1, 8, 6, 0, 8, 8
        ],
        'Books_Chapters': [
            25, 25, 16, 11, 15, 3, 21, 22, 8, 9, 6, 1, 3, 1, 4, 3, 1, 14, 0, 2, 0, 2, 0, 1, 0, 0, 0
        ],
        'Research_Projects_Completed': [
            8, 11, 1, 3, 6, 6, 7, 0, 6, 3, 14, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ],
        'Research_Projects_Ongoing': [
            3, 2, 0, 4, 10, 0, 3, 1, 0, 1, 4, 1, 1, 2, 1, 1, 3, 1, 0, 1, 3, 0, 0, 2, 0, 0, 0
        ],
        'Domain': [
            'Communication Systems', 'Human–Computer Interaction (HCI)', 'Signal processing', 'ML',
            'ML', 'Signal processing', 'Nanoelectronics', 'ML', 'ML', 'Signal processing',
            'Signal processing', 'ML', 'iot', 'Antenna design', 'iot', 'Signal Processing',
            'iot', 'Nanoelectronics', 'Spectrum', 'Signal processing', 'Antenna design',
            'Nanoelectronics', 'Amplifier', 'Communication Systems', 'Beam conductors',
            'Antenna design', 'Communication Systems'
        ]
    }
    
    df = pd.DataFrame(data)
    df['Total_Publications'] = df['Journal_Publications'] + df['Conference_Publications'] + df['Books_Chapters']
    df['Total_Research_Projects'] = df['Research_Projects_Completed'] + df['Research_Projects_Ongoing']
    
    return df

df = load_data()

st.markdown('<div class="main-title">🎓 ECE Research Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Faculty Research Analytics - Electronics & Communication Engineering</div>', unsafe_allow_html=True)
st.markdown(f"*Last Updated: {datetime.now().strftime('%B %d, %Y')}*")

st.sidebar.header("🔍 Filter Options")

search_name = st.sidebar.text_input("🔎 Search Professor by Name", "")

all_designations = sorted(df['Designation'].unique())
selected_designations = st.sidebar.multiselect(
    "👔 Filter by Designation",
    options=all_designations,
    default=all_designations
)

all_domains = sorted(df['Domain'].unique())
selected_domains = st.sidebar.multiselect(
    "🔬 Filter by Research Domain",
    options=all_domains,
    default=all_domains
)

min_total_pubs = st.sidebar.slider(
    "📚 Minimum Total Publications",
    min_value=0,
    max_value=int(df['Total_Publications'].max()),
    value=0
)

min_journal_pubs = st.sidebar.slider(
    "📰 Minimum Journal Publications",
    min_value=0,
    max_value=int(df['Journal_Publications'].max()),
    value=0
)

filtered_df = df.copy()

if search_name:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False, na=False)]

if selected_designations:
    filtered_df = filtered_df[filtered_df['Designation'].isin(selected_designations)]

if selected_domains:
    filtered_df = filtered_df[filtered_df['Domain'].isin(selected_domains)]

filtered_df = filtered_df[filtered_df['Total_Publications'] >= min_total_pubs]
filtered_df = filtered_df[filtered_df['Journal_Publications'] >= min_journal_pubs]

st.markdown("---")
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👨‍🏫 Total Professors", len(filtered_df))
    st.metric("📚 Total Journal Publications", filtered_df['Journal_Publications'].sum())

with col2:
    st.metric("📄 Total Conference Publications", filtered_df['Conference_Publications'].sum())
    st.metric("📖 Total Books/Chapters", filtered_df['Books_Chapters'].sum())

with col3:
    st.metric("✅ Completed Projects", filtered_df['Research_Projects_Completed'].sum())
    st.metric("🔄 Ongoing Projects", filtered_df['Research_Projects_Ongoing'].sum())

with col4:
    avg_pubs = filtered_df['Total_Publications'].mean() if len(filtered_df) > 0 else 0
    st.metric("📊 Avg Publications/Professor", f"{avg_pubs:.1f}")
    st.metric("🔬 Unique Domains", filtered_df['Domain'].nunique())

st.markdown("---")

st.subheader("📈 Research Analytics")

col1, col2 = st.columns(2)

with col1:
    top_profs = filtered_df.nlargest(15, 'Total_Publications')[['Name', 'Total_Publications']].copy()
    top_profs['Name'] = top_profs['Name'].str.replace('Dr ', '')
    
    fig1 = px.bar(
        top_profs,
        x='Total_Publications',
        y='Name',
        orientation='h',
        title='Top 15 Professors by Total Publications',
        labels={'Total_Publications': 'Total Publications', 'Name': 'Professor'},
        color='Total_Publications',
        color_continuous_scale='Blues'
    )
    fig1.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    domain_pubs = filtered_df.groupby('Domain')['Total_Publications'].sum().reset_index()
    domain_pubs = domain_pubs.sort_values('Total_Publications', ascending=False)
    
    fig2 = px.bar(
        domain_pubs,
        x='Domain',
        y='Total_Publications',
        title='Total Publications by Research Domain',
        labels={'Total_Publications': 'Total Publications', 'Domain': 'Research Domain'},
        color='Total_Publications',
        color_continuous_scale='Viridis'
    )
    fig2.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    project_data = filtered_df.groupby('Name')[['Research_Projects_Completed', 'Research_Projects_Ongoing']].sum()
    project_data = project_data[project_data.sum(axis=1) > 0].nlargest(15, 'Research_Projects_Completed')
    
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        name='Completed',
        x=project_data.index.str.replace('Dr ', ''),
        y=project_data['Research_Projects_Completed'],
        marker_color='#2ecc71'
    ))
    fig3.add_trace(go.Bar(
        name='Ongoing',
        x=project_data.index.str.replace('Dr ', ''),
        y=project_data['Research_Projects_Ongoing'],
        marker_color='#3498db'
    ))
    
    fig3.update_layout(
        title='Research Projects: Completed vs Ongoing (Top 15)',
        xaxis_title='Professor',
        yaxis_title='Number of Projects',
        barmode='stack',
        height=500
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    designation_counts = filtered_df['Designation'].value_counts().reset_index()
    designation_counts.columns = ['Designation', 'Count']
    
    fig4 = px.pie(
        designation_counts,
        values='Count',
        names='Designation',
        title='Faculty Distribution by Designation',
        hole=0.4
    )
    fig4.update_layout(height=500)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
col5, col6 = st.columns(2)

with col5:
    pub_types = pd.DataFrame({
        'Publication Type': ['Journal', 'Conference', 'Books/Chapters'],
        'Count': [
            filtered_df['Journal_Publications'].sum(),
            filtered_df['Conference_Publications'].sum(),
            filtered_df['Books_Chapters'].sum()
        ]
    })
    
    fig5 = px.pie(
        pub_types,
        values='Count',
        names='Publication Type',
        title='Publication Type Distribution',
        color_discrete_sequence=['#e74c3c', '#3498db', '#f39c12']
    )
    fig5.update_layout(height=400)
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    domain_desig = filtered_df.groupby(['Domain', 'Designation']).size().reset_index(name='Count')
    
    fig6 = px.bar(
        domain_desig,
        x='Domain',
        y='Count',
        color='Designation',
        title='Faculty Count by Domain and Designation',
        barmode='stack'
    )
    fig6.update_layout(height=400)
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
st.subheader("📋 Detailed Faculty Data")

display_df = filtered_df[[
    'S_No', 'Name', 'Designation', 'Domain',
    'Journal_Publications', 'Conference_Publications', 'Books_Chapters',
    'Total_Publications', 'Research_Projects_Completed', 'Research_Projects_Ongoing',
    'Total_Research_Projects'
]].sort_values('Total_Publications', ascending=False)

with st.expander("📊 View Full Research Data", expanded=True):
    st.dataframe(
        display_df.style.background_gradient(cmap='Blues', subset=['Total_Publications'])
                        .background_gradient(cmap='Greens', subset=['Total_Research_Projects']),
        use_container_width=True,
        height=400
    )

col7, col8, col9 = st.columns([1, 1, 2])

with col7:
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name=f"ece_research_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col8:
    full_csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Complete Data (CSV)",
        data=full_csv,
        file_name=f"ece_complete_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

st.markdown("---")
st.subheader("📈 Summary Statistics")

col10, col11 = st.columns(2)

with col10:
    with st.expander("📊 Publication Statistics by Domain"):
        domain_stats = filtered_df.groupby('Domain').agg({
            'Journal_Publications': 'sum',
            'Conference_Publications': 'sum',
            'Books_Chapters': 'sum',
            'Total_Publications': 'sum'
        }).sort_values('Total_Publications', ascending=False)
        st.dataframe(domain_stats.style.background_gradient(cmap='YlOrRd'), use_container_width=True)

with col11:
    with st.expander("📊 Research Project Statistics by Designation"):
        desig_stats = filtered_df.groupby('Designation').agg({
            'Research_Projects_Completed': 'sum',
            'Research_Projects_Ongoing': 'sum',
            'Total_Research_Projects': 'sum'
        }).sort_values('Total_Research_Projects', ascending=False)
        st.dataframe(desig_stats.style.background_gradient(cmap='Greens'), use_container_width=True)

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>ECE Research Dashboard | Electronics & Communication Engineering Department</p>
        <p style='font-size: 0.8rem;'>Data reflects faculty research contributions and ongoing projects</p>
    </div>
""", unsafe_allow_html=True)