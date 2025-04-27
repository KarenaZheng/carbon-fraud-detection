#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events
import plotly.graph_objects as go
import pycountry

st.set_page_config(layout="wide")
st.title("🌱 Greenwashing Detection")

# === Load data ===
df = pd.read_csv("merged_output.csv")
year_cols = [str(y) for y in range(1996, 2026)]
df[year_cols] = df[year_cols].apply(pd.to_numeric, errors='coerce')

# === Standardize and encode country names to ISO-3 ===
def get_iso3(name):
    try:
        return pycountry.countries.lookup(name).alpha_3
    except:
        return None

def standardize_country(name):
    try:
        return pycountry.countries.lookup(name).name
    except:
        return name

df['Country'] = df['Country'].apply(standardize_country)
df['iso_alpha_3'] = df['Country'].apply(get_iso3)

# === Top filters ===
col1, col2 = st.columns([2, 5])
with col1:
    registry_filter = st.selectbox("Filter by Voluntary Registry", ["All"] + sorted(df['Voluntary Registry'].dropna().unique().tolist()))
with col2:
    credit_range = st.slider(
        "Total Credits Issued Range",
        float(df["Total Credits \nIssued"].min()),
        float(df["Total Credits \nIssued"].max()),
        (float(df["Total Credits \nIssued"].min()), float(df["Total Credits \nIssued"].max()))
    )

# === Apply filters ===
filtered_df = df.copy()
if registry_filter != "All":
    filtered_df = filtered_df[filtered_df['Voluntary Registry'] == registry_filter]
filtered_df = filtered_df[filtered_df["Total Credits \nIssued"].between(credit_range[0], credit_range[1])]
anomalies_all = filtered_df[filtered_df['anomaly_flag'] == -1]

# === Country anomaly counts ===
country_anomalies = anomalies_all['Country'].value_counts().reset_index()
country_anomalies.columns = ['Country', 'Anomaly Count']
country_anomalies['Country'] = country_anomalies['Country'].apply(standardize_country)
country_anomalies['iso_alpha_3'] = country_anomalies['Country'].apply(get_iso3)

# === Layout ===
layout_top = st.columns([2.5, 1.5])  # Area 1 | Area 2 + 3
layout_bot = st.columns([1.3, 1.0])  # Area 4 | Area 5

# === Area 1: Map with ISO-3 Choropleth ===
with layout_top[0]:
    st.markdown("#### Anomalies by Country (Map)")

    # Build full list of world countries from Plotly dataset
    all_countries = pd.DataFrame({'Country': px.data.gapminder()['country'].unique()})
    all_countries['Country'] = all_countries['Country'].apply(standardize_country)
    all_countries['iso_alpha_3'] = all_countries['Country'].apply(get_iso3)

    world_map_df = all_countries.merge(country_anomalies, on='Country', how='left')
    world_map_df['iso_alpha_3'] = world_map_df['iso_alpha_3_x'].fillna(world_map_df['iso_alpha_3_y'])
    world_map_df['Anomaly Count'] = world_map_df['Anomaly Count'].fillna(0)

    fig_map = px.choropleth(
        world_map_df,
        locations='iso_alpha_3',
        color='Anomaly Count',
        hover_name='Country',
        color_continuous_scale='greens',
        title='Click a Country to Filter (or Reset)'
    )
    fig_map.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        height=600,
        margin=dict(l=0, r=0, t=30, b=0),
        coloraxis_colorbar=dict(title="Anomalies")
    )

    click_data = plotly_events(fig_map, click_event=True, override_height=600)

    # Reset and selection logic
    if st.button("🔄 Reset Country Filter"):
        country_selection = None
    else:
        country_selection = None
        if click_data:
            point_index = click_data[0].get('pointNumber')
            if point_index is not None and point_index < len(world_map_df):
                clicked_country = world_map_df.iloc[point_index]['Country']
                if clicked_country in country_anomalies['Country'].values:
                    country_selection = clicked_country

# === Filter by selected country ===
if country_selection:
    region_filtered_df = filtered_df[filtered_df['Country'] == country_selection]
else:
    region_filtered_df = filtered_df
anomalies = region_filtered_df[region_filtered_df['anomaly_flag'] == -1]

# === Area 2: Scope bar chart ===
with layout_top[1]:
    st.markdown("#### Anomalies by Scope")
    scope_chart = anomalies['Scope'].value_counts().reset_index()
    scope_chart.columns = ['Scope', 'Anomaly Count']
    fig_scope = px.bar(scope_chart, x='Scope', y='Anomaly Count',
                       color='Anomaly Count', color_continuous_scale='greens')
    fig_scope.update_layout(height=280)
    st.plotly_chart(fig_scope, use_container_width=True)

    # === Area 3: Risk bar ===
    st.markdown("#### Risk Level Proportion")
    if 'Risk_Level' in anomalies.columns:
        risk_counts = anomalies['Risk_Level'].value_counts(normalize=True).reset_index()
        risk_counts.columns = ['Risk_Level', 'Proportion']
        fig_risk = go.Figure()
        color_map = {"Low": "lightgreen", "Moderate": "green", "High": "darkgreen"}
        for _, row in risk_counts.iterrows():
            fig_risk.add_trace(go.Bar(
                x=[row['Proportion']],
                y=["Risk"],
                name=row['Risk_Level'],
                orientation='h',
                marker=dict(color=color_map.get(row['Risk_Level'], "gray")),
                hovertemplate=f"{row['Risk_Level']}: {row['Proportion']:.0%}<extra></extra>"
            ))
        fig_risk.update_layout(
            barmode='stack',
            height=200,
            xaxis=dict(tickformat=".0%", range=[0, 1]),
            yaxis=dict(showticklabels=False),
            showlegend=True
        )
        st.plotly_chart(fig_risk, use_container_width=True)

# === Area 4: Project Table ===
with layout_bot[0]:
    st.markdown("#### Project Details")
    table_cols = ['Project_ID', 'Project Name', 'Scope', 'Type', 'Total Credits \nIssued']
    st.dataframe(anomalies[table_cols], use_container_width=True)

# === Area 5: Line chart ===
with layout_bot[1]:
    st.markdown("#### Annual Credit Trend")
    selected_project_id = st.selectbox("Select Project_ID", anomalies['Project_ID'].unique() if not anomalies.empty else [])
    if selected_project_id:
        proj_data = anomalies[anomalies['Project_ID'] == selected_project_id]
        line_df = pd.melt(proj_data[year_cols], var_name='Year', value_name='Credits')
        fig_line = px.line(line_df, x='Year', y='Credits',
                           title=f"Credits Over Time: {selected_project_id}", markers=True)
        fig_line.update_traces(line_color='green')
        st.plotly_chart(fig_line, use_container_width=True)

