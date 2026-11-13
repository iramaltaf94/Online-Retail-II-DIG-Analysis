# Online Retail II Data Analysis | DIG Framework

A collaborative **team learning project** (Jul 2026 – Aug 2026) built on the Online Retail II practice dataset, following the **DIG Framework**: Discover → Interpret → Goal-Set.

> This was a practice/learning project and was not conducted for a real company.

## Dataset

- 525,461 transactions, 8 columns (Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country)
- Time range: Dec 2009 – Dec 2010
- After cleaning: 502,512 rows
- - Source: [Online Retail II, UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- Note: the full dataset covers two years (1,067,371 rows). This analysis uses the first year only (Dec 2009 – Dec 2010).
- The dataset file is not included in this repository due to its size.

## Analysis Performed

- **Data cleaning:** removed duplicates, non-product entries (postage, fees, etc.), cancellations, write-offs and zero-price rows
- **Feature engineering:** revenue, date features, and product-, invoice- and customer-level aggregates
- **Sales trend analysis:** monthly, day-of-week and hour-of-day patterns
- **Product performance analysis:** top products by revenue vs. quantity
- **Pareto / revenue concentration analysis**
- **Customer analysis:** repeat vs. one-time buyers

## Key Findings

- The top 20% of products (848 out of 4,242) generated approximately **78%** of total product revenue.
- Revenue builds steadily from August to November, with November the peak full month.
- Orders follow a business-hours pattern: activity starts around 7 AM, peaks at noon and tapers off by 8 PM.
- Only 3 products appear in both the top 10 by revenue and the top 10 by quantity, so volume alone can misidentify the products that matter for revenue.
- Repeat customers are 67% of customers (2,873 of 4,285) but generate about 94% of revenue (£8.14M of £8.64M).
- Across both products and customers, revenue is concentrated in a small share of the total.

## Recommendations

- Inventory prioritization
- Focused sales efforts
- Targeted marketing
- Performance monitoring

## Limitations

- About 20% of rows have no Customer ID, so the customer analysis covers only the rest.
- The data covers roughly one year, so year-over-year trends can't be assessed.

## Tools

Python, pandas, NumPy, Matplotlib, Seaborn (Google Colab)
