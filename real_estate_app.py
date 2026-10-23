import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="365 Real Estate | Valuation Studio", page_icon="🏙️", layout="wide", initial_sidebar_state="expanded")
BASE = Path(__file__).resolve().parent
MODEL_PATH, DATA_PATH = BASE / "real_estate_valuation_model.joblib", BASE / "real_estate_model_dataset.csv"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:radial-gradient(ellipse at 10% 0%, #18334a 0%, #0b1422 40%, #080e18 100%); color:#edf4fb;}
[data-testid="stSidebar"] {background:#0c1726;border-right:1px solid #24364b;}
.hero {padding:28px 32px;border:1px solid #29445a;border-radius:24px;background:linear-gradient(120deg,rgba(24,57,78,.96),rgba(15,29,48,.94));margin-bottom:22px;box-shadow:0 18px 50px #0003;}
.eyebrow {color:#77e2cf;text-transform:uppercase;letter-spacing:2px;font-size:11px;font-weight:800;}
.hero h1 {font-family:Manrope,sans-serif;font-size:34px;font-weight:800;margin:7px 0;color:#f5fbff;}
.hero p {color:#b7c9d9;margin:0;max-width:800px;}
.panel {padding:22px;border:1px solid #24384d;border-radius:18px;background:rgba(14,27,43,.86);margin-bottom:18px;}
.small-muted {color:#9eb2c7;font-size:13px;}
.result {padding:22px;border-radius:18px;background:linear-gradient(135deg,#103f43,#102e3d);border:1px solid #26766e;}
.result-label {color:#9ce9d9;font-size:12px;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;}
.result-value {font-family:Manrope,sans-serif;font-size:34px;font-weight:800;color:#fff;margin:6px 0;}
div[data-testid="stMetric"] {background:#101f30;border:1px solid #263c51;padding:16px 18px;border-radius:16px;}
.stButton>button, .stFormSubmitButton>button {border-radius:12px;border:0;background:linear-gradient(90deg,#4dd5bd,#7ce5cb);color:#09202a;font-weight:800;padding:10px 20px;}
.stButton>button:hover,.stFormSubmitButton>button:hover {background:#a0f2df;color:#09202a;}
/* Improve readability of dashboard metric cards */
[data-testid="stMetricLabel"] {
    color: #B8C7D9 !important;
}

[data-testid="stMetricValue"] {
    color: #F1F5F9 !important;
}

[data-testid="stMetricDelta"] {
    color: #34D399 !important;
}

/* Improve general text contrast */
.stMarkdown p,
.stMarkdown label {
    color: #CBD5E1;
}

/* Sidebar text readability */
[data-testid="stSidebar"] {
    background-color: #0B1625 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #CBD5E1;
}

/* Keep the status message readable */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background-color: #12332F;
    color: #86EFAC;
}

/* Make section headings clear */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #F1F5F9 !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model(): return joblib.load(MODEL_PATH)
@st.cache_data
def load_data(): return pd.read_csv(DATA_PATH, low_memory=False)

st.sidebar.markdown("## 🏙️ 365 REAL ESTATE")
st.sidebar.caption("VALUATION INTELLIGENCE PLATFORM")
page = st.sidebar.radio("WORKSPACE", ["Valuation Studio", "Market Explorer", "About the Model"], label_visibility="visible")
st.sidebar.markdown("---")
st.sidebar.markdown("**Model status**")
st.sidebar.success("Model & transaction data loaded" if MODEL_PATH.exists() and DATA_PATH.exists() else "Required model/data files missing")
st.sidebar.caption("Estimates are decision support, not a formal appraisal.")

if not MODEL_PATH.exists() or not DATA_PATH.exists():
    st.error("Place real_estate_valuation_model.joblib and real_estate_model_dataset.csv beside this app.")
    st.stop()
model, df = load_model(), load_data()
for c in ["area_sqft","actual_worth","sale_year","sale_month"]:
    if c in df: df[c] = pd.to_numeric(df[c], errors="coerce")

def options(col, default="Unknown"):
    vals = sorted(df[col].dropna().astype(str).unique().tolist()) if col in df else []
    return vals or [default]

if page == "Valuation Studio":
    st.markdown('<div class="hero"><div class="eyebrow">Property intelligence · Dubai</div><h1>Valuation Studio</h1><p>Estimate a residential property value using historical transaction patterns. Configure the property profile and review nearby comparable transactions before making a decision.</p></div>', unsafe_allow_html=True)
    left, right = st.columns([1.08, .92], gap="large")
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("01 · Property profile")
        with st.form("valuation_form"):
            community = st.selectbox("Community", options("area_name_en"))
            c1,c2 = st.columns(2)
            with c1: prop_type = st.selectbox("Property type", options("property_type_en"))
            with c2: subtype = st.selectbox("Subtype", options("property_sub_type_en"))
            c1,c2 = st.columns(2)
            with c1: rooms = st.selectbox("Room category", options("rooms_en"))
            with c2: reg = st.selectbox("Registration type", options("reg_type_en"))
            c1,c2 = st.columns(2)
            with c1: size = st.number_input("Built-up area (sq ft)", min_value=100.0, max_value=100000.0, value=1000.0, step=50.0)
            with c2: parking = st.selectbox("Parking available", [1,0], format_func=lambda x: "Yes" if x else "No")
            master_options = ["Unknown"] + options("master_project_en")
            master = st.selectbox("Master project (optional)", master_options)
            c1,c2 = st.columns(2)
            with c1: year = st.selectbox("Transaction year", list(range(2020,2026)), index=5)
            with c2: month = st.selectbox("Transaction month", list(range(1,13)), index=5)
            submitted = st.form_submit_button("✦  Generate valuation", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><div class="eyebrow">Quick market snapshot</div><h3>Transaction context</h3>', unsafe_allow_html=True)
        st.metric("Transactions in dataset", f"{len(df):,}")
        if "actual_worth" in df:
            st.metric("Median recorded sale", f"AED {df.actual_worth.median():,.0f}")
        if "area_sqft" in df:
            st.metric("Median property size", f"{df.area_sqft.median():,.0f} sq ft")
        st.markdown('<p class="small-muted">The snapshot describes the loaded modelling dataset; it is not a live market feed.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="panel"><h4>How to use the estimate</h4><p class="small-muted">1. Match the community and property characteristics.<br>2. Compare the estimate with recent similar transactions.<br>3. Escalate unusual, luxury or poorly represented properties to a human valuer.</p></div>', unsafe_allow_html=True)
    if submitted:
        row = pd.DataFrame([{"area_sqft":size,"has_parking":parking,"sale_year":year,"sale_month":month,"area_name_en":community,"property_type_en":prop_type,"property_sub_type_en":subtype,"rooms_en":rooms,"reg_type_en":reg,"master_project_en":None if master=="Unknown" else master}])
        try:
            value = max(0.0, float(model.predict(row)[0]))
            # Transparent indicative range; not a formal statistical prediction interval.
            lo, hi = value*.80, value*1.20
            st.markdown(f'<div class="result"><div class="result-label">Indicative estimated sale price</div><div class="result-value">AED {value:,.0f}</div><div style="color:#c3e7e4">Illustrative range ±20% · AED {lo:,.0f} – AED {hi:,.0f}</div></div>', unsafe_allow_html=True)
            a,b,c = st.columns(3)
            a.metric("Area", f"{size:,.0f} sq ft"); b.metric("Price per sq ft", f"AED {value/size:,.0f}"); c.metric("Range width", f"AED {hi-lo:,.0f}")
            st.subheader("Comparable transactions")
            comps = df[df.area_name_en.astype(str).eq(community)].copy()
            comps["size_difference_sqft"] = (comps.area_sqft-size).abs()
            if "instance_date" in comps: comps["instance_date"] = pd.to_datetime(comps.instance_date, errors="coerce")
            cols = [c for c in ["instance_date","area_name_en","property_type_en","property_sub_type_en","rooms_en","area_sqft","actual_worth","size_difference_sqft"] if c in comps]
            comps = comps.sort_values("size_difference_sqft").head(10)
            if len(comps): st.dataframe(comps[cols], use_container_width=True, hide_index=True)
            else: st.info("No comparable records found for this community in the loaded dataset.")
        except Exception as e: st.error(f"Unable to generate a prediction for these inputs: {e}")
elif page == "Market Explorer":
    st.markdown('<div class="hero"><div class="eyebrow">Market intelligence</div><h1>Market Explorer</h1><p>Explore recorded sales in the loaded dataset. Use these summaries as context, not as a substitute for current market research.</p></div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("Records", f"{len(df):,}"); c2.metric("Communities", f"{df.area_name_en.nunique():,}" if "area_name_en" in df else "—"); c3.metric("Median sale", f"AED {df.actual_worth.median():,.0f}" if "actual_worth" in df else "—")
    t1,t2,t3 = st.tabs(["Community ranking", "Price distribution", "Explore records"])
    with t1:
        if {"area_name_en","actual_worth"}.issubset(df.columns):
            n = st.slider("Minimum records per community", 1, 100, 10)
            agg = df.groupby("area_name_en").actual_worth.agg(median_price="median", mean_price="mean", transactions="count").query("transactions >= @n").sort_values("median_price",ascending=False).head(20)
            chart_data = agg.reset_index()

            fig = px.bar(
                chart_data,
                x="area_name_en",
                y="median_price",
                title="Top Communities by Median Sale Price",
                labels={
                    "area_name_en": "Community",
                    "median_price": "Median Sale Price (AED)"
                },
                color_discrete_sequence=["#77E2CF"],
                hover_data=["transactions", "mean_price"]
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0E1B2B",
                plot_bgcolor="#0E1B2B",
                font=dict(color="#EDF4FB"),
                title_font=dict(color="#F5FBFF", size=20),
                xaxis=dict(showgrid=False, tickangle=-35),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#294056",
                    tickprefix="AED ",
                    tickformat=",.0f"
                ),
                margin=dict(b=120)
            )

            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                agg.style.format({
                    "median_price": "AED {:,.0f}",
                    "mean_price": "AED {:,.0f}"
                }),
                use_container_width=True
            )
    with t2:
        if "actual_worth" in df:
            vals = df.actual_worth.dropna(); vals = vals[(vals>0)&(vals<=vals.quantile(.99))]
            price_bands = pd.cut(vals, bins=25)
            chart_data = (
                price_bands.value_counts()
                .sort_index()
                .rename_axis("Price band")
                .to_frame("Transactions")
            )

            chart_data.index = chart_data.index.astype(str)

                        fig = px.bar(
                chart_data.reset_index(),
                x="Price band",
                y="Transactions",
                title="Distribution of Recorded Sale Prices",
                labels={
                    "Price band": "Sale Price Band (AED)",
                    "Transactions": "Number of Transactions"
                },
                color_discrete_sequence=["#77E2CF"]
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0E1B2B",
                plot_bgcolor="#0E1B2B",
                font=dict(color="#EDF4FB"),
                title_font=dict(color="#F5FBFF", size=20),
                xaxis=dict(showgrid=False, tickangle=-45),
                yaxis=dict(showgrid=True, gridcolor="#294056"),
                margin=dict(b=140)
            )

            st.plotly_chart(fig, use_container_width=True)

            st.caption(
                "For readability, this view excludes the top 1% of sale prices "
                "from the displayed histogram only; the source dataset is unchanged."
            )
    with t3:
        community_filter = st.selectbox("Filter community", ["All communities"]+options("area_name_en"))
        view = df if community_filter=="All communities" else df[df.area_name_en.astype(str).eq(community_filter)]
        st.dataframe(view.head(500), use_container_width=True, hide_index=True)
        st.caption("Showing up to 500 records in the preview.")
else:
    st.markdown('<div class="hero"><div class="eyebrow">Transparency</div><h1>About the model</h1><p>Understand what the estimate means and where it should be used cautiously.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><h3>Model approach</h3><ul><li>Supervised regression trained on historical Dubai transaction records.</li><li>Inputs include area, property type/subtype, room category, parking, registration type and transaction date components.</li><li>Price-related fields that would reveal the answer should not be used as prediction inputs.</li></ul></div>', unsafe_allow_html=True)
    st.warning("The ±20% band is an illustrative range, not a statistically calibrated prediction interval. Model outputs depend on data quality and representation. Historical associations do not establish causation.")
    st.markdown('<div class="panel"><h3>When to involve a human valuer</h3><p class="small-muted">Use professional review for luxury or unusual properties, sparse communities, out-of-range sizes, non-standard property types, or when a transaction has special conditions not represented in the model.</p></div>', unsafe_allow_html=True)
