#!/usr/bin/env python3
"""
Generate static HTML dashboard for GitHub Pages
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
from datetime import datetime
import os

# Generate synthetic data for the dashboard
print("🔄 Generating synthetic data...")

categories = ['Customer', 'Spill', 'Injury', 'Transport', 'Equipment', 'Security', 'Divergence', 'Complaint']
causes = ['Material', 'Procedure', 'Design', 'Training', 'Management', 'External', 'Equipment', 'Personnel']
sites = ['Weston', 'Bolton', 'Shirley', 'Lincoln', 'Maynard', 'Acton', 'Concord', 'Hudson']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
years = [2007, 2008, 2009]
severities = ['Critical', 'Major', 'Medium', 'Near Miss']
status = ['Open', 'Closed']

np.random.seed(42)
records = []
for year in years:
    for month in months:
        for site in sites:
            for category in categories:
                for cause in np.random.choice(causes, size=2, replace=False):
                    severity = np.random.choice(severities)
                    stat = np.random.choice(status, p=[0.3, 0.7])
                    count = np.random.poisson(lam=8)
                    if count == 0:
                        continue
                    records.append({
                        'Category': category,
                        'Cause': cause,
                        'Site': site,
                        'Month': month,
                        'Year': year,
                        'Severity': severity,
                        'Status': stat,
                        'Count': count
                    })

df = pd.DataFrame(records)
print(f"✅ Data generated! Total records: {len(df)}")

def create_dashboard():
    """Create dashboard with multiple visualizations"""
    print("🔄 Creating dashboard visualizations...")
    
    # Create figure with 2x3 subplots
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=(
            'Incidents by Category', 'Incidents by Cause', 'Monthly Trend',
            'Incidents by Site', 'Monthly Distribution', 'Severity Distribution'
        ),
        specs=[
            [{"type": "bar"}, {"type": "bar"}, {"type": "scatter"}],
            [{"type": "bar"}, {"type": "bar"}, {"type": "pie"}]
        ],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # Color palette
    colors = px.colors.qualitative.Plotly
    
    # 1. Category chart
    cat_data = df.groupby('Category')['Count'].sum().reset_index().sort_values('Count', ascending=False)
    fig.add_trace(go.Bar(
        x=cat_data['Category'], 
        y=cat_data['Count'], 
        name='Category',
        showlegend=False,
        marker_color=colors[0]
    ), row=1, col=1)
    
    # 2. Cause chart
    cause_data = df.groupby('Cause')['Count'].sum().reset_index().sort_values('Count', ascending=False)
    fig.add_trace(go.Bar(
        x=cause_data['Cause'], 
        y=cause_data['Count'], 
        name='Cause',
        showlegend=False,
        marker_color=colors[1]
    ), row=1, col=2)
    
    # 3. Time series
    line_data = df.groupby(['Year', 'Month'])['Count'].sum().reset_index()
    line_data['MonthNum'] = line_data['Month'].apply(lambda m: months.index(m))
    line_data = line_data.sort_values(['Year', 'MonthNum'])
    line_data['Date'] = line_data['Year'].astype(str) + '-' + line_data['Month']
    fig.add_trace(go.Scatter(
        x=line_data['Date'], 
        y=line_data['Count'], 
        mode='lines+markers', 
        name='Trend',
        showlegend=False,
        line=dict(color=colors[2], width=3),
        marker=dict(size=8)
    ), row=1, col=3)
    
    # 4. Site chart (horizontal bar)
    site_data = df.groupby('Site')['Count'].sum().reset_index().sort_values('Count', ascending=True)
    fig.add_trace(go.Bar(
        y=site_data['Site'], 
        x=site_data['Count'], 
        orientation='h', 
        name='Site',
        showlegend=False,
        marker_color=colors[3]
    ), row=2, col=1)
    
    # 5. Month distribution
    month_data = df.groupby('Month')['Count'].sum().reset_index()
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_data['MonthOrder'] = month_data['Month'].apply(lambda x: month_order.index(x))
    month_data = month_data.sort_values('MonthOrder')
    fig.add_trace(go.Bar(
        x=month_data['Month'], 
        y=month_data['Count'], 
        name='Month',
        showlegend=False,
        marker_color=colors[4]
    ), row=2, col=2)
    
    # 6. Severity pie chart
    sev_data = df.groupby('Severity')['Count'].sum().reset_index()
    fig.add_trace(go.Pie(
        labels=sev_data['Severity'], 
        values=sev_data['Count'], 
        name='Severity',
        showlegend=True
    ), row=2, col=3)
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'AI Copilot Dashboard - Incident Analysis',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'family': 'Arial, sans-serif'}
        },
        height=800,
        font=dict(size=12, family='Arial, sans-serif'),
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='#f8f9fa'
    )
    
    # Update x-axis labels for category and cause charts
    fig.update_xaxes(tickangle=45, row=1, col=1)
    fig.update_xaxes(tickangle=45, row=1, col=2)
    fig.update_xaxes(tickangle=45, row=1, col=3)
    fig.update_xaxes(tickangle=45, row=2, col=2)
    
    return fig

def generate_html():
    """Generate the complete HTML page"""
    print("🔄 Generating HTML dashboard...")
    
    # Create dashboard
    dashboard_fig = create_dashboard()
    
    # Calculate statistics
    total_records = len(df)
    total_incidents = df['Count'].sum()
    period = f"{df['Year'].min()} - {df['Year'].max()}"
    sites_count = df['Site'].nunique()
    categories_count = df['Category'].nunique()
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%d/%m/%Y at %H:%M:%S')
    
    # Create HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Copilot Dashboard - Incident Analysis</title>
    <meta name="description" content="Interactive dashboard for incident analysis using AI and data visualization">
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 0; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{ 
            text-align: center; 
            background: rgba(255,255,255,0.95); 
            color: #2c3e50; 
            padding: 30px; 
            margin-bottom: 20px; 
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .header p {{
            margin: 10px 0 0 0;
            color: #666;
            font-size: 1.1em;
        }}
        .stats {{ 
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0; 
        }}
        .stat {{ 
            background: rgba(255,255,255,0.95); 
            padding: 25px; 
            border-radius: 15px; 
            text-align: center; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }}
        .stat:hover {{
            transform: translateY(-5px);
        }}
        .number {{ 
            font-size: 2.5em; 
            font-weight: bold; 
            color: #2c3e50; 
            margin: 0;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .label {{ 
            color: #666; 
            font-size: 1em; 
            margin-top: 5px;
            font-weight: 500;
        }}
        .dashboard-container {{
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }}
        .footer p {{
            margin: 0;
            color: #666;
        }}
        .tech-stack {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        .tech-badge {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
        }}
        @media (max-width: 768px) {{
            .container {{ padding: 10px; }}
            .header h1 {{ font-size: 2em; }}
            .stats {{ grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); }}
            .number {{ font-size: 2em; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Copilot Dashboard</h1>
            <p>Advanced Incident Analysis & Data Visualization Platform</p>
            <p style="font-size: 0.9em; color: #888;">Generated on {timestamp}</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="number">{total_records:,}</div>
                <div class="label">Total Records</div>
            </div>
            <div class="stat">
                <div class="number">{total_incidents:,}</div>
                <div class="label">Total Incidents</div>
            </div>
            <div class="stat">
                <div class="number">{sites_count}</div>
                <div class="label">Sites Monitored</div>
            </div>
            <div class="stat">
                <div class="number">{categories_count}</div>
                <div class="label">Categories</div>
            </div>
            <div class="stat">
                <div class="number">{period}</div>
                <div class="label">Analysis Period</div>
            </div>
        </div>
        
        <div class="dashboard-container">
            {pyo.plot(dashboard_fig, output_type='div', include_plotlyjs=True)}
        </div>
        
        <div class="footer">
            <p><strong>🚀 Built with Modern Technologies</strong></p>
            <div class="tech-stack">
                <span class="tech-badge">Python</span>
                <span class="tech-badge">Plotly</span>
                <span class="tech-badge">Dash</span>
                <span class="tech-badge">Pandas</span>
                <span class="tech-badge">NumPy</span>
                <span class="tech-badge">Bootstrap</span>
            </div>
            <p style="margin-top: 15px; font-size: 0.9em;">
                Dashboard automatically generated with AI-powered analytics
            </p>
        </div>
    </div>
</body>
</html>"""
    
    # Save the dashboard
    filename = "dashboard.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Dashboard saved as: {filename}")
    print(f"📊 Dashboard contains {total_records:,} records and {total_incidents:,} incidents")
    return filename

if __name__ == "__main__":
    generate_html()
    print("🎉 Dashboard generation complete!")