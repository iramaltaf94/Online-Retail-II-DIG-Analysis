# Online Retail II Data Analysis | DIG Framework

A collaborative team learning project (Jul 2026 – Aug 2026) built on the Online Retail II practice dataset, following the DIG Framework: **Discover → Interpret → Goal-Set**.

**Live Dashboard:** https://iram-retail-dashboard.streamlit.app

> This was a practice/learning project and was not conducted for a real company.

## Team

**Team Members**
- Mr. Hanan Gulzar
- Mr. Shariq Rashid
- Ms. Saher Nabi
- Ms. Tehleel un nisa

**Mentor:** Ms. Suha Vaqar Khan

**Lead Mentor:** Mr. Zuhaib Khaki

---

## What is this project about?

Online Retail II contains real-style sales records from a UK-based online wholesaler that sells gifts and homeware. The goal of this project is to turn those raw transactions into clear findings and measurable business goals.

The main focus is **sales trends and product performance**. A lighter, secondary view looks at **customers** (repeat vs one-time buyers).

## The DIG framework in plain words

| Step | Question it answers | Where to find it in the dashboard |
|---|---|---|
| **Discover** | What does the data show? | Discover tab (charts and numbers) |
| **Interpret** | What do these patterns mean? | Interpret tab |
| **Goal-Set** | What should the business aim for? | Goal-Set tab |

## The dataset

- Source: Online Retail II (UCI Machine Learning Repository), first sheet only
- Period: 1 Dec 2009 to 9 Dec 2010
- Size: 525,461 rows and 8 columns in the raw data
- After cleaning: **502,512 rows**
- The raw dataset is **not** stored in this repository because it is too large

## What was done

1. **Data cleaning:** removed exact duplicates, non-product codes (postage, fees, manual entries), cancellations, stock write-offs and zero-price rows. Rows with a missing Customer ID were kept, because trend and product analysis does not need them.
2. **Feature engineering:** created `Revenue`, date features (year, month, day of week, hour), and summary tables for products, invoices and customers.
3. **Exploratory analysis:** summary statistics, distributions, correlations and country totals.
4. **Discover / Interpret / Goal-Set:** findings, explanations and 10 SMART goals with baselines, illustrative targets and priorities.

## Key findings

- Revenue builds from **August to a November peak**, which fits pre-Christmas ordering.
- Orders follow **business hours** (about 7am to 8pm, peak at noon), typical of wholesale buyers.
- The products that earn the most revenue are **mostly different** from the products that sell the most units (only 3 overlap).
- The **top 20% of products (848 of 4,242) generate about 78% of revenue**.
- **Repeat customers** are 67% of identified customers but generate about **94%** of their revenue.

**Recommended goal:** raise the revenue share of the top 848 products from 78% to an illustrative 80%.

## Dashboard sections

| Tab | What it shows |
|---|---|
| Overview | Project summary, DIG explanation, dataset facts |
| Data Cleaning | Rows removed at each step, with before/after counts |
| Feature Engineering | New columns and summary tables, with samples |
| EDA | Statistics, distributions, correlations, countries |
| Discover | Sales trend, day, hour, top products, Pareto, customers |
| Interpret | What each pattern means |
| Goal-Set | SMART goals, priorities, goal scores, final goal |
| Findings & Recommendations | Key findings and suggested actions |
| Limitations & Tools | What this analysis cannot tell, and tools used |

## Repository files

All files are in the repository root (no folders).

| File | Purpose |
|---|---|
| `DIG_Framework.ipynb` | The full analysis notebook (Google Colab) |
| `app.py` | The Streamlit dashboard |
| `requirements.txt` | Python libraries needed by the dashboard |
| `*.csv` (30 small files) | Summary tables the dashboard reads |
| `README.md` | This file |

The CSV files are small summary tables exported from the notebook. They are what lets the dashboard run without the 500,000-row raw dataset.

## Run the dashboard on your own computer

1. Install Python 3.9 or newer.
2. Download or clone this repository.
3. Open a terminal in the project folder and run:

```
pip install -r requirements.txt
streamlit run app.py
```

## Limitations

- Only one full year of data, so seasonal patterns can be studied but year-over-year growth cannot.
- December 2009 and December 2010 are partial months, so they are left out of trend views.
- About 20% of rows have no Customer ID, so customer findings may not describe all customers.
- There is no cost, product-category, marketing-channel or cancellation-reason data, so profit and cause analysis is not possible.
- All goal targets and timeframes are **illustrative**, not supplied by a business.

## Tools used

Python (pandas, numpy), matplotlib, seaborn, Google Colab, Google Drive, Streamlit, Plotly, GitHub, Streamlit Community Cloud.
