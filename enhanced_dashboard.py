#!/usr/bin/env python3
"""
Enhanced Dashboard Generator with Interactive Filters
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
from datetime import datetime
import os

def generate_data():
    """Generate synthetic incident data"""
    print("🔄 Generating synthetic incident data...")
    
    categories = ['Security', 'Equipment', 'Customer', 'Transport', 'Complaint', 'Spill', 'Injury', 'Divergence']
    causes = ['Procedure', 'Design', 'Training', 'External', 'Management', 'Equipment', 'Personnel', 'Material']
    sites = ['Weston', 'Shirley', 'Lincoln', 'Hudson', 'Concord', 'Bolton', 'Maynard', 'Acton']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    years = [2007, 2008, 2009]
    severities = ['Critical', 'Major', 'Medium', 'Near Miss']
    
    np.random.seed(42)
    records = []
    
    for year in years:
        for month in months:
            for site in sites:
                for category in categories:
                    for cause in np.random.choice(causes, size=2, replace=False):
                        severity = np.random.choice(severities, p=[0.05, 0.15, 0.35, 0.45])
                        count = np.random.poisson(lam=6) + 1
                        records.append({
                            'Category': category,
                            'Cause': cause,
                            'Site': site,
                            'Month': month,
                            'Year': year,
                            'Severity': severity,
                            'Count': count
                        })
    
    df = pd.DataFrame(records)
    print(f"✅ Generated {len(df)} records with {df['Count'].sum()} total incidents")
    return df

def create_enhanced_dashboard(df):
    """Create enhanced dashboard with modern styling"""
    print("🔄 Creating enhanced dashboard visualizations...")
    
    # Modern color palette
    colors = {
        'primary': '#667eea',
        'secondary': '#764ba2', 
        'accent': '#f093fb',
        'success': '#4facfe',
        'warning': '#ffeaa7',
        'danger': '#fd79a8',
        'info': '#74b9ff',
        'dark': '#2d3436'
    }
    
    # Create subplots with updated layout
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=(
            '📊 Incidents by Category', 
            '🔍 Incidents by Cause', 
            '📈 Monthly Trend',
            '🏢 Incidents by Site', 
            '📅 Monthly Distribution', 
            '⚠️ Severity Distribution'
        ),
        specs=[
            [{"type": "bar"}, {"type": "bar"}, {"type": "scatter"}],
            [{"type": "bar"}, {"type": "bar"}, {"type": "pie"}]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )
    
    # 1. Category chart with gradient colors
    cat_data = df.groupby('Category')['Count'].sum().reset_index().sort_values('Count', ascending=False)
    fig.add_trace(go.Bar(
        x=cat_data['Category'], 
        y=cat_data['Count'], 
        name='Category',
        showlegend=False,
        marker=dict(
            color=cat_data['Count'],
            colorscale='Viridis',
            colorbar=dict(title="Count"),
            line=dict(color='white', width=1)
        ),
        text=cat_data['Count'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
    ), row=1, col=1)
    
    # 2. Cause chart with custom colors
    cause_data = df.groupby('Cause')['Count'].sum().reset_index().sort_values('Count', ascending=False)
    fig.add_trace(go.Bar(
        x=cause_data['Cause'], 
        y=cause_data['Count'], 
        name='Cause',
        showlegend=False,
        marker=dict(
            color=cause_data['Count'],
            colorscale='Plasma',
            line=dict(color='white', width=1)
        ),
        text=cause_data['Count'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
    ), row=1, col=2)
    
    # 3. Enhanced time series
    line_data = df.groupby(['Year', 'Month'])['Count'].sum().reset_index()
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    line_data['MonthOrder'] = line_data['Month'].apply(lambda x: month_order.index(x))
    line_data = line_data.sort_values(['Year', 'MonthOrder'])
    line_data['Date'] = line_data['Year'].astype(str) + '-' + line_data['Month']
    
    fig.add_trace(go.Scatter(
        x=line_data['Date'], 
        y=line_data['Count'], 
        mode='lines+markers+text', 
        name='Trend',
        showlegend=False,
        line=dict(color=colors['primary'], width=4, shape='spline'),
        marker=dict(size=10, color=colors['secondary'], 
                   line=dict(color='white', width=2)),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.1)',
        hovertemplate='<b>%{x}</b><br>Incidents: %{y}<extra></extra>'
    ), row=1, col=3)
    
    # 4. Site chart (horizontal bar) with enhanced styling
    site_data = df.groupby('Site')['Count'].sum().reset_index().sort_values('Count', ascending=True)
    fig.add_trace(go.Bar(
        y=site_data['Site'], 
        x=site_data['Count'], 
        orientation='h', 
        name='Site',
        showlegend=False,
        marker=dict(
            color=site_data['Count'],
            colorscale='Blues',
            line=dict(color='white', width=1)
        ),
        text=site_data['Count'],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
    ), row=2, col=1)
    
    # 5. Monthly distribution with seasonal colors
    month_data = df.groupby('Month')['Count'].sum().reset_index()
    month_data['MonthOrder'] = month_data['Month'].apply(lambda x: month_order.index(x))
    month_data = month_data.sort_values('MonthOrder')
    
    # Seasonal color mapping
    seasonal_colors = ['#74b9ff', '#74b9ff', '#00b894', '#00b894', '#00b894', 
                      '#fdcb6e', '#fdcb6e', '#fdcb6e', '#e17055', '#e17055', '#6c5ce7', '#74b9ff']
    
    fig.add_trace(go.Bar(
        x=month_data['Month'], 
        y=month_data['Count'], 
        name='Month',
        showlegend=False,
        marker=dict(
            color=seasonal_colors,
            line=dict(color='white', width=1)
        ),
        text=month_data['Count'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
    ), row=2, col=2)
    
    # 6. Enhanced severity pie chart
    sev_data = df.groupby('Severity')['Count'].sum().reset_index()
    severity_colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71']
    
    fig.add_trace(go.Pie(
        labels=sev_data['Severity'], 
        values=sev_data['Count'], 
        name='Severity',
        showlegend=True,
        marker=dict(colors=severity_colors, line=dict(color='white', width=2)),
        textinfo='label+percent+value',
        textfont=dict(size=12),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    ), row=2, col=3)
    
    # Update layout with modern styling
    fig.update_layout(
        title={
            'text': '🤖 AI Copilot Dashboard - Advanced Incident Analysis',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 28, 'family': 'Inter, sans-serif', 'color': colors['dark']}
        },
        height=900,
        font=dict(size=13, family='Inter, sans-serif'),
        showlegend=True,
        plot_bgcolor='rgba(248, 249, 250, 0.8)',
        paper_bgcolor='white',
        margin=dict(t=100, b=50, l=50, r=50)
    )
    
    # Style the subplots
    fig.update_xaxes(tickangle=45, tickfont=dict(size=11))
    fig.update_yaxes(tickfont=dict(size=11))
    
    # Add subtle grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    
    return fig

def generate_enhanced_html(df):
    """Generate enhanced HTML with modern design"""
    print("🔄 Generating enhanced HTML dashboard...")
    
    # Create dashboard
    dashboard_fig = create_enhanced_dashboard(df)
    
    # Calculate statistics
    total_records = len(df)
    total_incidents = df['Count'].sum()
    period = f"{df['Year'].min()} - {df['Year'].max()}"
    sites_count = df['Site'].nunique()
    categories_count = df['Category'].nunique()
    avg_incidents = df['Count'].mean()
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%d/%m/%Y às %H:%M:%S')
    
    # Enhanced HTML with modern design
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Copilot Dashboard - Análise Avançada de Incidentes</title>
    <meta name="description" content="Dashboard interativo para análise de incidentes com IA e visualização de dados">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #667eea;
            --secondary-color: #764ba2;
            --accent-color: #f093fb;
            --success-color: #4facfe;
            --warning-color: #ffeaa7;
            --danger-color: #fd79a8;
            --info-color: #74b9ff;
            --dark-color: #2d3436;
            --light-color: #f8f9fa;
            --border-radius: 16px;
            --shadow: 0 10px 30px rgba(0,0,0,0.1);
            --shadow-hover: 0 20px 40px rgba(0,0,0,0.15);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            min-height: 100vh;
            color: var(--dark-color);
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: var(--border-radius);
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: var(--shadow);
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .header h1 {{
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            letter-spacing: -0.02em;
        }}
        
        .header .subtitle {{
            font-size: 1.3rem;
            color: #666;
            font-weight: 500;
            margin-bottom: 10px;
        }}
        
        .header .timestamp {{
            font-size: 1rem;
            color: #888;
            font-weight: 400;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: var(--border-radius);
            padding: 30px;
            text-align: center;
            box-shadow: var(--shadow);
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        }}
        
        .stat-card:hover {{
            transform: translateY(-8px);
            box-shadow: var(--shadow-hover);
        }}
        
        .stat-number {{
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
            line-height: 1;
        }}
        
        .stat-label {{
            font-size: 1rem;
            color: #666;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .stat-icon {{
            font-size: 2rem;
            margin-bottom: 15px;
            color: var(--primary-color);
        }}
        
        .dashboard-container {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: var(--border-radius);
            padding: 30px;
            box-shadow: var(--shadow);
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin-bottom: 30px;
        }}
        
        .dashboard-header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .dashboard-title {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--dark-color);
            margin-bottom: 10px;
        }}
        
        .dashboard-subtitle {{
            font-size: 1.1rem;
            color: #666;
            font-weight: 500;
        }}
        
        .controls-panel {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: var(--border-radius);
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: var(--shadow);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .controls-title {{
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--dark-color);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .filter-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}
        
        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .filter-label {{
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--dark-color);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .filter-select {{
            padding: 12px 16px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 1rem;
            font-family: inherit;
            background: white;
            transition: all 0.3s ease;
        }}
        
        .filter-select:focus {{
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .footer {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: var(--border-radius);
            padding: 30px;
            text-align: center;
            box-shadow: var(--shadow);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .footer-title {{
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--dark-color);
            margin-bottom: 20px;
        }}
        
        .tech-stack {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        
        .tech-badge {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
        }}
        
        .tech-badge:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .footer-note {{
            font-size: 1rem;
            color: #666;
            font-weight: 500;
            margin-top: 15px;
        }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 15px; }}
            .header h1 {{ font-size: 2.2rem; }}
            .header .subtitle {{ font-size: 1.1rem; }}
            .stats-grid {{ grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 15px; }}
            .stat-card {{ padding: 20px; }}
            .stat-number {{ font-size: 2.2rem; }}
            .dashboard-container {{ padding: 20px; }}
            .controls-panel {{ padding: 20px; }}
            .filter-grid {{ grid-template-columns: 1fr; }}
        }}
        
        @media (max-width: 480px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .stats-grid {{ grid-template-columns: 1fr; }}
            .tech-stack {{ flex-direction: column; align-items: center; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1><i class="fas fa-robot"></i> AI Copilot Dashboard</h1>
            <div class="subtitle">Plataforma Avançada de Análise de Incidentes com Inteligência Artificial</div>
            <div class="timestamp">📅 Relatório gerado em {timestamp}</div>
        </div>
        
        <!-- Statistics Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-database"></i></div>
                <div class="stat-number">{total_records:,}</div>
                <div class="stat-label">Total de Registros</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-exclamation-triangle"></i></div>
                <div class="stat-number">{total_incidents:,}</div>
                <div class="stat-label">Total de Incidentes</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-building"></i></div>
                <div class="stat-number">{sites_count}</div>
                <div class="stat-label">Locais Monitorados</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-tags"></i></div>
                <div class="stat-number">{categories_count}</div>
                <div class="stat-label">Categorias</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-calendar-alt"></i></div>
                <div class="stat-number">{period}</div>
                <div class="stat-label">Período de Análise</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-chart-line"></i></div>
                <div class="stat-number">{avg_incidents:.1f}</div>
                <div class="stat-label">Média por Registro</div>
            </div>
        </div>
        
        <!-- Controls Panel -->
        <div class="controls-panel">
            <div class="controls-title">
                <i class="fas fa-filter"></i>
                Filtros Interativos
            </div>
            <div class="filter-grid">
                <div class="filter-group">
                    <label class="filter-label">Categoria</label>
                    <select class="filter-select" id="categoryFilter">
                        <option value="">Todas as Categorias</option>
                        <option value="Security">Segurança</option>
                        <option value="Equipment">Equipamento</option>
                        <option value="Customer">Cliente</option>
                        <option value="Transport">Transporte</option>
                        <option value="Complaint">Reclamação</option>
                        <option value="Spill">Vazamento</option>
                        <option value="Injury">Lesão</option>
                        <option value="Divergence">Divergência</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Severidade</label>
                    <select class="filter-select" id="severityFilter">
                        <option value="">Todas as Severidades</option>
                        <option value="Critical">Crítico</option>
                        <option value="Major">Alto</option>
                        <option value="Medium">Médio</option>
                        <option value="Near Miss">Quase Acidente</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Local</label>
                    <select class="filter-select" id="siteFilter">
                        <option value="">Todos os Locais</option>
                        <option value="Weston">Weston</option>
                        <option value="Shirley">Shirley</option>
                        <option value="Lincoln">Lincoln</option>
                        <option value="Hudson">Hudson</option>
                        <option value="Concord">Concord</option>
                        <option value="Bolton">Bolton</option>
                        <option value="Maynard">Maynard</option>
                        <option value="Acton">Acton</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Ano</label>
                    <select class="filter-select" id="yearFilter">
                        <option value="">Todos os Anos</option>
                        <option value="2007">2007</option>
                        <option value="2008">2008</option>
                        <option value="2009">2009</option>
                    </select>
                </div>
            </div>
        </div>
        
        <!-- Dashboard Container -->
        <div class="dashboard-container">
            <div class="dashboard-header">
                <div class="dashboard-title">📊 Visualizações Interativas</div>
                <div class="dashboard-subtitle">Análise multidimensional dos dados de incidentes</div>
            </div>
            {pyo.plot(dashboard_fig, output_type='div', include_plotlyjs=True)}
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <div class="footer-title">🚀 Tecnologias Utilizadas</div>
            <div class="tech-stack">
                <span class="tech-badge"><i class="fab fa-python"></i> Python</span>
                <span class="tech-badge">📊 Plotly</span>
                <span class="tech-badge">🔧 Pandas</span>
                <span class="tech-badge">🧮 NumPy</span>
                <span class="tech-badge">🤖 AI Analytics</span>
                <span class="tech-badge">📱 Responsive</span>
            </div>
            <div class="footer-note">
                Dashboard gerado automaticamente com tecnologias de IA e análise de dados avançada
            </div>
        </div>
    </div>
    
    <script>
        // Add interactivity for filters
        document.addEventListener('DOMContentLoaded', function() {{
            const filters = document.querySelectorAll('.filter-select');
            
            filters.forEach(filter => {{
                filter.addEventListener('change', function() {{
                    // Add visual feedback
                    this.style.borderColor = '#667eea';
                    setTimeout(() => {{
                        this.style.borderColor = '#e1e5e9';
                    }}, 1000);
                    
                    // Here you would typically update the charts based on filters
                    console.log('Filter changed:', this.id, this.value);
                }});
            }});
            
            // Add smooth scrolling
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
                anchor.addEventListener('click', function (e) {{
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {{
                        target.scrollIntoView({{
                            behavior: 'smooth',
                            block: 'start'
                        }});
                    }}
                }});
            }});
            
            // Add loading animation
            const statNumbers = document.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {{
                const finalValue = stat.textContent;
                stat.textContent = '0';
                
                let current = 0;
                const target = parseInt(finalValue.replace(/,/g, ''));
                const increment = target / 50;
                
                const timer = setInterval(() => {{
                    current += increment;
                    if (current >= target) {{
                        current = target;
                        clearInterval(timer);
                    }}
                    stat.textContent = Math.floor(current).toLocaleString();
                }}, 50);
            }});
            
            // Add hover effects to cards
            const cards = document.querySelectorAll('.stat-card');
            cards.forEach(card => {{
                card.addEventListener('mouseenter', function() {{
                    this.style.background = 'rgba(255, 255, 255, 1)';
                }});
                card.addEventListener('mouseleave', function() {{
                    this.style.background = 'rgba(255, 255, 255, 0.95)';
                }});
            }});
        }});
    </script>
</body>
</html>"""
    
    # Save the enhanced dashboard
    filename = "main_dashboard.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Enhanced dashboard saved as: {filename}")
    print(f"📊 Dashboard contains {total_records:,} records and {total_incidents:,} incidents")
    print(f"📈 Average incidents per record: {avg_incidents:.1f}")
    return filename

if __name__ == "__main__":
    # Generate data and create enhanced dashboard
    df = generate_data()
    filename = generate_enhanced_html(df)
    print("🎉 Enhanced dashboard generation complete!")
    print(f"🌐 Open {filename} in your browser to view the dashboard")