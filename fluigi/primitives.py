from typing import Optional
from parchmint.device import Device
from pymint.mintdevice import MINTDevice
from parchmint.port import Port
import subprocess
import json
import os
import fluigi.parameters as parameters
import requests

# All the imports for the java pipe
import jpype
import jpype.imports

# from jpype.types import *


# java_path = parameters.FLUIGI_JAVA_PNR_JAR_PATH.resolve()
# jpype.startJVM(classpath=[str(java_path)])

# import java
# from org.cidarlab.fluigi.fluigi import *


# def stop_java_vm():
#     jpype.shutdownJVM()


OLD_PRIMITIVES_CHECKLIST = []


def get_defaults(mint: str):

    if mint in OLD_PRIMITIVES_CHECKLIST:
        print(
            "Warning this is one of the the old fluigi primitives, this means that the we dont pull defaults"
        )
        return None
    else:
        # primitives_dir = os.path.join(parameters.PROGRAM_DIR, "primitives","dist")
        # cmd = ['node', 'index.js' , mint,  'defaults']
        # output = subprocess.run(cmd, cwd=primitives_dir, stdout=subprocess.PIPE)

        try:
            # python_object = json.loads(output.stdout.decode('utf-8'))
            params = {"mint": mint}
            r = requests.get(
                "{}/defaults".format(parameters.PRIMITIVE_SERVER_URI), params=params
            )
            python_object = r.json()
            return python_object
        except Exception as e:
            print("Could not retrieve default parameters for {}".format(mint))
            print(e)
            return None


def get_dimensions(mint: str, params):

    if mint in [s.replace(" ", "") for s in OLD_PRIMITIVES_CHECKLIST]:
        print(
            "Warning this is one of the the old fluigi primitives, this means that the default values can be incorrect"
        )

        map = dict()
        for key in params.data.keys():
            val = params.data[key]
            try:
                map[key] = int(val)

            except ValueError:
                print("Found a non int param: {} - {}".format(key, val))

        try:
            python_object = dict(Fluigi.getDimensions(mint, java.util.HashMap(map)))
            print("Data Retrieved by the java pipe: {}".format(python_object))
            return python_object
        except Exception as e:
            print(e)
            print(
                "Error occured during the java dimension retrieval for: {}-{}".format(
                    mint, params
                )
            )

    else:
        # primitives_dir = os.path.join(parameters.PROGRAM_DIR, "primitives","dist")

        # cmd = ['node', 'index.js', mint, 'dimension', json.dumps(params.data)]

        # output = subprocess.run(cmd, cwd=primitives_dir, stdout=subprocess.PIPE)

        try:
            req_params = {"mint": mint}
            req_params["params"] = json.dumps(params.data)
            r = requests.get(
                "{}/dimensions".format(parameters.PRIMITIVE_SERVER_URI),
                params=req_params,
            )

            python_object = r.json()
            return python_object

        except Exception as e:
            print("Could not retrieve dimensions for {}".format(mint))
            print(e)
            return None


def get_terminals(mint: str, params):

    if mint in [s.replace(" ", "") for s in OLD_PRIMITIVES_CHECKLIST]:
        print(
            "Warning this is one of the the old fluigi primitives, this means that the default values can be incorrect"
        )

        map = dict()
        for key in params.data.keys():
            val = params.data[key]
            try:
                map[key] = int(val)

            except ValueError:
                print("Found a non int param: {} - {}".format(key, val))

        java_object = dict(Fluigi.getTerminals(mint, java.util.HashMap(map)))
        print("Data Retrieved by the java pipe: {}".format(java_object))

        terminals = []
        for key in java_object.keys():
            coords = java_object["0"].getPointCoords()
            componentport = Port()
            componentport.x = int(coords[0])
            componentport.y = int(coords[1])
            componentport.label = str(key)

            # print(componentport)
            terminals.append(componentport)

        return terminals

    else:
        try:
            req_params = {"mint": mint}
            req_params["params"] = json.dumps(params.data)
            r = requests.get(
                "{}/terminals".format(parameters.PRIMITIVE_SERVER_URI),
                params=req_params,
            )

            terminals = r.json()

            python_object = []

            for terminal in terminals:
                componentport = Port(terminal)
                python_object.append(componentport)
                # print(componentport)

            return python_object

        except Exception as e:
            print("Could not retrieve dimensions for {}".format(mint))
            print(e)
            return None


def pull_defaults(device: Device):
    print("Pulling Default Values of Components")
    for component in device.components:
        # print("comonent name {}".format(component.name))
        defaults = get_defaults(component.entity)
        if defaults is None:
            print(
                "Warning: Could not pull default values for {} of type :{}".format(
                    component.name, component.entity
                )
            )
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
                    'Deleted unsupported param "{}" from component {} : {}'.format(
                        param_key, component.ID, component.entity
                    )
                )
                mark_for_delete.append(param_key)

        for param_key in mark_for_delete:
            del component.params.data[param_key]


def pull_dimensions(device: Device):
    print("Pulling Dimensions of Components")
    for component in device.components:
        # print("comonent name {}".format(component.name))
        dims = get_dimensions(component.entity, component.params)
        # print(dims)

        if dims is None:
            print(
                "Warning: Could not pull default values for {} of type :{}".format(
                    component.name, component.entity
                )
            )
            continue

        # Assign the xspan and yspan
        component.xspan = dims["x-span"]
        component.yspan = dims["y-span"]


def pull_terminals(device: Device):
    print("Pulling Terminals of Components")
    for component in device.components:
        terminals = get_terminals(component.entity, component.params)
        if terminals is None:
            print(
                "Warning: Could not pull terminal data for {} of type: {}".format(
                    component.name, component.entity
                )
            )
        else:
            # Assign the terminals
            component.add_component_ports(terminals)
            # print("Updated the component terminals: {}", component)
