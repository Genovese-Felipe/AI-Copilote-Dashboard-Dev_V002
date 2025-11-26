import pandas as pd
import pytest
import plotly.graph_objects as go
from src.dashboard_components import create_dashboard, create_enhanced_dashboard
from src.data_generator import generate_data

@pytest.fixture(scope="module")
def sample_data():
    """
    Pytest fixture to generate sample data once for all tests in this module.
    """
    return generate_data()

def test_create_dashboard_returns_figure(sample_data):
    """
    Tests that create_dashboard returns a Plotly Figure object.
    """
    fig = create_dashboard(sample_data)
    assert isinstance(fig, go.Figure)

def test_create_dashboard_has_expected_subplots(sample_data):
    """
    Tests that the figure from create_dashboard has the correct number of subplots and traces.
    """
    fig = create_dashboard(sample_data)
    # The dashboard is a 2x3 grid, so it should have 6 subplots.
    assert len(fig._grid_ref) == 2
    assert len(fig._grid_ref[0]) == 3
    # Check that there are 6 traces (one for each subplot)
    assert len(fig.data) == 6

def test_create_enhanced_dashboard_returns_figure(sample_data):
    """
    Tests that create_enhanced_dashboard returns a Plotly Figure object.
    """
    fig = create_enhanced_dashboard(sample_data)
    assert isinstance(fig, go.Figure)

def test_create_enhanced_dashboard_has_expected_subplots(sample_data):
    """
    Tests that the figure from create_enhanced_dashboard has the correct number of subplots and traces.
    """
    fig = create_enhanced_dashboard(sample_data)
    # The dashboard is a 2x3 grid, so it should have 6 subplots.
    assert len(fig._grid_ref) == 2
    assert len(fig._grid_ref[0]) == 3
    # Check that there are 6 traces (one for each subplot)
    assert len(fig.data) == 6

def test_dashboard_titles_and_labels(sample_data):
    """
    Tests that the dashboards have titles and the subplots have annotations (titles).
    """
    legacy_fig = create_dashboard(sample_data)
    enhanced_fig = create_enhanced_dashboard(sample_data)

    assert legacy_fig.layout.title.text is not None
    assert enhanced_fig.layout.title.text is not None

    # Check for subplot titles (annotations)
    assert len(legacy_fig.layout.annotations) >= 6
    assert len(enhanced_fig.layout.annotations) >= 6