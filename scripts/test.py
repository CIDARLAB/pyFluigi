import json
import sys

from parchmint import Device

file_path = sys.argv[1]

print("File Name: " + file_path)

device = None

with open(file_path) as data_file:
    text = data_file.read()
    device_json = json.loads(text)
    device = Device(device_json)

print("Checking for components with no dimensions:")
for component in device.components:
    if component.xspan < 0 or component.yspan < 0:
        print(
            "Component - {} | Type - {} | Dimensions - ({}, {})".format(
                component.ID, component.entity, component.xspan, component.yspan
            )
        )
    for port in component.ports:
        if port.x < 0 or port.y < 0:
            "Component - {} | Type - {} | Port {} - ({}, {})".format(
                component.ID, component.entity, port.label, port.x, port.y
            )

print("Checking for components with no ports:")
for component in device.components:
    if len(component.ports) == 0:
        print("Component - {} | Type - {}".format(component.ID, component.entity))

print("Checking to see if connection have floating terminals")
for connection in device.connections:
    if connection.source.port is None:
        print(
            "Connection - {} | Source - {} - No port found".format(
                connection.ID, connection.source.component
            )
        )
    for sink in connection.sinks:
        if sink.port is None:
            print(
                "Connection - {} | Sink - {} - No port found".format(
                    connection.ID, sink.component
                )
            )
