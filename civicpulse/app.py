"""
BRICS CivicPulse – Streamlit Prototype
From Citizen Voice to Development Action
Track 1: AI for Digital Public Infrastructure & Governance
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Page config & theme
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="BRICS CivicPulse",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS matching CivicPulse palette
st.markdown("""
<style>
    :root {
        --indigo: #1B2A4A;
        --teal: #00A8A8;
        --coral: #FF6B4A;
        --soft-gray: #F4F6F8;
    }
    .stApp { background-color: #F4F6F8; }
    h1, h2, h3 { color: #1B2A4A !important; }
    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #00A8A8;
    }
    .evidence-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-top: 4px solid #1B2A4A;
    }
    .priority-high { color: #FF6B4A; font-weight: 700; }
    .priority-med { color: #00A8A8; font-weight: 700; }
    div[data-testid="stMetricValue"] { color: #1B2A4A; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
DATA_DIR = Path(__file__).parent / "data"

@st.cache_data
def load_data():
    requests = pd.read_csv(DATA_DIR / "sample_requests.csv")
    infra = pd.read_csv(DATA_DIR / "infrastructure.csv")
    investments = pd.read_csv(DATA_DIR / "investment_plans.csv")
    return requests, infra, investments

requests_df, infra_df, invest_df = load_data()

# ---------------------------------------------------------------------------
# Simple AI extraction (rule-based for prototype)
# ---------------------------------------------------------------------------
CATEGORY_KEYWORDS = {
    "road": ["road", "bridge", "pothole", "highway", "सड़क", "రోడ్డు", "path", "approach"],
    "water": ["water", "pipeline", "hand pump", "tanker", "पानी", "drinking", "supply"],
    "healthcare": ["health", "doctor", "hospital", "phc", "ambulance", "clinic", "medical", "स्वास्थ्य"],
    "sanitation": ["drain", "garbage", "toilet", "street light", "waste", "sanitation", "light"],
    "education": ["school", "toilet", "classroom", "student", "education", "digital classroom"],
    "digital": ["internet", "network", "mobile", "digital", "connectivity", "online"],
}

URGENCY_WORDS = {
        "high": ["ambulance", "pregnant", "emergency", "unsafe", "completely", "unusable", "sick", "drop out"],
    "med": ["broken", "poor", "no ", "not working", "insufficient", "leaking"],
}

def extract_entities(text: str, language: str = "en") -> dict:
    """Simulate multilingual AI extraction."""
    text_lower = text.lower()
    
    # Category
    category = "other"
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(kw in text_lower for kw in kws):
            category = cat
            break
    
    # Urgency (0-100)
    urgency = 55
    if any(w in text_lower for w in ["ambulance", "pregnant", "emergency", "completely unusable", "unsafe"]):
        urgency = 90
    elif any(w in text_lower for w in ["broken", "no doctor", "no road", "overflowing", "dry"]):
        urgency = 78
    elif any(w in text_lower for w in ["poor", "insufficient", "leaking"]):
        urgency = 65
    
    # Affected population estimate (heuristic)
    pop = 1500
    if category == "healthcare":
        pop = np.random.randint(4000, 12000)
    elif category == "road":
        pop = np.random.randint(2000, 9000)
    elif category == "water":
        pop = np.random.randint(1500, 4000)
    else:
        pop = np.random.randint(1000, 5000)
    
    # Simple location guess from keywords
    location = "Unspecified location"
    if "guntur" in text_lower or "village" in text_lower:
        location = "Village cluster, Guntur"
    elif "nagpur" in text_lower or "colony" in text_lower or "ward" in text_lower:
        location = "Residential area, Nagpur"
    elif "sitapur" in text_lower or "phc" in text_lower or "health" in text_lower:
        location = "Primary Health Centre area, Sitapur"
    elif "indore" in text_lower or "market" in text_lower:
        location = "Market / ward area, Indore"
    
    issue_map = {
        "road": "Road / connectivity issue",
        "water": "Water supply / pipeline issue",
        "healthcare": "Healthcare access issue",
        "sanitation": "Sanitation / civic amenity issue",
        "education": "Education infrastructure issue",
        "digital": "Digital connectivity issue",
    }
    
    return {
        "category": category,
        "issue": issue_map.get(category, "General civic issue"),
        "location": location,
        "urgency": urgency,
        "affected_population": pop,
        "confidence": round(np.random.uniform(0.78, 0.96), 2),
    }

def compute_priority(demand: float, infra_score: float, pop_impact: float, urgency: float, invest_gap: float) -> float:
    """Weighted priority score (0-100)."""
    # Invert infra_score (low score = high deficit)
    deficit = 100 - infra_score
    score = (
        0.30 * demand +
        0.25 * deficit +
        0.20 * pop_impact +
        0.15 * urgency +
        0.10 * invest_gap
    )
    return round(min(100, max(0, score)), 1)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📡 BRICS CivicPulse")
    st.caption("From Citizen Voice to Development Action")
    st.markdown("---")
    
    page = st.radio(
        "Navigate",
        ["🏠 Overview", "📝 Citizen Report", "🧠 Request Intelligence", 
         "🗺️ Hotspot Map", "📋 Recommendations", "📈 Impact Measurement"],
        label_visibility="collapsed",
    )
    
    st.markdown("---")
    st.markdown("**Pilot Focus:** India")
    st.markdown("**Languages:** EN · HI · TE (mock)")
    st.markdown("**Status:** Prototype Demo")
    st.caption("Synthetic data for demonstration only.")

# ---------------------------------------------------------------------------
# PAGE: Overview
# ---------------------------------------------------------------------------
if page == "🏠 Overview":
    st.title("BRICS CivicPulse")
    st.markdown("#### AI-powered civic intelligence for evidence-backed development planning")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Citizen Requests", f"{len(requests_df):,}")
    with col2:
        st.metric("Development Clusters", requests_df["cluster_id"].nunique())
    with col3:
        st.metric("High-Priority Gaps", "4")
    with col4:
        st.metric("Pop. Potentially Affected", "28,000+")
    
    st.markdown("---")
    
    st.markdown("### The Alignment Layer")
    st.info(
        "**Citizen Demand + Demographic Need + Infrastructure Deficit + Investment Gap "
        "= Evidence-backed Development Intelligence**"
    )
    
    st.markdown("### End-to-End Flow")
    flow_cols = st.columns(7)
    labels = ["Citizen\nInput", "AI\nGateway", "Request\nIntel", "Data\nFusion", 
              "Hotspot &\nPriority", "Policy\nRecommend", "Impact\nMeasure"]
    for i, (c, lab) in enumerate(zip(flow_cols, labels)):
        with c:
            color = "#FF6B4A" if i == 6 else "#1B2A4A"
            st.markdown(
                f"<div style='background:{color};color:white;padding:12px 4px;"
                f"border-radius:8px;text-align:center;font-size:12px;font-weight:600;"
                f"min-height:70px;display:flex;align-items:center;justify-content:center;'>"
                f"{lab.replace(chr(10),'<br>')}</div>",
                unsafe_allow_html=True,
            )
    
    st.markdown("---")
    st.markdown("### Sample Hotspot Snapshot")
    st.markdown(
        """
        **Rural Road Connectivity – Guntur, Andhra Pradesh**  
        - 10+ related citizen reports clustered  
        - ~8,500 affected residents across linked villages  
        - Infrastructure score: **28 / 100** (severe deficit)  
        - Matching investment plan: **None for village roads**  
        - Prototype Priority Score: **88 / 100**
        """
    )

# ---------------------------------------------------------------------------
# PAGE: Citizen Report
# ---------------------------------------------------------------------------
elif page == "📝 Citizen Report":
    st.title("Multilingual Citizen Gateway")
    st.caption("Report a development issue via text (voice input simulated)")
    
    col_l, col_r = st.columns([1.2, 1])
    
    with col_l:
        language = st.selectbox("Language", ["English", "Hindi", "Telugu"], index=0)
        input_mode = st.radio("Input mode", ["Text", "Mock Voice"], horizontal=True)
        
        if input_mode == "Text":
            user_text = st.text_area(
                "Describe the issue",
                height=140,
                placeholder="Example: The road to our village becomes unusable during monsoon. Ambulances cannot reach us.",
            )
        else:
            st.info("🎤 Mock voice input active. In production this uses Whisper / Indic STT models.")
            user_text = st.text_area(
                "Transcribed text (simulated)",
                value="Our village road becomes completely unusable during the monsoon. School buses and ambulances cannot reach us.",
                height=120,
            )
        
        submit = st.button("Submit Report →", type="primary", use_container_width=True)
    
    with col_r:
        st.markdown("#### AI Extraction Preview")
        if submit and user_text.strip():
            result = extract_entities(user_text, language)
            st.success("Structured development request generated")
            st.json({
                "language": language[:2].lower(),
                "category": result["category"],
                "issue": result["issue"],
                "location": result["location"],
                "urgency": result["urgency"],
                "affected_population": result["affected_population"],
                "extraction_confidence": result["confidence"],
                "source": "citizen_" + ("voice" if input_mode == "Mock Voice" else "text"),
            })
            st.session_state["last_extraction"] = result
        else:
            st.markdown(
                "<div style='background:white;padding:1.5rem;border-radius:10px;"
                "border:1px dashed #CBD5E1;text-align:center;color:#94A3B8;'>"
                "Submit a report to see AI extraction</div>",
                unsafe_allow_html=True,
            )
    
    st.markdown("---")
    st.markdown("### Recent Sample Reports (from seed data)")
    display_cols = ["request_id", "language", "category", "issue", "district", "urgency", "affected_population"]
    st.dataframe(
        requests_df[display_cols].head(8),
        use_container_width=True,
        hide_index=True,
    )

# ---------------------------------------------------------------------------
# PAGE: Request Intelligence
# ---------------------------------------------------------------------------
elif page == "🧠 Request Intelligence":
    st.title("AI Request Intelligence")
    st.caption("Deduplication · Semantic clustering · Category distribution")
    
    # Category distribution
    cat_counts = requests_df["category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        fig = px.bar(
            cat_counts, x="Category", y="Count",
            color="Count", color_continuous_scale=["#1B2A4A", "#00A8A8", "#FF6B4A"],
            title="Requests by Infrastructure Category",
        )
        fig.update_layout(showlegend=False, height=320, margin=dict(t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Cluster Summary")
        cluster_summary = (
            requests_df.groupby("cluster_id")
            .agg(
                reports=("request_id", "count"),
                category=("category", "first"),
                district=("district", "first"),
                avg_urgency=("urgency", "mean"),
                total_affected=("affected_population", "sum"),
            )
            .reset_index()
            .sort_values("reports", ascending=False)
        )
        cluster_summary["avg_urgency"] = cluster_summary["avg_urgency"].round(0).astype(int)
        st.dataframe(cluster_summary, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("#### Sample Cluster Detail – C1 (Road Connectivity, Guntur)")
    c1 = requests_df[requests_df["cluster_id"] == "C1"][
        ["request_id", "language", "text", "urgency", "affected_population"]
    ]
    st.dataframe(c1, use_container_width=True, hide_index=True)
    
    st.info(
        f"**Cluster C1** contains {len(c1)} related reports. "
        "Semantic similarity + location proximity grouped them into one development hotspot."
    )

# ---------------------------------------------------------------------------
# PAGE: Hotspot Map
# ---------------------------------------------------------------------------
elif page == "🗺️ Hotspot Map":
    st.title("Development Hotspot Map")
    st.caption("Citizen demand density + infrastructure gaps (India pilot sample)")
    
    # Aggregate by district + category for map points
    hotspots = (
        requests_df.groupby(["district", "state", "category", "cluster_id"])
        .agg(
            reports=("request_id", "count"),
            avg_urgency=("urgency", "mean"),
            total_affected=("affected_population", "sum"),
            lat=("latitude", "mean"),
            lon=("longitude", "mean"),
        )
        .reset_index()
    )
    
    # Merge infrastructure scores
    hotspots = hotspots.merge(
        infra_df[["district", "category", "infrastructure_score"]],
        on=["district", "category"],
        how="left",
    )
    hotspots["infrastructure_score"] = hotspots["infrastructure_score"].fillna(50)
    
    # Priority score
    hotspots["demand_norm"] = (hotspots["reports"] / hotspots["reports"].max() * 100).round(1)
    hotspots["pop_norm"] = (hotspots["total_affected"] / hotspots["total_affected"].max() * 100).round(1)
    hotspots["invest_gap"] = 100  # simplified: assume gap for demo
    hotspots["priority"] = hotspots.apply(
        lambda r: compute_priority(
            r["demand_norm"], r["infrastructure_score"],
            r["pop_norm"], r["avg_urgency"], r["invest_gap"]
        ),
        axis=1,
    )
    
    # Map
    m = folium.Map(location=[22.5, 78.5], zoom_start=5, tiles="CartoDB positron")
    
    for _, row in hotspots.iterrows():
        color = "#FF6B4A" if row["priority"] >= 80 else ("#00A8A8" if row["priority"] >= 65 else "#1B2A4A")
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=10 + row["reports"] * 1.5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            popup=folium.Popup(
                f"<b>{row['district']}, {row['state']}</b><br>"
                f"Category: {row['category']}<br>"
                f"Reports: {row['reports']}<br>"
                f"Affected: {int(row['total_affected']):,}<br>"
                f"Infra score: {int(row['infrastructure_score'])}<br>"
                f"<b>Priority: {row['priority']}</b>",
                max_width=250,
            ),
        ).add_to(m)
    
    st_folium(m, width=None, height=420, returned_objects=[])
    
    st.markdown("**Legend:** 🔴 High priority (≥80) &nbsp; 🟢 Medium (65–79) &nbsp; 🔵 Lower")
    
    st.markdown("---")
    st.markdown("#### Hotspot Ranking")
    rank_df = hotspots[
        ["district", "state", "category", "reports", "total_affected",
         "infrastructure_score", "priority"]
    ].sort_values("priority", ascending=False)
    rank_df.columns = ["District", "State", "Category", "Reports", 
                       "Affected Pop.", "Infra Score", "Priority Score"]
    st.dataframe(rank_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# PAGE: Recommendations
# ---------------------------------------------------------------------------
elif page == "📋 Recommendations":
    st.title("Policy Recommendation Engine")
    st.caption("Evidence-backed development priorities for policymaker review")
    
    # Build recommendation cards from top clusters
    top_clusters = (
        requests_df.groupby("cluster_id")
        .agg(
            reports=("request_id", "count"),
            category=("category", "first"),
            district=("district", "first"),
            state=("state", "first"),
            avg_urgency=("urgency", "mean"),
            total_affected=("affected_population", "sum"),
        )
        .reset_index()
        .sort_values("reports", ascending=False)
    )
    
    # Attach infra + investment info
    recommendations = []
    for _, row in top_clusters.iterrows():
        infra_row = infra_df[
            (infra_df["district"] == row["district"]) & 
            (infra_df["category"] == row["category"])
        ]
        infra_score = int(infra_row["infrastructure_score"].values[0]) if len(infra_row) else 50
        
        inv_match = invest_df[
            (invest_df["district"] == row["district"]) & 
            (invest_df["category"] == row["category"])
        ]
        if len(inv_match) == 0:
            invest_status = "No matching project identified"
            invest_gap = 100
        else:
            invest_status = f"{inv_match.iloc[0]['status'].title()} – {inv_match.iloc[0]['notes']}"
            invest_gap = 40 if inv_match.iloc[0]["status"] == "planned" else 20
        
        demand = min(100, row["reports"] * 12)
        pop_impact = min(100, row["total_affected"] / 150)
        priority = compute_priority(demand, infra_score, pop_impact, row["avg_urgency"], invest_gap)
        
        recommendations.append({
            "cluster": row["cluster_id"],
            "category": row["category"].title(),
            "location": f"{row['district']}, {row['state']}",
            "reports": int(row["reports"]),
            "affected": int(row["total_affected"]),
            "infra_score": infra_score,
            "invest_status": invest_status,
            "priority": priority,
            "confidence": round(np.random.uniform(0.82, 0.95), 2),
        })
    
    recommendations = sorted(recommendations, key=lambda x: x["priority"], reverse=True)
    
    for i, rec in enumerate(recommendations[:5]):
        with st.container():
            st.markdown(
                f"""
                <div class="evidence-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <h3 style="margin:0;color:#1B2A4A;">{rec['category']} – {rec['location']}</h3>
                        <span class="priority-high" style="font-size:1.4rem;">{rec['priority']} / 100</span>
                    </div>
                    <hr style="border:none;border-top:1px solid #E2E8F0;margin:12px 0;">
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:0.95rem;">
                        <div><b>Citizen Reports:</b> {rec['reports']}</div>
                        <div><b>Affected Population:</b> {rec['affected']:,}</div>
                        <div><b>Infrastructure Score:</b> {rec['infra_score']} / 100</div>
                        <div><b>Confidence:</b> {rec['confidence']*100:.0f}%</div>
                    </div>
                    <p style="margin-top:12px;"><b>Investment Status:</b> {rec['invest_status']}</p>
                    <p style="margin:8px 0 0;"><b>Recommended Action:</b> Evaluate a targeted 
                    {rec['category'].lower()} intervention in the identified hotspot. 
                    Present evidence to district / state planning authority for human review.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("")  # spacing
    
    st.warning(
        "⚠️ All priority scores are **decision-support indicators**. "
        "Final decisions remain with accountable human policymakers."
    )

# ---------------------------------------------------------------------------
# PAGE: Impact Measurement
# ---------------------------------------------------------------------------
elif page == "📈 Impact Measurement":
    st.title("Impact Measurement")
    st.caption("Did the public investment actually close the original citizen demand gap?")
    
    st.markdown("### Illustrative Before → After Scenario")
    st.markdown("**Intervention:** Rural road connectivity improvement – Guntur cluster (C1)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div style="background:#FFF0ED;padding:1.5rem;border-radius:12px;border-left:5px solid #FF6B4A;">
                <h3 style="color:#FF6B4A;margin-top:0;">BEFORE</h3>
                <ul style="font-size:1.05rem;line-height:1.8;">
                    <li><b>4,820</b> related citizen reports (scaled)</li>
                    <li>Infrastructure access score: <b>28 / 100</b></li>
                    <li>Estimated affected residents: <b>28,000+</b></li>
                    <li>Matching investment: <b>None</b></li>
                    <li>School / health access severely constrained</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            """
            <div style="background:#E0F7F7;padding:1.5rem;border-radius:12px;border-left:5px solid #00A8A8;">
                <h3 style="color:#00A8A8;margin-top:0;">AFTER (simulated 12 months)</h3>
                <ul style="font-size:1.05rem;line-height:1.8;">
                    <li><b>1,100</b> residual reports (−77%)</li>
                    <li>Infrastructure access score: <b>71 / 100</b></li>
                    <li>Population with improved access: <b>~24,000</b></li>
                    <li>Project status: <b>Completed</b></li>
                    <li>Measurable reduction in service-access gap</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("---")
    
    # Simple trend chart
    months = ["Month 0", "M3", "M6", "M9", "M12"]
    complaints = [4820, 3900, 2600, 1700, 1100]
    access = [28, 35, 48, 62, 71]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, y=complaints, name="Citizen Reports",
        line=dict(color="#FF6B4A", width=3), mode="lines+markers",
    ))
    fig.add_trace(go.Scatter(
        x=months, y=access, name="Infrastructure Score",
        line=dict(color="#00A8A8", width=3), mode="lines+markers", yaxis="y2",
    ))
    fig.update_layout(
        title="Projected Impact Trajectory (Illustrative)",
        yaxis=dict(title="Citizen Reports", color="#FF6B4A"),
        yaxis2=dict(title="Infra Score", overlaying="y", side="right", color="#00A8A8", range=[0, 100]),
        height=360,
        legend=dict(orientation="h", y=1.12),
        margin=dict(t=60),
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.success(
        "✅ **Closed-loop intelligence:** CivicPulse links the original citizen demand "
        "to the intervention and quantifies whether the gap was actually reduced."
    )
    
    st.markdown("---")
    st.markdown("### Prototype Limitations (Transparency)")
    st.markdown(
        """
        - All citizen reports and impact numbers in this demo are **synthetic / illustrative**.  
        - Priority scores are **decision-support indicators**, not automatic decisions.  
        - Production use requires validated government datasets and institutional agreements.  
        - AI recommendations always require **human policymaker review**.
        """
    )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "BRICS CivicPulse Prototype  ·  Track 1 – AI for Digital Public Infrastructure & Governance  ·  "
    "India Pilot → BRICS Scale  ·  Synthetic data for demonstration only"
)
