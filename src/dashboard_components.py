import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_enhanced_dashboard(df: pd.DataFrame) -> go.Figure:
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


def create_dashboard(df: pd.DataFrame) -> go.Figure:
    """Create dashboard with multiple visualizations"""
    print("🔄 Creating dashboard visualizations...")

    # Define months for ordering
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

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

    # Update x-axis labels
    fig.update_xaxes(tickangle=45, row=1, col=1)
    fig.update_xaxes(tickangle=45, row=1, col=2)
    fig.update_xaxes(tickangle=45, row=1, col=3)
    fig.update_xaxes(tickangle=45, row=2, col=2)

    return fig