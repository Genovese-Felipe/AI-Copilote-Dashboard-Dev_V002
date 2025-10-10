#!/usr/bin/env python3
"""
Generate static HTML dashboard for GitHub Pages
"""
import os
from datetime import datetime
import pandas as pd
import plotly.offline as pyo

from .data_generator import generate_data
from .dashboard_components import create_dashboard


def generate_stats_grid(df: pd.DataFrame) -> str:
    """Generate the HTML for the statistics grid."""
    total_records = len(df)
    total_incidents = df['Count'].sum()
    sites_count = df['Site'].nunique()
    categories_count = df['Category'].nunique()
    period = f"{df['Year'].min()} - {df['Year'].max()}"

    stats = [
        {"label": "Total Records", "value": f"{total_records:,}"},
        {"label": "Total Incidents", "value": f"{total_incidents:,}"},
        {"label": "Sites Monitored", "value": sites_count},
        {"label": "Categories", "value": categories_count},
        {"label": "Analysis Period", "value": period}
    ]

    grid_html = ""
    for stat in stats:
        grid_html += f"""
        <div class="stat">
            <div class="number">{stat['value']}</div>
            <div class="label">{stat['label']}</div>
        </div>
        """
    return grid_html


def generate_footer() -> str:
    """Generate the HTML for the footer."""
    tech_badges = ["Python", "Plotly", "Dash", "Pandas", "NumPy", "Bootstrap"]
    badges_html = "".join([f'<span class="tech-badge">{badge}</span>' for badge in tech_badges])
    return f"""
        <p><strong>🚀 Built with Modern Technologies</strong></p>
        <div class="tech-stack">{badges_html}</div>
        <p style="margin-top: 15px; font-size: 0.9em;">
            Dashboard automatically generated with AI-powered analytics
        </p>
    """


def generate_html(df: pd.DataFrame, template_path: str, output_path: str):
    """Generate the complete HTML page"""
    print("🔄 Generating HTML dashboard...")

    # Create dashboard figure
    dashboard_fig = create_dashboard(df)

    # Read HTML template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Generate dynamic components
    title = "🤖 AI Copilot Dashboard"
    subtitle = "Advanced Incident Analysis & Data Visualization Platform"
    timestamp = datetime.now().strftime('%d/%m/%Y at %H:%M:%S')
    stats_grid = generate_stats_grid(df)
    plotly_graph = pyo.plot(dashboard_fig, output_type='div', include_plotlyjs=True)
    footer = generate_footer()

    # Inject components into the template
    html_content = template.replace("{{title}}", title)
    html_content = html_content.replace("{{subtitle}}", subtitle)
    html_content = html_content.replace("{{timestamp}}", timestamp)
    html_content = html_content.replace("{{stats_grid}}", stats_grid)
    html_content = html_content.replace("{{plotly_graph}}", plotly_graph)
    html_content = html_content.replace("{{footer}}", footer)

    # Save the dashboard
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Dashboard saved as: {output_path}")
    print(f"📊 Dashboard contains {len(df):,} records and {df['Count'].sum():,} incidents")


if __name__ == "__main__":
    dataframe = generate_data()
    template_file = os.path.join("src", "assets", "legacy_template.html")
    output_file = os.path.join("docs", "dashboard.html")
    generate_html(dataframe, template_file, output_file)
    print("🎉 Dashboard generation complete!")