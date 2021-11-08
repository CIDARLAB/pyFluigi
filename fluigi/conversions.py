import json
from pathlib import Path
import fluigi.parameters as parameters
from pymint.mintdevice import MINTDevice
from fluigi.pnr.utils import assign_component_ports
from fluigi.primitives import (
    pull_defaults,
    pull_dimensions,
    pull_terminals,
)


def add_spacing(current_device: MINTDevice) -> None:
    for component in current_device.components:
        if component.params.exists("componentSpacing") is False:
            component.params.set_param("componentSpacing", parameters.COMPONENT_SPACING)

    for connection in current_device.connections:
        if connection.params.exists("connectionSpacing") is False:
            connection.params.set_param(
                "connectionSpacing", parameters.CONNECTION_SPACING
            )


def generate_device_from_mint(
    file_path: str, skip_constraints: bool = False
) -> MINTDevice:
    current_device = MINTDevice.from_mint_file(file_path, skip_constraints)
    if current_device is None:
        raise Exception("Error generating device from the MINT file !")
    try:
        # start_java_vm()
        pull_defaults(current_device)
        pull_dimensions(current_device)
        pull_terminals(current_device)
        add_spacing(current_device)
        # stop_java_vm()
    except Exception as e:
        print("Error getting Primitive data: {}".format(e))
    print(
        "Setting Default MAX Dimensions to the device: ({}, {})".format(
            parameters.DEVICE_X_DIM, parameters.DEVICE_Y_DIM
        )
    )
    return current_device


def convert_to_parchmint(
    input_file: Path,
    outpath: Path,
    assign_terminals: bool = False,
    skip_constriants: bool = True,
):
    """
    Convert a .mint file to a .parchmint.json file
    """
    extension = input_file.suffix
    if extension == ".mint" or extension == ".uf":
        current_device = generate_device_from_mint(str(input_file), skip_constriants)
        # Set the device dimensions
        current_device.params.set_param("x-span", parameters.DEVICE_X_DIM)
        current_device.params.set_param("y-span", parameters.DEVICE_Y_DIM)

        # Assign terminals
        if assign_terminals:
            assign_component_ports(current_device)

        # Save the device parchmint v1_2 to a file
        parchmint_text = current_device.to_parchmint_v1_x()

        # Create new file in outpath with the same name as the current device
        outpath.mkdir(parents=True, exist_ok=True)
        with open(str(outpath.joinpath(input_file.stem + ".json")), "w") as f:
            print("Writing to file: {}".format(f.name))

            json.dump(parchmint_text, f, indent=4)

    else:
        raise Exception("Unsupported file extension: {}".format(extension))