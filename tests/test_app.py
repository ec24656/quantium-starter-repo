import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

def find_component_by_id(component, target_id):
    if hasattr(component, "id") and component.id == target_id:
        return True

    if hasattr(component, "children"):
        children = component.children

        if isinstance(children, list):
            return any(find_component_by_id(child, target_id) for child in children)
        else:
            return find_component_by_id(children, target_id)

    return False


def find_text(component, text):
    if hasattr(component, "children"):
        if isinstance(component.children, str) and text in component.children:
            return True

        children = component.children

        if isinstance(children, list):
            return any(find_text(child, text) for child in children)
        else:
            return find_text(children, text)

    return False

def test_header_present():
    assert find_text(app.layout, "Soul Foods Sales Visualiser")


def test_graph_present():
    assert find_component_by_id(app.layout, "sales-graph")


def test_region_picker_present():
    assert find_component_by_id(app.layout, "region-filter")