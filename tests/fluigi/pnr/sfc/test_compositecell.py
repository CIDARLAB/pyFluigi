from fluigi.pnr.sfc.compositecell import CompositeCell
from tests.conftest import generate_new_primitive, cell_test1, cell_test2, cell_test3


def test_from_parchmint_component():
    raise NotImplementedError()


def test_spread_ports():
    raise NotImplementedError()


def test_activate_ports():
    raise NotImplementedError()


def test_equals(cell_test1, cell_test2, cell_test3):

    assert CompositeCell(cell_test1) == CompositeCell(cell_test2)

    assert not CompositeCell(cell_test1) == CompositeCell(cell_test3)

    # TODO - Generate more test cases


