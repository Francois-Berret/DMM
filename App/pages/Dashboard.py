import streamlit as st
import pandas as pd
import plotly.express as px


data = st.session_state['data']

## ----------- DASHBOARD PAGE ------------

# Title
st.markdown(
    "<h1 style='text-align: center;'>Data Jobs Dashboard</h1>",
    unsafe_allow_html=True
)
    
# Text
st.markdown(
    "<h3 style='text-align: center;'>Visualisation du marché de l'emploi français dans les métiers de la data</h3>",
    unsafe_allow_html=True
)
# Cluster filtering
cluster_options = ["Tout voir"] + data["cluster"].unique().tolist()
cluster_filter = st.selectbox("Type d'emploi", cluster_options)
    
if cluster_filter == "Tout voir":
    filtered_data = data
else:
    filtered_data = data[data["cluster"] == cluster_filter]
    
# Skills filtering
skills_options = ["Tout voir"] + data['skills'].str.split(', ', expand=True).stack().unique().tolist()
skills_filter = st.selectbox("Skills", skills_options)
    
if skills_filter == "Tout voir":
    filtered_data = filtered_data
else:
    filtered_data = filtered_data[filtered_data["skills"] == skills_filter]
    
# Mapbox
def createmapbox(data):
    fig = px.scatter_mapbox(data, lat='lat', lon='lon', hover_name="job_title", hover_data="job_company", color="job_class", height=600, color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(mapbox=dict(center=dict(lat=46.603354, lon=1.888334), zoom=5))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_traces(marker=dict(size=10))
    return fig

mapbox = createmapbox(filtered_data)
st.plotly_chart(mapbox,use_container_width = True)

st.markdown("----------------")

# Histogram to visualize the number of offers / type of job sought
fig = px.histogram(
    data,
    x="job_class",
    color="job_class",
    title="Offre d'emploi / types de poste",
    labels={'job_class' : "Types de poste",
            "count": "Nombre d'offres"}
    )
fig.update_layout(showlegend=False, title_text="Offre d'emploi / types de poste", yaxis_title="Nombre d'offres", title_x=0.4)
st.plotly_chart(fig, use_container_width = True)

st.markdown('--------------')

# Cluster filtering bis
cluster = ["Tout voir"] + data["cluster"].unique().tolist()
cluster_filter2 = st.selectbox("Type d'emploi", cluster, key="cluster_filter2")

# Top 10 skills / clusters mask
if cluster_filter2 == "Tout voir":
    filtered_data2 = data['skills'].str.split(', ', expand=True).stack().value_counts()
    top_skills = data['skills'].str.split(', ', expand=True).stack().value_counts()
    filtered_data2 = top_skills.head(10).to_frame('count')
    filtered_data2 = filtered_data2.rename_axis('skills').reset_index()
else:
    mask =data['cluster']==cluster_filter2
    new_data = data.where(mask)
    top_skills = new_data['skills'].str.split(', ', expand=True).stack().value_counts()
    filtered_data2 = top_skills.head(10).to_frame('count')
    filtered_data2 = filtered_data2.rename_axis('skills').reset_index()

# Top 10 skills histogram
fig2 = px.histogram(
    filtered_data2,
    x="skills",
    y="count",
    color="skills",
    color_discrete_sequence=px.colors.qualitative.Prism
)
fig2.update_layout(showlegend=False, title_text="Top 10 des compétences les plus mentionnées",
                   yaxis_title="Nombre d'offres", title_x=0.4)
st.plotly_chart(fig2, use_container_width = True)

# Top 10 recruiters histogtram
company = data['job_company'].value_counts().head(10)
top_company = pd.DataFrame({"Société" : company.index, "Nombre d'offre": company.values})
fig3 = px.histogram(
    top_company,
    x="Société",
    y="Nombre d'offre",
    color="Société",
    color_discrete_sequence=px.colors.qualitative.Dark2
)
fig3.update_layout(showlegend=False, title_text="Top 10 des entreprises qui recrutent le plus",
                   yaxis_title="Nombre d'offres", title_x=0.4)
st.plotly_chart(fig3, use_container_width = True)