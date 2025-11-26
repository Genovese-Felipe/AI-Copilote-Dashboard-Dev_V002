# 🤖 AI Copilot Dashboard

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-brightgreen)](https://genovese-felipe.github.io/AI-Copilote-Dashboard-Dev_V002/docs/main_dashboard.html)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Plotly](https://img.shields.io/badge/Plotly-6.3+-orange.svg)](https://plotly.com)
[![Dash](https://img.shields.io/badge/Dash-3.2+-red.svg)](https://dash.plotly.com)
[![Tests](https://img.shields.io/badge/Tests-Passing-green)](tests/)

An advanced incident analysis and data visualization platform powered by artificial intelligence and modern web technologies. This repository has been professionally refactored for improved structure, maintainability, and testability.

## 🌟 Live Demo

**[🚀 View Live Dashboard →](https://genovese-felipe.github.io/AI-Copilote-Dashboard-Dev_V002/docs/main_dashboard.html)**

## 📋 Overview

This project showcases a comprehensive dashboard for incident analysis, featuring:

- **Interactive Data Visualizations**: Built with Plotly for dynamic charts and graphs.
- **Advanced Filtering**: Multi-dimensional filtering capabilities in the interactive version.
- **Responsive Design**: Works seamlessly across all devices.
- **Modular & Testable Code**: Refactored for robustness and easy maintenance.

## 📁 Project Structure

The repository is now organized into a professional and scalable structure:

```
.
├── data/                  # Data files (if any)
├── docs/                  # Generated static HTML dashboards for GitHub Pages
│   ├── dashboard.html
│   └── main_dashboard.html
├── notebooks/             # Jupyter notebooks for exploration
├── src/                   # Main source code
│   ├── assets/            # CSS, JS, and HTML templates
│   ├── __init__.py
│   ├── app.py             # Interactive Dash application
│   ├── data_generator.py  # Centralized data generation module
│   ├── dashboard_components.py # Reusable chart-generating functions
│   └── ...
├── tests/                 # Automated tests
│   ├── test_app_integration.py
│   ├── test_data_generator.py
│   └── test_dashboard_components.py
├── README.md              # This file
├── requirements.txt       # Project dependencies
└── run.py                 # Main entry point for the application
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Genovese-Felipe/AI-Copilote-Dashboard-Dev_V002.git
    cd AI-Copilote-Dashboard-Dev_V002
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies from `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Use the `run.py` script to either launch the interactive dashboard or generate the static HTML files.

-   **To run the interactive Dash application:**
    ```bash
    python run.py run
    ```
    Then, open your browser and navigate to `http://localhost:8050`.

-   **To generate the enhanced static dashboard:**
    ```bash
    python run.py generate-enhanced
    ```
    The output will be saved to `docs/main_dashboard.html`.

-   **To generate the legacy static dashboard:**
    ```bash
    python run.py generate-legacy
    ```
    The output will be saved to `docs/dashboard.html`.

## ✅ Testing

This project includes a comprehensive test suite to ensure code quality and reliability.

-   **To run all tests:**
    ```bash
    python -m pytest
    ```

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Backend & Data Processing |
| **Dash** | Web Application Framework |
| **Plotly** | Interactive Visualizations |
| **Pandas** | Data Manipulation & Analysis |
| **Pytest** | Automated Testing |
| **HTML5/CSS3** | Frontend Structure & Styling |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Contact

**Felipe Genovese** - [GitHub Profile](https://github.com/Genovese-Felipe)

**Project Link**: [https://github.com/Genovese-Felipe/AI-Copilote-Dashboard-Dev_V002](https://github.com/Genovese-Felipe/AI-Copilote-Dashboard-Dev_V002)