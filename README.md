🎯## What This Project Does
This pipeline takes raw e-commerce data (customers, sales, products) and:

Cleans messy data (dates, duplicates, typos, missing values)

Combines 12+ product files into one master catalog

Joins everything into a single master dataset

Analyzes 5 key business questions

Visualizes insights with professional charts

Generates actionable recommendations

Creates stakeholder-ready reports

One command. Complete analysis. Zero manual work.

# Question                                                #What We Found 

**When should we staff our warehouse?**                          Peak: 12-4PM, Low: 1-5AM → Save $54K/year 
 **Which customer segment is most profitable?**                    Corporate customers = highest margin 
**Is our referral program worth it?**                                         272% higher order value from referred customers 
**How does Black Friday perform?**                                          70% higher average order vs normal days 
**Which region should we focus on?**                                       West region = $845K profit (top performer) 

Ecommerce_Analysis_2025/Project Pipeline
│
├── data/
│ ├── raw/ # Original files (DO NOT EDIT)
│ │ ├── buyers.csv
│ │ ├── sales.csv
│ │ └── products/ # 12 product CSV files
│ ├── interim/ # Cleaned individual files
│ └── processed/ # master_sales_data.csv

## Step 1: Data Cleaning
Each raw file gets cleaned:

clean_buyers.py - Fixes customer data
clean_sales.py - Fixes dates, quantities, typos
clean_products.py - Combines 12 files, cleans prices


├── src/ # All Python code
│ ├── data/ # Cleaning scripts
│ ├── analysis/ # Business analysis
│ ├── visualization/ # Chart generation
│ ├── recommendations/ # Strategic insights
│ └── reports/ # Report generator

## Step 2: Data Integration
join.py merges all data into one master file (352K rows)

Step 3: Analysis
analysis.py calculates revenue, profit, margins, and answers business questions

## Step 4: Recommendations
recommender.py turns insights into action:
── templates/ # Report templates
├── reports/ # Generated outputs
├── main.py # Run everything
└── requirements.txt

Step 5: Reports 📝
generate_reports.py creates executive summaries, stakeholder reports, and action plans

# E-commerce Analytics Pipeline 2026

A complete data pipeline that transforms raw e-commerce data into strategic business insights. From messy CSV files to boardroom-ready recommendations in one command.

---

## 🎯 What It Does

- **Cleans** messy data (dates, duplicates, typos, missing values)
- **Combines** 12+ product files into one master catalog
- **Joins** everything into a single master dataset
- **Answers** 5 key business questions
- **Generates** actionable recommendations
- **Creates** stakeholder-ready reports

**One command. Complete analysis. Zero manual work.**

---

## 📊 Key Findings





## FINANCIAL METRICS
   • Total Revenue: $8.2M
   • Total Profit: $2.1M
   • Avg Order Value: $22
   • Total Orders: 352K

## REFERRAL PROGRAM (YOUR BIGGEST WIN!)
   • Referred customers: $67/order
   • Non-referred: $18/order
   • 272% HIGHER value!

## BLACK FRIDAY
   • BF orders: $60/order
   • Normal days: $22/order
   • 70% higher average order

##STAFFING OPTIMIZATION
   • Low volume hours: 1AM, 2AM, 3AM, 4AM, 5AM
   • Potential savings: $54,750/year

## REGIONAL PERFORMANCE
   • Best region: West ($845K profit)
   • Best segment: Corporate customers
