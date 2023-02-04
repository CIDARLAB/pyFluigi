import pytest
from parchmint.component import Component


@pytest.fixture
def component():
    # Create a component
    component = Component(
        name="test_component",
        ID="test_component",
        xpos=0,
        ypos=0,
        xspan=1000,
        yspan=1000,
    )
    return component
