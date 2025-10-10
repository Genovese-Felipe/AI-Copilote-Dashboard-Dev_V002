import pytest
from dash import dcc, html
import dash_bootstrap_components as dbc
from src.app import app

def test_app_layout_is_valid():
    """
    Tests that the app layout is not None and is a Dash component.
    The root component is expected to be a dbc.Container.
    """
    assert app.layout is not None
    assert isinstance(app.layout, dbc.Container)

def test_app_layout_contains_expected_elements():
    """
    Tests that the app layout contains the expected graph and filter elements by checking their IDs.
    """
    layout_str = str(app.layout)

    graph_ids = ['bar-category', 'bar-cause', 'line-month', 'bar-site', 'bar-trend', 'pie-severity']
    filter_ids = ['filter-category', 'filter-site', 'filter-month', 'filter-cause', 'filter-severity', 'filter-year', 'filter-status']

    for graph_id in graph_ids:
        assert f"id='{graph_id}'" in layout_str, f"Graph with ID '{graph_id}' not found in layout."

    for filter_id in filter_ids:
        assert f"id='{filter_id}'" in layout_str, f"Filter with ID '{filter_id}' not found in layout."


def test_app_callbacks_are_registered():
    """
    Tests that the callbacks for updating graphs and filters are registered.
    This version iterates through the keys of the callback_map for a more robust check.
    """
    # Get all registered output strings from the callback map keys
    registered_outputs_str = app.callback_map.keys()

    # Check that the main graph and count outputs are registered
    expected_graph_outputs = [
        'bar-category.figure',
        'bar-cause.figure',
        'line-month.figure',
        'bar-site.figure',
        'bar-trend.figure',
        'pie-severity.figure',
        'filtered-count.children'
    ]

    # Check that the filter population outputs are registered
    expected_filter_outputs = [
        'filter-category.options',
        'filter-site.options',
        'filter-month.options',
        'filter-cause.options',
        'filter-severity.options',
        'filter-year.options',
        'filter-status.options'
    ]

    all_found = all(any(expected_output in s for s in registered_outputs_str) for expected_output in expected_graph_outputs)
    assert all_found, "Not all graph update callbacks are registered."

    all_found = all(any(expected_output in s for s in registered_outputs_str) for expected_output in expected_filter_outputs)
    assert all_found, "Not all filter population callbacks are registered."