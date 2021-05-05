import cairo

from fluigi.pnr.cell import Cell

PT_TO_MM = 2.83465
PT_TO_UM = 0.00283465
WIDTH, HEIGHT = 256, 256


class SVGDraw(object):
    def __init__(self) -> None:
        self._surface = cairo.SVGSurface(
            "test.svg", WIDTH * PT_TO_UM, HEIGHT * PT_TO_UM
        )
        self._ctx = cairo.Context(self._surface)

        self._ctx.scale(PT_TO_UM, PT_TO_UM)

    def draw_cell(self, cell: Cell) -> None:
        print("Cell - {}".format(cell))
        self._ctx.move_to(cell.x * PT_TO_UM, cell.y * PT_TO_UM)
        self._ctx.rectangle(0, 0, cell.xdim * PT_TO_UM, cell.ydim * PT_TO_UM)
        self._ctx.fill()

    def generate_output(self) -> None:
        self._surface.finish()
