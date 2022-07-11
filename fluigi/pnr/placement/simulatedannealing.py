# from jpype.types import *
import json

from pymint.mintdevice import MINTDevice

from fluigi.pnr.layout import Layout

# import jpype
# import jpype.imports


# jpype.startJVM(classpath=['/home/krishna/CIDAR/pyfluigi/pnr/fluigi-java/Fluigi-jar-with-dependencies.jar'])


# import java
# from org.cidarlab.fluigi.fluigi import *

# from org.cidarlab.fluigi.netlist import Device, AbstractPrimitive


def generate_simulated_annealing_layout(layout: Layout):

    d = Device("TEST")
    d.addLayer("flow")

    for cell in layout.get_cells():
        ap = AbstractPrimitive(cell.ID, cell.x_span, cell.y_span)
        # TODO set terminal locations for this cell
        d.addComponent(ap, "flow")
        print("Added component: {}".format(ap.getName()))

    for net in layout.get_nets():
        if len(net.sink_terminals) > 1:
            # this is the case for nets
            raise Exception("Need to implement logic for converting nets")
        else:
            c1 = d.getComponent("flow", net.source_terminal.component)
            c2 = d.getComponent(net.sink[0])
            cp1.getTerminal()
            c = d.addChannel(c1, c2, "flow")
            c.setName(net.ID)
            c.setSourcePoint(cp2)
            c.setTargetPoint(cp1)
            c.setSourceIndex(tindex1)
            c.setTargetIndex(tindex2)

    Fluigi.placeAndRouteDevice(d)


def generate_simulated_annealing_layout_v2(device: MINTDevice) -> Layout:
    jsonstring = json.dumps(device.to_parchmint_v1())
    print(jsonstring)
    device = Fluigi.placeAndRouteDevice(jsonstring)

    print("PNR Executed" + device.getName())
