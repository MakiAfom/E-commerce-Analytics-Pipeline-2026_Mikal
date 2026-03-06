"""
STRATEGIC RECOMMENDATIONS - Short & Sweet
"""

import pandas as pd

def get_recommendations(df, insights):
    """Turn insights into actions - 30 lines"""
    recs = []
    
    # 1. Staffing
    if 'staffing' in insights:
        s = insights['staffing']
        if s.get('annual_savings', 0) > 50000:
            recs.append(['🏢 Staffing', 'High', f'Close hours {s.get("low_hours",[])}', 
                        f'${s.get("annual_savings",0):,.0f} savings', 'Next quarter'])
    
    # 2. Referral
    if 'referral' in insights:
        r = insights['referral']
        if r.get('payback', 99) < 6:
            recs.append(['🎯 Marketing', 'High', 'Expand referral program', 
                        f'{r.get("ltv_ratio",1):.1f}x customer value', 'Next 30 days'])
    
    # 3. Region
    if 'region' in df.columns:
        top = df.groupby('region')['profit'].sum().idxmax()
        recs.append(['📍 Geography', 'Medium', f'Focus on {top}', 
                    f'${df.groupby("region")["profit"].sum().max():,.0f} profit', 'Next 6 months'])
    
    # 4. Segment
    if 'customer_segment' in df.columns:
        best = df.groupby('customer_segment')['profit'].sum().idxmax()
        recs.append(['👥 Customers', 'Medium', f'Target {best} segment', 
                    f'{best} = top performer', 'Next quarter'])
    
    # 5. Black Friday
    if 'is_black_friday' in df.columns:
        bf = df[df.is_black_friday].revenue.mean()
        norm = df[~df.is_black_friday].revenue.mean()
        if bf > norm * 1.5:
            recs.append(['🎄 Seasonal', 'High', 'Double BF inventory', 
                        f'{((bf/norm)-1)*100:.0f}% higher orders', 'Q4 2026'])
    
    return pd.DataFrame(recs, columns=['Area','Priority','Recommendation','Impact','Timeline'])

# Usage
df = pd.read_csv("data/processed/master_sales_data.csv")
insights = {
    'staffing': {'annual_savings': 120000, 'low_hours': [1,2,3,4,5]},
    'referral': {'payback': 3.2, 'ltv_ratio': 2.3}
}

recs = get_recommendations(df, insights)
print(recs.to_markdown())
recs.to_excel("reports/excel/recommendations.xlsx", index=False)