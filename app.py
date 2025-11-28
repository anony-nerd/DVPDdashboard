import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
    st.markdown("#### Top 15 Professors by Total Publications")
    top_profs = filtered_df.nlargest(15, 'Total_Publications')[['Name', 'Total_Publications']].copy()
    top_profs['Name'] = top_profs['Name'].str.replace('Dr ', '')
    
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(top_profs['Name'], top_profs['Total_Publications'], color='#4A90E2')
    ax.set_xlabel('Total Publications', fontsize=12)
    ax.set_ylabel('Professor', fontsize=12)
    ax.invert_yaxis()
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, f'{int(width)}', 
                ha='left', va='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown("#### Total Publications by Research Domain")
    domain_pubs = filtered_df.groupby('Domain')['Total_Publications'].sum().reset_index()
    domain_pubs = domain_pubs.sort_values('Total_Publications', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = plt.cm.viridis(domain_pubs['Total_Publications'] / domain_pubs['Total_Publications'].max())
    bars = ax.bar(range(len(domain_pubs)), domain_pubs['Total_Publications'], color=colors)
    ax.set_xlabel('Research Domain', fontsize=12)
    ax.set_ylabel('Total Publications', fontsize=12)
    ax.set_xticks(range(len(domain_pubs)))
    ax.set_xticklabels(domain_pubs['Domain'], rotation=45, ha='right')
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

col3, col4 = st.columns(2)

with col3:
    st.markdown("#### Research Projects: Completed vs Ongoing (Top 15)")
    project_data = filtered_df.groupby('Name')[['Research_Projects_Completed', 'Research_Projects_Ongoing']].sum()
    project_data = project_data[project_data.sum(axis=1) > 0].nlargest(15, 'Research_Projects_Completed')
    
    if len(project_data) > 0:
        fig, ax = plt.subplots(figsize=(10, 8))
        x = range(len(project_data))
        width = 0.8
        
        p1 = ax.bar(x, project_data['Research_Projects_Completed'], width, label='Completed', color='#2ecc71')
        p2 = ax.bar(x, project_data['Research_Projects_Ongoing'], width, 
                    bottom=project_data['Research_Projects_Completed'], label='Ongoing', color='#3498db')
        
        ax.set_ylabel('Number of Projects', fontsize=12)
        ax.set_xlabel('Professor', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels([name.replace('Dr ', '') for name in project_data.index], rotation=45, ha='right')
        ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No project data available for selected filters")

with col4:
    st.markdown("#### Faculty Distribution by Designation")
    designation_counts = filtered_df['Designation'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = plt.cm.Set3(range(len(designation_counts)))
    wedges, texts, autotexts = ax.pie(designation_counts.values, labels=designation_counts.index, 
                                        autopct='%1.1f%%', colors=colors, startangle=90)
    
    for text in texts:
        text.set_fontsize(9)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)
    
    ax.axis('equal')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")
col5, col6 = st.columns(2)

with col5:
    st.markdown("#### Publication Type Distribution")
    pub_types = pd.DataFrame({
        'Publication Type': ['Journal', 'Conference', 'Books/Chapters'],
        'Count': [
            filtered_df['Journal_Publications'].sum(),
            filtered_df['Conference_Publications'].sum(),
            filtered_df['Books_Chapters'].sum()
        ]
    })
    
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = ['#e74c3c', '#3498db', '#f39c12']
    wedges, texts, autotexts = ax.pie(pub_types['Count'], labels=pub_types['Publication Type'], 
                                        autopct='%1.1f%%', colors=colors, startangle=90)
    
    for text in texts:
        text.set_fontsize(11)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    ax.axis('equal')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col6:
    st.markdown("#### Faculty Count by Domain and Designation")
    domain_desig = filtered_df.groupby(['Domain', 'Designation']).size().reset_index(name='Count')
    
    pivot_data = domain_desig.pivot(index='Domain', columns='Designation', values='Count').fillna(0)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    pivot_data.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
    ax.set_xlabel('Research Domain', fontsize=12)
    ax.set_ylabel('Faculty Count', fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.legend(title='Designation', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

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
