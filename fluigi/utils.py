import os
import pathlib
from typing import Tuple

import cairo
import networkx as nx
from parchmint import Device, Target

import fluigi.parameters as parameters
from fluigi.parameters import DEVICE_X_DIM, DEVICE_Y_DIM, PT_TO_UM


def printgraph(G, filename: str) -> None:
    tt = pathlib.Path(parameters.OUTPUT_DIR).joinpath(filename + ".dot")
    print("output:", str(tt.absolute()))
    nx.nx_agraph.to_agraph(G).write(str(tt.absolute()))

    os.system(
        "dot -Tpdf {} -o {}.pdf".format(str(tt.absolute()), pathlib.Path(parameters.OUTPUT_DIR).joinpath(tt.stem))
    )


def get_ouput_path(filename: str) -> str:
    return os.path.join(parameters.OUTPUT_DIR, filename)


def calcuate_waypoint(device: Device, target: Target) -> Tuple[float, float]:
    """Calculates the coordinates of the Target

    [extended_summary]

    Args:
        device (Device): [description]
        target (Target): [description]

    Returns:
        Tuple[float]: [description]
    """
    # Get  position of the of target and calculate the offset from the base component
    component = device.get_component(target.component)
    if target.port is not None:
        port = component.get_port(target.port)
        xoffset = component.xpos + port.x
        yoffset = component.ypos + port.y
        return (xoffset, yoffset)
    else:
        # Return the center of the component instead
        return (
            int(component.xpos + component.xspan / 2),
            int(component.ypos + component.yspan / 2),
        )


def render_svg(d: Device, suffix: str) -> None:

    suffix = suffix.replace(d.name, "")
    if d.params.exists("x-span"):
        xspan = d.params.get_param("x-span")
    else:
        xspan = DEVICE_X_DIM

    if d.params.exists("y-span"):
        yspan = d.params.get_param("y-span")
    else:
        yspan = DEVICE_Y_DIM

    rats_nest_count = 0
    print("Rendering device {}".format(d.name))

    surface = cairo.SVGSurface(
        str(parameters.OUTPUT_DIR.joinpath("{}.svg".format(d.name + suffix))),
        xspan * PT_TO_UM,
        yspan * PT_TO_UM,
    )
    ctx = cairo.Context(surface)
    ctx.scale(PT_TO_UM, PT_TO_UM)

    for component in d.components:
        print("Old position {} ({}):{}, {}".format(component.ID, component.entity, component.xpos, component.ypos))
        component.rotate_component()
        print("new position:{}, {}".format(component.xpos, component.ypos))
        if component.params.exists("position"):
            xpos = component.xpos
            ypos = component.ypos

            # Printing
            ctx.rectangle(xpos, ypos, component.xspan, component.yspan)
            # Set the color to black
            ctx.set_source_rgb(0, 0, 0)
            ctx.fill()

        else:
            print("Could not render component:{} since no position information was found".format(component.ID))

    for component in d.components:
        if component.params.exists("position"):
            xpos = component.xpos
            ypos = component.ypos

            # Printing
            ctx.rectangle(xpos, ypos, component.xspan, component.yspan)
            ctx.set_source_rgb(1, 1, 1)
            ctx.set_line_width(100)
            ctx.stroke()
        else:
            print("Could not render component:{} since no position information was found".format(component.ID))

    ctx.set_source_rgb(0, 0, 1)

    # Go through each of the connections
    for connection in d.connections:
        # For every source, sink pair check if a path exists with the same source sink pair and if so draw a line using the waypoints else draw a line between the source and sink components
        channelwidth = connection.params.get_param("channelWidth")
        source = connection.source
        if source is None:
            print("No source for connection:", connection.ID)
            continue
        for sink in connection.sinks:
            # First ensure that the ports are set for the source and sink or else you'll need to render rats nests at the
            # centers
            found_flag = False
            if source.port is not None and sink.port is not None:
                for path in connection.paths:
                    if source == path.source and sink == path.sink:
                        found_flag = True
                        waypoints = path.waypoints
                        if len(waypoints) > 0:
                            for i in range(len(waypoints) - 1):
                                # Set the color to blue
                                ctx.set_source_rgb(0, 0, 1)
                                waypoint = waypoints[i]
                                next_waypoint = waypoints[i + 1]
                                ctx.move_to(waypoint[0], waypoint[1])
                                ctx.line_to(next_waypoint[0], next_waypoint[1])
                                ctx.set_line_width(channelwidth / 2)
                                ctx.stroke()
                        else:
                            print(
                                "No waypoints found in \n connection:{} Source:{}  Sink:{} ".format(
                                    connection.ID, str(source), str(sink)
                                )
                            )
                            render_rats_nest(d, ctx, channelwidth, source, sink)

                if found_flag is False:
                    rats_nest_count += 1
                    print(
                        "No paths found in \n connection:{} Source:{}  Sink:{} ".format(
                            connection.ID, str(source), str(sink)
                        )
                    )
                    render_rats_nest(d, ctx, channelwidth, source, sink)

    # Draw ports at the end so that all the port connections are visible thoroughly
    for component in d.components:
        if component.params.exists("position"):
            # Set the color to black
            xpos = component.xpos
            ypos = component.ypos
            # Draw small cicles for all the ports
            for port in component.ports:
                # Set the color to red
                ctx.set_source_rgb(1, 0, 0)
                # Draw circle of radius 5
                ctx.arc(xpos + port.x, ypos + port.y, 100, 0, 2 * 3.14)
                ctx.fill()
        else:
            print("Could not render port of component :{} since no position information was found".format(component.ID))

    surface.finish()

    print(
        "Rendered {} components , {} connections and {} rats nests".format(
            len(d.components), len(d.connections), rats_nest_count
        )
    )


def render_rats_nest(d, ctx, channelwidth, source, sink):
    # Set the color to grey
    ctx.set_source_rgb(0.5, 0.5, 0.5)
    source_waypoint = calcuate_waypoint(d, source)
    target_waypoint = calcuate_waypoint(d, sink)

    ctx.move_to(source_waypoint[0], source_waypoint[1])
    ctx.line_to(target_waypoint[0], target_waypoint[1])
    ctx.set_line_width(channelwidth / 2)
    ctx.stroke()
