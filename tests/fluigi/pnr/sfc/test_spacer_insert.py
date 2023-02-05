from fluigi.pnr.sfc.spacer_insert import get_spacer_size


def test_get_spacer_size():
    # Note - SPACER_THRESHOLD is 5000 
    # this needs to be set in parameters.py
    assert get_spacer_size(200, 1000) == 0
    assert get_spacer_size(1000, 7000) == 1

def test_generate_spacers():
    raise NotImplementedError()

def test_insert_vertical_spacer_column():
    raise NotImplementedError()

def test_insert_horizontal_spacer_column():
    raise NotImplementedError()



