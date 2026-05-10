import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Effect of Hydrogen Enrichment on Laminar Flame Speed and Adiabatic Flame Temperature of Premixed Methane-Air Flames Using Cantera",
    page_icon="🔥",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv("full_results.csv")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Combustion Controls")

selected_h2 = st.sidebar.selectbox(
    "Hydrogen Percentage (%)",
    sorted(df["H2 Percentage"].unique())
)

selected_phi = st.sidebar.slider(
    "Equivalence Ratio (ϕ)",
    min_value=0.6,
    max_value=1.4,
    step=0.1,
    value=1.0
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_df = df[
    df["H2 Percentage"] == selected_h2
]

selected_point = df[
    (df["H2 Percentage"] == selected_h2) &
    (abs(df["Equivalence Ratio"] - selected_phi) < 1e-6)
]

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🔥 Effect of Hydrogen Enrichment on Laminar Flame Speed and Adiabatic Flame Temperature of Premixed Methane-Air Flames Using Cantera")

st.markdown("""
Interactive computational combustion study using:

- Cantera
- GRI-Mech 3.0
- 1D Freely Propagating Flame Solver
- Python + Streamlit

This study investigates the influence of hydrogen enrichment
on laminar flame speed and adiabatic flame temperature
of premixed methane-air combustion.
""")

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------

if not selected_point.empty:

    flame_speed = selected_point["Flame Speed (m/s)"].values[0]
    flame_temp = selected_point["Flame Temperature (K)"].values[0]

    col1, col2 = st.columns(2)

    col1.metric(
        label="Laminar Flame Speed",
        value=f"{flame_speed:.3f} m/s"
    )

    col2.metric(
        label="Adiabatic Flame Temperature",
        value=f"{flame_temp:.1f} K"
    )

# ---------------------------------------------------
# MAIN CHARTS
# ---------------------------------------------------

tab1, tab2, tab3 = st.tabs([
    "Flame Speed",
    "Temperature",
    "Raw Data"
])

# ---------------------------------------------------
# TAB 1
# ---------------------------------------------------

with tab1:

    fig_speed = px.line(
        filtered_df,
        x="Equivalence Ratio",
        y="Flame Speed (m/s)",
        markers=True,
        title=f"Laminar Flame Speed for {selected_h2}% H₂"
    )

    fig_speed.update_layout(
        xaxis_title="Equivalence Ratio (ϕ)",
        yaxis_title="Flame Speed (m/s)",
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(
        fig_speed,
        use_container_width=True
    )

    st.markdown("""
### Physical Interpretation

- Flame speed increases with hydrogen enrichment.
- Maximum flame speed occurs near stoichiometric conditions.
- Lean and rich mixtures reduce flame propagation rates.

Hydrogen enhances:
- radical formation
- diffusivity
- combustion reactivity
""")

# ---------------------------------------------------
# TAB 2
# ---------------------------------------------------

with tab2:

    fig_temp = px.line(
        filtered_df,
        x="Equivalence Ratio",
        y="Flame Temperature (K)",
        markers=True,
        title=f"Adiabatic Flame Temperature for {selected_h2}% H₂"
    )

    fig_temp.update_layout(
        xaxis_title="Equivalence Ratio (ϕ)",
        yaxis_title="Temperature (K)",
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(
        fig_temp,
        use_container_width=True
    )

    st.markdown("""
### Temperature Trends

- Temperature peaks near stoichiometric combustion.
- Lean mixtures contain excess air which absorbs heat.
- Rich mixtures suffer incomplete combustion.
- Hydrogen slightly increases flame temperature.
""")

# ---------------------------------------------------
# TAB 3
# ---------------------------------------------------

with tab3:

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# ---------------------------------------------------
# THEORY SECTION
# ---------------------------------------------------

st.header("📘 Combustion Theory")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Equivalence Ratio")

    st.latex(
        r"\phi = \frac{(F/A)_{actual}}{(F/A)_{stoichiometric}}"
    )

    st.markdown("""
- ϕ < 1 → Lean combustion
- ϕ = 1 → Stoichiometric combustion
- ϕ > 1 → Rich combustion
""")

with col2:

    st.subheader("Hydrogen Effects")

    st.markdown("""
Hydrogen enrichment leads to:

- Faster flame propagation
- Improved flame stability
- Wider flammability limits
- Increased flashback risk

Key chain branching reaction:
""")

    st.latex(
        r"H + O_2 \rightarrow O + OH"
    )

# ---------------------------------------------------
# FULL COMPARISON CHART
# ---------------------------------------------------

st.header("📈 Full Dataset Comparison")

fig_compare = px.line(
    df,
    x="Equivalence Ratio",
    y="Flame Speed (m/s)",
    color="H2 Percentage",
    markers=True,
    title="Comparison of Flame Speed for All Hydrogen Fractions"
)

fig_compare.update_layout(
    template="plotly_dark",
    height=700
)

st.plotly_chart(
    fig_compare,
    use_container_width=True
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption("""
Developed using Python, Cantera, Streamlit, and GRI-Mech 3.0.

This application demonstrates computational analysis
of premixed methane-hydrogen combustion under laminar conditions.
""")