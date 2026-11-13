import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Online Retail II Dashboard", page_icon="🛒", layout="wide")


@st.cache_data
def load(name):
    return pd.read_csv(f"{name}.csv")


monthly = load("monthly_revenue")
dow = load("dow_revenue")
hourly = load("hourly_revenue")
top_rev = load("top_products_revenue")
top_qty = load("top_products_quantity")
pareto = load("pareto")
cust = load("customer_summary")

st.title("🛒 Online Retail II — Sales Dashboard")
st.caption("DIG Framework mini project · Practice/learning project (Dec 2009 – Dec 2010), not for a real company")

# ---- KPIs ----
total_cust = int(cust["Customers"].sum())
repeat = cust[cust["CustomerType"] == "Repeat"].iloc[0]
cut = pareto[pareto["ProductRankPct"] <= 20]["CumulativeRevenuePct"].max()
peak = monthly.loc[monthly["Revenue"].idxmax()]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Top 20% products → revenue", f"{cut:.0f}%")
k2.metric("Repeat customers", f"{repeat['Customers'] / total_cust:.0%}")
k3.metric("Repeat revenue share", f"{repeat['TotalSpend'] / cust['TotalSpend'].sum():.0%}")
k4.metric("Peak month", f"{peak['YearMonth']}")

tab1, tab2, tab3 = st.tabs(["📈 Sales Trends", "📦 Products", "👥 Customers"])

with tab1:
    st.subheader("Monthly Revenue (full months only)")
    st.plotly_chart(px.line(monthly, x="YearMonth", y="Revenue", markers=True,
                            labels={"Revenue": "Revenue (£)"}), use_container_width=True)
    st.caption("Dec 2009 and Dec 2010 are partial months, so they are excluded. "
               "Revenue grows from Aug se Nov.")
    a, b = st.columns(2)
    a.subheader("Day of Week")
    a.plotly_chart(px.bar(dow, x="DayOfWeek", y="Revenue", labels={"Revenue": "Revenue (£)"}),
                   use_container_width=True)
    a.caption("Near-zero Saturday revenue is a platform pattern, not customer behaviour.")
    b.subheader("Hour of Day")
    b.plotly_chart(px.bar(hourly, x="Hour", y="Revenue", labels={"Revenue": "Revenue (£)"}),
                   use_container_width=True)

with tab2:
    a, b = st.columns(2)
    a.subheader("Top 10 by Revenue")
    a.plotly_chart(px.bar(top_rev.iloc[::-1], x="TotalRevenue", y="Description", orientation="h",
                          labels={"TotalRevenue": "Revenue (£)"}), use_container_width=True)
    b.subheader("Top 10 by Quantity")
    b.plotly_chart(px.bar(top_qty.iloc[::-1], x="TotalQuantitySold", y="Description", orientation="h",
                          labels={"TotalQuantitySold": "Units sold"}), use_container_width=True)
    common = set(top_rev["Description"].str.strip()) & set(top_qty["Description"].str.strip())
    st.info(f"Only {len(common)} products appear in both top-10 — looking at "
            "volume alone can miss high-revenue products.")

    st.subheader("Revenue Concentration (Pareto)")
    fig = px.line(pareto, x="ProductRankPct", y="CumulativeRevenuePct",
                  labels={"ProductRankPct": "% of products (ranked by revenue)",
                          "CumulativeRevenuePct": "Cumulative % of revenue"})
    fig.add_hline(y=80, line_dash="dash")
    fig.add_vline(x=20, line_dash="dash")
    st.plotly_chart(fig, use_container_width=True)
    st.info(f"The top 20% of products generate about **{cut:.0f}%** of revenue.")

with tab3:
    a, b = st.columns(2)
    a.subheader("Customer Split")
    a.plotly_chart(px.pie(cust, names="CustomerType", values="Customers"), use_container_width=True)
    b.subheader("Revenue by Customer Type")
    b.plotly_chart(px.bar(cust, x="CustomerType", y="TotalSpend", labels={"TotalSpend": "Spend (£)"}),
                   use_container_width=True)
    st.caption("Only rows with a valid Customer ID (~80% of the data) are used.")

st.divider()
st.caption("Source: Online Retail II, UCI Machine Learning Repository · Built with Python, pandas, Streamlit")
