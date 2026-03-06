# E-commerce-Analytics-Pipeline-2026_Mikal
🎯 What This Project Does
This pipeline takes raw e-commerce data (customers, sales, products) and:

Cleans messy data (dates, duplicates, typos, missing values)

Combines 12+ product files into one master catalog

Joins everything into a single master dataset

Analyzes 5 key business questions

Visualizes insights with professional charts

Generates actionable recommendations

Creates stakeholder-ready reports

One command. Complete analysis. Zero manual work.

|Question                                                What We Found 

|When should we staff our warehouse?       Peak: 12-4PM, Low: 1-5AM → Save $54K/year |
 Which customer segment is most profitable?  Corporate customers = highest margin |
|Is our referral program worth it? 272% higher order value from referred customers |
How does Black Friday perform? |70% higher average order vs normal days |
Which region should we focus on? West region = $845K profit (top performer) |

Ecommerce_Analysis_2025/
│
├── data/
│ ├── raw/ # Original files (DO NOT EDIT)
│ │ ├── buyers.csv
│ │ ├── sales.csv
│ │ └── products/ # 12 product CSV files
│ ├── interim/ # Cleaned individual files
│ └── processed/ # master_sales_data.csv
│
├── src/ # All Python code
│ ├── data/ # Cleaning scripts
│ ├── analysis/ # Business analysis
│ ├── visualization/ # Chart generation
│ ├── recommendations/ # Strategic insights
│ └── reports/ # Report generator
│
├── templates/ # Report templates
├── reports/ # Generated outputs
├── main.py # Run everything
└── requirements.txt 
