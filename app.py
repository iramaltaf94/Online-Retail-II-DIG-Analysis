# ============================================================
# Online Retail II - DIG Framework Dashboard
# Reads small CSV files from the repo root (flat, no data/ folder).
# ============================================================
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Online Retail II - DIG Analysis", page_icon="🛒", layout="wide")


# ---------- Helpers ----------
@st.cache_data
def load(name):
    """Read one CSV from the repo root. Returns an empty table if the file is missing."""
    try:
        return pd.read_csv(f"{name}.csv", dtype={"Customer ID": "string", "StockCode": "string"})
    except FileNotFoundError:
        return pd.DataFrame()


def ok(df, name):
    """Show a friendly warning and return False when a CSV is missing."""
    if df.empty:
        st.warning(f"`{name}.csv` was not found in the repository root.")
        return False
    return True


def table(df):
    st.dataframe(df, use_container_width=True, hide_index=True)


def bullets(items):
    st.markdown("\n".join(f"- {i}" for i in items))


# ---------- Chart styling ----------
PALETTE = ["#2563eb", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#14b8a6", "#ec4899", "#f97316"]
GRADIENT = [[0, "#14b8a6"], [0.25, "#10b981"], [0.5, "#f59e0b"], [0.75, "#f97316"], [1, "#ec4899"]]


def show(fig, **_):
    """Apply one consistent, colorful style to every chart, then display it."""
    fig.update_layout(
        template="plotly_white", colorway=PALETTE, font=dict(size=13),
        title_font=dict(size=16), margin=dict(l=10, r=10, t=50, b=10),
        hoverlabel=dict(font_size=13),
    )
    for tr in fig.data:
        if tr.type == "bar":
            # White outline between bars; a single-series bar chart gets a different colour per bar
            tr.marker.line.color = "white"
            tr.marker.line.width = 1.5
            if tr.marker.color is None and len(fig.data) == 1:
                n = len(tr.x) if tr.x is not None else len(tr.y)
                tr.marker.color = [PALETTE[i % len(PALETTE)] for i in range(n)]
        elif tr.type == "pie":
            tr.hole = 0.45  # donut style
            tr.textinfo = "percent+label"
    st.plotly_chart(fig, use_container_width=True)


def bar3d(labels, values, title, z_title="Revenue (£)", max_ticks=14, tick_len=18,
          colorscale="Turbo", color_by_value=False):
    """Build a real 3D bar chart from boxes (Plotly Mesh3d). Drag to rotate, scroll to zoom.
    Each bar gets its own colour (rainbow by position). Set color_by_value=True to colour by height
    instead (better for histograms with many bars).
    Long labels are shortened on the axis (full text stays in the hover box)."""
    labels = [str(lab) for lab in labels]
    values = [float(v) for v in values]
    w = 0.38  # half the width of one bar
    # 12 triangles = the 6 faces of one box (vertices 0-3 are the base, 4-7 the top)
    faces = [(0, 1, 2), (0, 2, 3), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4),
             (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
    x, y, z, i, j, k, intensity, hover = [], [], [], [], [], [], [], []
    for n, (lab, v) in enumerate(zip(labels, values)):
        x += [n - w, n + w, n + w, n - w] * 2
        y += [-w, -w, w, w] * 2
        z += [0] * 4 + [v] * 4
        base = 8 * n
        i += [base + f[0] for f in faces]
        j += [base + f[1] for f in faces]
        k += [base + f[2] for f in faces]
        intensity += [v if color_by_value else n] * 8
        hover += [f"{lab}<br>{z_title}: {v:,.0f}"] * 8
    fig = go.Figure(go.Mesh3d(
        x=x, y=y, z=z, i=i, j=j, k=k, intensity=intensity, colorscale=colorscale,
        showscale=False, flatshading=True, text=hover, hoverinfo="text",
        lighting=dict(ambient=0.7, diffuse=0.9, specular=0.4, roughness=0.3),
    ))
    # Show at most max_ticks labels so crowded charts (e.g. histograms) stay readable
    step = max(1, -(-len(labels) // max_ticks))
    tick_pos = list(range(0, len(labels), step))
    tick_txt = [labels[p] if len(labels[p]) <= tick_len else labels[p][: tick_len - 1] + "…" for p in tick_pos]
    fig.update_layout(
        title=title, height=460,
        scene=dict(
            xaxis=dict(tickmode="array", tickvals=tick_pos, ticktext=tick_txt, title="", tickangle=-30),
            yaxis=dict(visible=False),
            zaxis=dict(title=z_title),
            aspectmode="manual", aspectratio=dict(x=2.4, y=0.9, z=1.0),
            camera=dict(eye=dict(x=1.5, y=-1.8, z=0.9)),
        ),
    )
    return fig


# ---------- Header and KPIs ----------
st.title("🛒 Online Retail II: DIG Framework Analysis")
st.caption("Discover → Interpret → Goal-Set | UCI Online Retail II, Dec 2009 to Dec 2010")
USE_3D = st.checkbox("Show 3D bar charts (untick for flat charts)", value=True)

kpi_df = load("kpi_summary")
kpi = dict(zip(kpi_df["Metric"], kpi_df["Value"])) if not kpi_df.empty else {}


def kv(key, fmt):
    return fmt(kpi[key]) if key in kpi else "n/a"


c1, c2, c3, c4 = st.columns(4)
c1.metric("Total revenue", kv("Total revenue", lambda v: f"£{v:,.0f}"))
c2.metric("Invoices", kv("Invoices", lambda v: f"{v:,.0f}"))
c3.metric("Identified customers", kv("Identified customers", lambda v: f"{v:,.0f}"))
c4.metric("Products", kv("Products", lambda v: f"{v:,.0f}"))

tabs = st.tabs([
    "Overview", "Data Cleaning", "Feature Engineering", "EDA", "Discover",
    "Interpret", "Goal-Set", "Findings & Recommendations", "Limitations & Tools",
])


# ============================================================
# 1. OVERVIEW
# ============================================================
with tabs[0]:
    st.header("Project overview")
    st.write(
        "This project analyses the Online Retail II dataset, a UK-based online wholesaler of gift and "
        "homeware products. The analysis follows the DIG framework to move from raw transactions to "
        "measurable business goals. The primary focus is sales trends and product performance, with a "
        "lighter secondary view of customers."
    )
    st.subheader("The DIG framework")
    d1, d2, d3 = st.columns(3)
    d1.markdown("**Discover**\n\nDescribe the data: structure, quality, trends, top products and customer split.")
    d2.markdown("**Interpret**\n\nExplain why the patterns appear and what each finding does and does not prove.")
    d3.markdown("**Goal-Set**\n\nTurn supported findings into SMART goals with baselines, targets and priorities.")
    st.subheader("Dataset facts (raw data)")
    facts = load("raw_facts")
    if ok(facts, "raw_facts"):
        table(facts)
    st.info("Only the first sheet of the Excel file was used. The raw dataset is not stored in the repository.")


# ============================================================
# 2. DATA CLEANING
# ============================================================
with tabs[1]:
    st.header("Data cleaning")
    steps = load("cleaning_steps")
    if ok(steps, "cleaning_steps"):
        raw_rows, clean_rows = int(steps["RowsRemaining"].iloc[0]), int(steps["RowsRemaining"].iloc[-1])
        a, b, c = st.columns(3)
        a.metric("Rows before cleaning", f"{raw_rows:,}")
        b.metric("Rows after cleaning", f"{clean_rows:,}")
        c.metric("Rows removed or set aside", f"{raw_rows - clean_rows:,}")
        if USE_3D:
            removed = steps.iloc[1:]  # skip step 0 (the raw dataset removed nothing)
            show(bar3d(["Step " + s for s in removed["Step"]], removed["RowsRemoved"],
                       "Rows removed or set aside at each cleaning step", z_title="Rows"))
        else:
            fig = px.bar(steps, x="Step", y="RowsRemaining", text="RowsRemaining",
                         hover_data=["Action", "RowsRemoved"], title="Rows remaining after each cleaning step")
            fig.update_traces(texttemplate="%{text:,}")
            fig.update_yaxes(range=[480000, 530000])
            show(fig)
            st.caption("The y-axis starts at 480,000 so the small drops stay visible.")
        table(steps)

    st.subheader("What was removed and why")
    bullets([
        "**Exact duplicates:** they inflate every count and total without adding information.",
        "**Non-product StockCodes** (postage, fees, discounts, manual entries): not product sales.",
        "**Cancellations** (invoices starting with C): set aside so gross sales are not distorted.",
        "**Non-C negative quantities:** a separate group, likely stock write-offs, not customer cancellations.",
        "**Zero-price rows:** samples, giveaways or stock movements with no revenue.",
        "**Missing Customer ID (about 20%):** kept, because trend and product analysis does not need it. "
        "These rows are excluded only from the customer view.",
        "**Real products with unusual codes** (PADS, DCGSSGIRL, DCGSSBOY, DCGSLBOY, DCGSLGIRL) were kept after manual review.",
    ])

    left, right = st.columns(2)
    with left:
        st.subheader("Data set aside")
        side = load("side_datasets")
        if ok(side, "side_datasets"):
            table(side)
    with right:
        st.subheader("Missing values in the raw data")
        miss = load("missing_raw")
        if ok(miss, "missing_raw"):
            m = miss[miss["Missing"] > 0]
            if USE_3D:
                show(bar3d(m["Column"], m["Missing"], "Missing values (raw data)", z_title="Missing rows"))
            else:
                fig = px.bar(m, x="Column", y="Missing", text="MissingPct")
                fig.update_traces(texttemplate="%{text}%")
                show(fig)

    st.subheader("Non-product StockCodes that were excluded")
    npc = load("non_product_codes")
    if ok(npc, "non_product_codes"):
        table(npc)


# ============================================================
# 3. FEATURE ENGINEERING
# ============================================================
with tabs[2]:
    st.header("Feature engineering")
    st.write("New columns and aggregates were created at four levels: row, date, product, invoice and customer.")
    feats = load("features_catalog")
    if ok(feats, "features_catalog"):
        table(feats)
    st.subheader("Sample of the clean data with new features")
    s = load("sample_clean_rows")
    if ok(s, "sample_clean_rows"):
        table(s)
    st.subheader("Product aggregate (top 10 by revenue)")
    s = load("sample_product_agg")
    if ok(s, "sample_product_agg"):
        table(s)
    left, right = st.columns(2)
    with left:
        st.subheader("Invoice aggregate (sample)")
        s = load("sample_invoice_agg")
        if ok(s, "sample_invoice_agg"):
            table(s)
    with right:
        st.subheader("Customer aggregate (sample)")
        s = load("sample_customer_agg")
        if ok(s, "sample_customer_agg"):
            table(s)
    st.caption(
        "The customer aggregate uses only rows with a valid Customer ID. A full RFM segmentation was "
        "considered and deliberately left out to keep the customer view simple."
    )


# ============================================================
# 4. EDA
# ============================================================
with tabs[3]:
    st.header("Exploratory data analysis")
    st.subheader("Summary statistics (clean data)")
    ns = load("numeric_summary")
    if ok(ns, "numeric_summary"):
        table(ns)
    st.subheader("Invoice-level statistics")
    inv = load("invoice_summary")
    if ok(inv, "invoice_summary"):
        table(inv)

    st.subheader("Distributions")
    st.caption("Values above the 99th percentile are hidden so the main shape stays readable. All three are right-skewed.")
    h1, h2, h3 = st.columns(3)
    for col, name, label, cs in [(h1, "hist_quantity", "Quantity per row", "Plasma"),
                                 (h2, "hist_price", "Price per unit (£)", "Viridis"),
                                 (h3, "hist_invoice_total", "Invoice total (£)", "Turbo")]:
        with col:
            h = load(name)
            if ok(h, name):
                h["BinMid"] = (h["BinStart"] + h["BinEnd"]) / 2
                if USE_3D:
                    # Histograms have many bars, so colour by height with a different theme each
                    show(bar3d(h["BinMid"].round(1), h["Count"], label, z_title="Count", max_ticks=6,
                               colorscale=cs, color_by_value=True))
                else:
                    fig = px.bar(h, x="BinMid", y="Count", title=label)
                    fig.update_layout(xaxis_title=label, bargap=0.05)
                    show(fig)

    st.subheader("Correlations")
    k1, k2 = st.columns(2)
    for col, name, label in [(k1, "correlation", "Row level"), (k2, "product_correlation", "Product level")]:
        with col:
            cdf = load(name)
            if ok(cdf, name):
                fig = px.imshow(cdf.set_index("Variable"), text_auto=True, zmin=-1, zmax=1,
                                color_continuous_scale="RdBu_r", title=label)
                show(fig, use_container_width=True)

    st.subheader("Revenue by country (top 10)")
    ctry = load("country_revenue")
    if ok(ctry, "country_revenue"):
        if USE_3D:
            show(bar3d(ctry["Country"], ctry["Revenue"], "Revenue by country (top 10)", tick_len=12))
        else:
            show(px.bar(ctry.sort_values("Revenue"), x="Revenue", y="Country", orientation="h"))
        st.caption("Descriptive only. Country-level causes were not investigated in the notebook.")


# ============================================================
# 5. DISCOVER
# ============================================================
with tabs[4]:
    st.header("Discover: what does the data show?")

    st.subheader("Sales trends")
    monthly = load("monthly_revenue")
    if USE_3D and not monthly.empty:
        show(bar3d(monthly["YearMonth"], monthly["Revenue"], "Monthly revenue (full months only, Jan-Nov 2010)"))
    elif ok(monthly, "monthly_revenue"):
        show(px.line(monthly, x="YearMonth", y="Revenue", markers=True,
                     title="Monthly revenue (full months only, Jan-Nov 2010)"),
             use_container_width=True)
    monthly_all = load("monthly_revenue_all")
    if not monthly_all.empty:
        with st.expander("Show all months including the two partial months"):
            show(px.bar(monthly_all, x="YearMonth", y="Revenue", color="MonthType"),
                 use_container_width=True)

    left, right = st.columns(2)
    with left:
        dow = load("dow_revenue")
        if USE_3D and not dow.empty:
            show(bar3d(dow["DayOfWeek"], dow["Revenue"], "Revenue by day of week"))
        elif ok(dow, "dow_revenue"):
            show(px.bar(dow, x="DayOfWeek", y="Revenue", title="Revenue by day of week"),
                 use_container_width=True)
    with right:
        hourly = load("hourly_revenue")
        if USE_3D and not hourly.empty:
            show(bar3d(hourly["Hour"], hourly["Revenue"], "Revenue by hour of day"))
        elif ok(hourly, "hourly_revenue"):
            show(px.bar(hourly, x="Hour", y="Revenue", title="Revenue by hour of day"),
                 use_container_width=True)

    st.subheader("Product performance")
    left, right = st.columns(2)
    with left:
        tr = load("top_products_revenue")
        if ok(tr, "top_products_revenue"):
            if USE_3D:
                show(bar3d(tr["Description"], tr["TotalRevenue"], "Top 10 products by revenue", tick_len=14))
            else:
                show(px.bar(tr.sort_values("TotalRevenue"), x="TotalRevenue", y="Description",
                            orientation="h", title="Top 10 products by revenue"))
    with right:
        tq = load("top_products_quantity")
        if ok(tq, "top_products_quantity"):
            if USE_3D:
                show(bar3d(tq["Description"], tq["TotalQuantitySold"], "Top 10 products by units sold",
                           z_title="Units sold", tick_len=14))
            else:
                show(px.bar(tq.sort_values("TotalQuantitySold"), x="TotalQuantitySold", y="Description",
                            orientation="h", title="Top 10 products by units sold"))

    pareto = load("pareto")
    if ok(pareto, "pareto"):
        fig = px.line(pareto, x="ProductRankPct", y="CumulativeRevenuePct",
                      title="Revenue concentration across products")
        fig.add_hline(y=80, line_dash="dash", line_color="red")
        fig.add_vline(x=20, line_dash="dash", line_color="gray")
        fig.update_layout(xaxis_title="% of products (ranked by revenue)", yaxis_title="Cumulative % of revenue")
        show(fig, use_container_width=True)

    st.subheader("Customer view (customers with a valid ID only)")
    cust = load("customer_summary")
    if ok(cust, "customer_summary"):
        left, right = st.columns(2)
        with left:
            show(px.pie(cust, names="CustomerType", values="Customers",
                        title="Customers: repeat vs one-time"), use_container_width=True)
        with right:
            if USE_3D:
                show(bar3d(cust["CustomerType"], cust["TotalSpend"], "Total spend: repeat vs one-time",
                           z_title="Total spend (£)"))
            else:
                show(px.bar(cust, x="CustomerType", y="TotalSpend", title="Total spend: repeat vs one-time"))
    detail = load("customer_detail")
    if not detail.empty:
        table(detail)


# ============================================================
# 6. INTERPRET
# ============================================================
with tabs[5]:
    st.header("Interpret: what do the patterns mean?")
    st.subheader("Data quality")
    bullets([
        "Negative quantity does not always mean a cancellation: 2,119 rows were negative without a C invoice, "
        "so they were treated as a separate group.",
        "Pattern-based filters (short or all-letter StockCodes) needed manual review: five real products "
        "would otherwise have been dropped.",
        "Missing Customer IDs may not be random, so customer findings may not describe the whole customer base.",
    ])
    st.subheader("Sales trends")
    bullets([
        "**Seasonality:** revenue builds from August and peaks in November 2010, consistent with pre-Christmas "
        "ordering. December was excluded because both December months are partial.",
        "**Day of week:** Monday to Thursday is steady, Thursday peaks, Friday dips and Sunday is strong. "
        "Saturday has only 400 rows because the platform barely processed orders, not because demand was low.",
        "**Hour of day:** activity starts around 7am, peaks at noon and tapers by 8pm, which points to "
        "business-hours B2B ordering rather than consumer shopping.",
    ])
    st.subheader("Products")
    bullets([
        "Only 3 products appear in both the top-10 revenue and top-10 quantity lists. Cheap bulk items drive "
        "volume, while higher-priced items drive revenue, so volume alone would misidentify the products that matter.",
        "The top 20% of products (848 of 4,242) generate about 78% of revenue, close to a classic 80/20 split.",
    ])
    st.subheader("Customers")
    bullets([
        "Repeat customers are 67% of identified customers (2,873 of 4,285) but generate about 94% of "
        "their revenue (£8.14M of £8.64M).",
        "**Cross-cutting theme:** revenue is concentrated in a minority of products and a minority of customers.",
    ])


# ============================================================
# 7. GOAL-SET
# ============================================================
with tabs[6]:
    st.header("Goal-Set: from findings to SMART goals")
    st.info(
        "The dataset has no business targets, budgets or timelines, so all target values and timeframes "
        "are illustrative. Baselines come directly from the notebook outputs."
    )
    goals = load("goals")
    if ok(goals, "goals"):
        area = st.selectbox("Filter by area", ["All"] + sorted(goals["Area"].unique()))
        table(goals if area == "All" else goals[goals["Area"] == area])

    st.subheader("Top three quick wins")
    bullets([
        "**ST1:** complete peak-season readiness before August (high impact, medium effort).",
        "**PP3:** prioritise the top 848 products (high impact, medium effort).",
        "**CV2:** grow repeat-customer revenue (high impact, medium effort).",
    ])

    st.subheader("Goal evaluation")
    scores = load("goal_scores")
    if ok(scores, "goal_scores"):
        if USE_3D:
            ranked = scores.sort_values("Total", ascending=False)
            show(bar3d(ranked["Goal"], ranked["Total"], "Candidate goal scores (out of 30)",
                       z_title="Score", tick_len=16))
        else:
            show(px.bar(scores.sort_values("Total"), x="Total", y="Goal", orientation="h",
                        title="Candidate goal scores (out of 30)"))
        table(scores)

    st.subheader("Recommended final goal")
    st.success(
        "Increase the revenue contribution of the top 848 products from the historical baseline of 78% to an "
        "illustrative target of 80%, using focused inventory, marketing and sales effort."
    )
    st.write(
        "**Traceability:** the top 848 products (20% of the catalogue) generated 78% of product revenue → "
        "a small group of products drives most revenue and deserves more focus → raise their contribution to 80%. "
        "It scored highest (29 of 30) because it has a clear baseline, an existing metric and depends less on "
        "missing information than the repeat-customer goal."
    )

    st.subheader("Areas where no defensible goal can be set")
    bullets([
        "Year-over-year growth (only one complete year)",
        "Profit or margin (no cost data)",
        "Product-category growth (no category field)",
        "Marketing-channel performance (no channel field)",
        "Cancellation reduction by cause (no reason codes)",
        "Geographic diversification (country causes not investigated)",
        "Cross-category cross-selling (variants of similar products not separated)",
        "Basket size or invoice value (computed but not interpreted)",
    ])


# ============================================================
# 8. FINDINGS & RECOMMENDATIONS
# ============================================================
with tabs[7]:
    st.header("Key findings")
    bullets([
        "Cleaning reduced 525,461 raw rows to 502,512 analysis-ready rows.",
        "Revenue builds from August to a November peak, a seasonal pattern consistent with pre-Christmas ordering.",
        "Ordering follows business hours (7am to 8pm, peak at noon), typical of B2B wholesale.",
        "Revenue leaders and volume leaders are mostly different products (only 3 overlap).",
        "The top 20% of products generate about 78% of revenue.",
        "Repeat customers are 67% of identified customers and generate about 94% of their revenue.",
    ])
    st.header("Recommendations")
    bullets([
        "**Prepare for peak season early:** have stock and order-processing capacity ready by the end of July.",
        "**Focus on the top 848 products:** protect availability and direct marketing toward them.",
        "**Rank products by revenue, not only volume:** Regency Cakestand 3 Tier and White Hanging Heart "
        "T-Light Holder deserve specific attention.",
        "**Invest in repeat customers:** they carry most identifiable revenue, and converting more one-time buyers is valuable.",
        "**Align staffing with ordering hours:** cover 7am to 8pm with the strongest coverage around noon.",
        "**Report Saturday separately** so limited processing is not read as weak demand.",
        "**Improve data capture:** remove duplicates before analysis and reduce missing Customer IDs.",
    ])


# ============================================================
# 9. LIMITATIONS & TOOLS
# ============================================================
with tabs[8]:
    st.header("Limitations")
    bullets([
        "Only one full year is available, so seasonality can be studied but year-over-year growth cannot.",
        "December 2009 and December 2010 are partial months and were excluded from trend views.",
        "About 20% of clean rows have no Customer ID, so customer findings may not generalise.",
        "No cost, category, marketing-channel or cancellation-reason data exists, so profit, category and cause analysis is not possible.",
        "The United Kingdom dominates the data, and country-level performance was not investigated.",
        "Only the first sheet of the Excel file was analysed.",
        "All goal targets and timeframes are illustrative, not business-supplied.",
    ])
    st.header("Tools used")
    bullets([
        "**Python** with pandas and numpy for cleaning and aggregation",
        "**matplotlib and seaborn** for charts in the notebook",
        "**Google Colab and Google Drive** for the notebook environment and data storage",
        "**Streamlit and Plotly** for this dashboard",
        "**GitHub and Streamlit Community Cloud** for hosting and automatic deployment",
    ])
