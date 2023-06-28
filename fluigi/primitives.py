import json
from typing import Dict, Optional, List
from parchmint.params import Params

import requests
from parchmint.device import Device, Device, ValveType, ValveType
from parchmint.port import Port, Port

import fluigi.parameters as parameters

OLD_PRIMITIVES_CHECKLIST = []


def _get_defaults(mint: str) -> Optional[Dict]:
    """Calls the rest api for pulling the data

    Args:
        mint (str): the mint string for the mint

    Returns:
        Dict: returns the object
    """
    try:
        params = {"mint": mint}
        r = requests.get(f"{parameters.PRIMITIVE_SERVER_URI}/defaults", params=params, timeout=1000)
        python_object = r.json()
        return python_object
    except Exception as exception:
        print(f"Could not retrieve default parameters for {mint}, Exception: {exception}")
        return None


def _get_dimensions(mint: str, params: Params) -> Optional[Dict]:
    """Calls the dimension respect

    Args:
        mint (str): mint type
        params (Dict): data for the params

    Returns:
        Optional[Dict]: the dimension data
    """
    try:
        req_params = {"mint": mint}
        req_params["params"] = json.dumps(params.data)
        r = requests.get(
            f"{parameters.PRIMITIVE_SERVER_URI}/dimensions",
            params=req_params,
            timeout=1000
        )

        python_object = r.json()
        return python_object

    except Exception as exception:
        print(f"Could not retrieve dimensions for {mint}, Exception: {exception}")
        return None


def _get_terminals(mint: str, params: Params) -> Optional[List]:
    """ Calls the rest api

    Args:
        mint (str): type of the component
        params (Params): params object

    Returns:
        Optional[Dict]: filled out data object
    """
    try:
        req_params = {"mint": mint}
        req_params["params"] = json.dumps(params.data)
        req = requests.get(
            f"{parameters.PRIMITIVE_SERVER_URI}/terminals",
            params=req_params,
            timeout=1000
        )

        terminals = req.json()

        python_object = []

        for terminal in terminals:
            componentport = Port(json_data=terminal)
            python_object.append(componentport)
            # print(componentport)

        return python_object

    except Exception as exception:
        print(f"Could not retrieve dimensions for {mint}, Exception: {exception}")
        return None


def get_valve_type(mint: str) -> Optional[str]:
    """Gets the valve type as a REST call

    Args:
        mint (str): MINT type string

    Returns:
        Optional[str]: the valve type
    """
    try:
        # python_object = json.loads(output.stdout.decode('utf-8'))
        params = {"mint": mint}
        r = requests.get(f"{parameters.PRIMITIVE_SERVER_URI}/valve_type", params=params, timeout=1000)
        python_object = r.json()
        return python_object
    except Exception as exception:
        print(f"Could not retrieve default parameters for {mint}, Exception: {exception}")
        return None


def pull_defaults(device: Device):
    """Pull the default the params for all the components

    Args:
        device (Device): Device you want to pull the defaults for
    """    
    print("Pulling Default Values of Components")
    for component in device.components:
        # print("comonent name {}".format(component.name))
        defaults = _get_defaults(component.entity)
        if defaults is None:
            print(f"Warning: Could not pull default values for {component.name} of type :{component.entity}")
            continue

        # Fills out all the missing params
        for key in defaults.keys():
            if not component.params.exists(key):
                val = defaults[key]
                try:
                    num = float(val)
                    component.params.set_param(key, num)
                except ValueError:
                    component.params.set_param(key, val)

        mark_for_delete = []
        for param_key in component.params.data.keys():
            if param_key not in defaults.keys():
                print(
                    f'Deleted unsupported param "{param_key}" from component {component.ID} : {component.entity}'
                )
                mark_for_delete.append(param_key)

        for param_key in mark_for_delete:
            del component.params.data[param_key]


def pull_dimensions(device: Device):
    """Pull the dimensions for the device

    Pulls the dimensions from the 3DuF primitives server

    Args:
        device (Device): The device we need to pull the dimensions for
    """
    print("Pulling Dimensions of Components")
    for component in device.components:
        dims = _get_dimensions(component.entity, component.params)

        if dims is None:
            print(f"Warning: Could not pull default values for {component.name} of type :{component.entity}")
            continue

        # Assign the xspan and yspan
        component.xspan = dims["x-span"]
        component.yspan = dims["y-span"]
        # print("comonent name: {}, Dims: ({}, {}) ".format(component.name, component.xspan, component.yspan))


def pull_terminals(device: Device):
    """Pulls all the terminal information for all the components

    Args:
        device (Device): The device for which need to pull the info for
    """
    print("Pulling Terminals of Components")
    for component in device.components:
        terminals = _get_terminals(component.entity, component.params)
        if terminals is None:
            print(f"Warning: Could not pull terminal data for {component.name} of type: {component.entity}")
        else:
            # Print warning if the terminal is outside of the x and y span of the component
            for terminal in terminals:
                if terminal.x < 0 or terminal.x > component.xspan or terminal.y < 0 or terminal.y > component.yspan:
                    print(
                        f"Warning: Terminal {terminal.label} ({terminal.x}, {terminal.y}) of component {component.ID} is outside of the span of the component ({component.xspan}, {component.yspan})"
                    )
            # Assign the terminals
            component.add_component_ports(terminals)
            # print("Updated the component terminals: {}", component)


def pull_valve_types(device: Device):
    """Pull the valve types for the device

    Args:
        device (Device): Device we need to pull the valve type data from
    """    
    print("Pulling Valve Type Information")
    for component in device.get_valves():
        type_info = get_valve_type(component.entity)
        if type_info is None:
            print(f"Warning: Could not pull valve type data for {component.name} of type: {component.entity}")
        else:
            if type_info == "NORMALLY_OPEN":
                device.update_valve_type(component, ValveType.NORMALLY_OPEN)
            elif type_info == "NORMALLY_CLOSED":
                device.update_valve_type(component, ValveType.NORMALLY_CLOSED)
            else:
                print(
                    f"Warning: Found unknown valve type data for {component.name} of type: {component.entity} - {type_info}"
                )


def size_nodes(device: Device) -> None:
    """Sizes the nodes to the right dimensions

    Args:
        device (Device): Device that we want to pull the node sizes for
    """    
    for component in device.components:
        if component.entity == "NODE":
            # Find the connections to the nodes
            connections = device.get_connections_for_component(component)
            # Find the connection with the largest connectionWidth param
            max_width = 0
            for connection in connections:
                if connection.params.get_param("channelWidth") > max_width:
                    max_width = connection.params.get_param("channelWidth")
            # Set the node size to the max connection width
            component.xspan = max_width
            component.yspan = max_width
