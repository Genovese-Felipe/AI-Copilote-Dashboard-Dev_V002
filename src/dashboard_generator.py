#!/usr/bin/env python3
"""
Enhanced Dashboard Generator with Interactive Filters
"""
import os
from datetime import datetime
import pandas as pd
import plotly.offline as pyo

from .data_generator import generate_data
from .dashboard_components import create_enhanced_dashboard


def generate_stats_grid(df: pd.DataFrame) -> str:
    """Generate the HTML for the statistics grid."""
    total_records = len(df)
    total_incidents = df['Count'].sum()
    sites_count = df['Site'].nunique()
    categories_count = df['Category'].nunique()
    period = f"{df['Year'].min()} - {df['Year'].max()}"
    avg_incidents = df['Count'].mean()

    stats = [
        {"icon": "fa-database", "label": "Total de Registros", "value": f"{total_records:,}"},
        {"icon": "fa-exclamation-triangle", "label": "Total de Incidentes", "value": f"{total_incidents:,}"},
        {"icon": "fa-building", "label": "Locais Monitorados", "value": sites_count},
        {"icon": "fa-tags", "label": "Categorias", "value": categories_count},
        {"icon": "fa-calendar-alt", "label": "Período de Análise", "value": period},
        {"icon": "fa-chart-line", "label": "Média por Registro", "value": f"{avg_incidents:.1f}"}
    ]

    grid_html = ""
    for stat in stats:
        grid_html += f"""
        <div class="stat-card">
            <div class="stat-icon"><i class="fas {stat['icon']}"></i></div>
            <div class="stat-number">{stat['value']}</div>
            <div class="stat-label">{stat['label']}</div>
        </div>
        """
    return grid_html


def generate_footer() -> str:
    """Generate the HTML for the footer."""
    tech_badges = [
        {"icon": "fab fa-python", "label": "Python"},
        {"icon": "", "label": "📊 Plotly"},
        {"icon": "", "label": "🔧 Pandas"},
        {"icon": "", "label": "🧮 NumPy"},
        {"icon": "", "label": "🤖 AI Analytics"},
        {"icon": "", "label": "📱 Responsive"}
    ]

    badges_html = ""
    for badge in tech_badges:
        badges_html += f'<span class="tech-badge"><i class="{badge["icon"]}"></i> {badge["label"]}</span>'

    return f"""
        <div class="footer-title">🚀 Tecnologias Utilizadas</div>
        <div class="tech-stack">{badges_html}</div>
        <div class="footer-note">
            Dashboard gerado automaticamente com tecnologias de IA e análise de dados avançada
        </div>
    """


def generate_html(df: pd.DataFrame, template_path: str, output_path: str):
    """Generate enhanced HTML with modern design"""
    print("🔄 Generating enhanced HTML dashboard...")

    # Create dashboard figure
    dashboard_fig = create_enhanced_dashboard(df)

    # Read HTML template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Generate dynamic components
    title = "AI Copilot Dashboard"
    subtitle = "Plataforma Avançada de Análise de Incidentes com Inteligência Artificial"
    timestamp = datetime.now().strftime('%d/%m/%Y às %H:%M:%S')
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

    # Save the enhanced dashboard
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Enhanced dashboard saved as: {output_path}")
    print(f"📊 Dashboard contains {len(df):,} records and {df['Count'].sum():,} incidents")


if __name__ == "__main__":
    # Generate data and create enhanced dashboard
    dataframe = generate_data()
    template_file = os.path.join("src", "assets", "template.html")
    output_file = os.path.join("docs", "main_dashboard.html")
    generate_html(dataframe, template_file, output_file)
    print("🎉 Enhanced dashboard generation complete!")
    print(f"🌐 Open {output_file} in your browser to view the dashboard")