#!/usr/bin/env python3
"""
Main application to generate the interactive dashboard.
"""

from enhanced_dashboard import generate_data, create_main_dashboard_file

def main():
    """Main function to generate and save the dashboard."""
    print("🚀 Starting dashboard generation process...")

    # 1. Generate synthetic data
    df = generate_data()

    # 2. Create and save the dashboard file
    dashboard_filename = create_main_dashboard_file(df)

    print(f"🎉 Successfully generated dashboard: {dashboard_filename}")
    print("🌐 Open the HTML file in your browser to view the dashboard.")

if __name__ == "__main__":
    main()
