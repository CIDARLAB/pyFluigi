import json

from pymint.mintdevice import MINTDevice
from fluigi.pnr.utils import assign_component_ports
from fluigi.primitives import pull_defaults, pull_dimensions, pull_terminals, size_nodes


def test_dx10_ref():
        
    mint_device = MINTDevice.from_mint_file("/workspaces/pyfluigi/tests/dx10_ref.mint")

    current_device = mint_device.device
    if current_device is None:
        raise ValueError("Error generating device from the MINT file !")
    try:
        pull_defaults(current_device)
        pull_dimensions(current_device)
        pull_terminals(current_device)
        # add_spacing(current_device)
        size_nodes(current_device)
    except Exception as e:
        print(f"Error getting Primitive data: {e}")

    assign_component_ports(mint_device)

    # print(
    #     "Setting Default MAX Dimensions to the device: ({}, {})".format(
    #         parameters.DEVICE_X_DIM, parameters.DEVICE_Y_DIM
    #     )
    # )

    json_text = json.dumps(current_device.to_parchmint_v1_2())
    print(json_text)
    raise NotImplementedError()
