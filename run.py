import argparse
import os

from src.data_generator import generate_data
from src.dashboard_generator import generate_html as generate_enhanced_html
from src.legacy_dashboard_generator import generate_html as generate_legacy_html
from src.app import app

def main():
    """
    Main entry point for the AI Copilot Dashboard application.

    This script allows you to either run the interactive Dash application
    or generate static HTML dashboards.
    """
    parser = argparse.ArgumentParser(description="AI Copilot Dashboard Runner")
    parser.add_argument(
        "action",
        choices=["run", "generate-legacy", "generate-enhanced"],
        help="The action to perform: 'run' the interactive app, 'generate-legacy' or 'generate-enhanced' static dashboard."
    )
    args = parser.parse_args()

    if args.action == "run":
        print("🚀 Starting the interactive Dash application...")
        app.run_server(debug=True, port=8050)

    elif args.action in ["generate-legacy", "generate-enhanced"]:
        print("🔄 Generating data for the static dashboard...")
        df = generate_data()

        if args.action == "generate-legacy":
            print("🎨 Generating the legacy static dashboard...")
            template_path = os.path.join("src", "assets", "legacy_template.html")
            output_path = os.path.join("docs", "dashboard.html")
            generate_legacy_html(df, template_path, output_path)
            print(f"🎉 Legacy dashboard generated at {output_path}")

        elif args.action == "generate-enhanced":
            print("✨ Generating the enhanced static dashboard...")
            template_path = os.path.join("src", "assets", "template.html")
            output_path = os.path.join("docs", "main_dashboard.html")
            generate_enhanced_html(df, template_path, output_path)
            print(f"🎉 Enhanced dashboard generated at {output_path}")
    else:
        print("❌ Invalid action. Please choose from 'run', 'generate-legacy', or 'generate-enhanced'.")

if __name__ == "__main__":
    main()