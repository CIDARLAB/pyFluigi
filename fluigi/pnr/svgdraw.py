from __future__ import annotations

import cairo

from fluigi.parameters import DEVICE_X_DIM, DEVICE_Y_DIM, OUTPUT_DIR

PT_TO_UM = 1 / 352.778


class SVGDraw(object):
    def __init__(self, filename: str, layout: Layout) -> None:
        self._file_path = OUTPUT_DIR.joinpath("{}.svg".format(filename))
        self._layout = layout

    def generate_output(self) -> None:
        surface = cairo.SVGSurface(
            str(self._file_path), DEVICE_X_DIM * PT_TO_UM, DEVICE_Y_DIM * PT_TO_UM
        )
        ctx = cairo.Context(surface)
        ctx.scale(PT_TO_UM, PT_TO_UM)

        for cell in self._layout.get_cells():
            ctx.rectangle(cell.x, cell.y, cell.xdim, cell.ydim)
            ctx.fill()

        for net in self._layout.get_nets():
            waypoints = net.waypoints
            # TODO - Have a more correct version of this later on
            channelwidth = 100
            for i in range(len(waypoints) - 1):
                waypoint = waypoints[i]
                next_waypoint = waypoints[i + 1]
                ctx.move_to(waypoint[0], waypoint[1])
                ctx.line_to(next_waypoint[0], next_waypoint[1])
                ctx.set_line_width(channelwidth / 2)
                ctx.stroke()

        surface.finish()
