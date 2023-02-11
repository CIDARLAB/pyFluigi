import math
from typing import List, Optional, Tuple

from parchmint.component import Component
from parchmint.port import Port

from fluigi.pnr.sfc.primitivecell import ComponentSide


def to_polar(rectangle: Tuple[int, int, int, int], point: Tuple[int, int]) -> Tuple[float, float]:
    """ Converts a point from cartesian to polar coordinates for the component 
    center as the origin

    Converts a point from cartesian to polar coordinates for the component center 
    as the origin, and flips the y axis to make the translation. This is a quick 
    way of figuring out the angle of the point relative to the center of the component

    Args:
        rectangle (Tuple[int, int, int, int]): Tuple of x1, y1, x2, y2 coordinates
        point (Tuple[int, int]): Tuple of x, y coordinates

    Returns:
        Tuple[float, float]: r, theta in polar coordinates
    """    
    x1, y1, x2, y2 = rectangle
    x, y = point
    center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
    # Flip the y axis
    y = -y
    center_y = -center_y
    r = ((x - center_x)**2 + (y - center_y)**2)**0.5
    theta = math.atan2(y - center_y, x - center_x)
    return (r, math.degrees(theta))


def get_closest_side(component: Component, port: Port) -> Optional[ComponentSide]:
    """Finds the side of the component that is closest to the port

    Returns the side of the component that is closest to the port, or None if the 
    port is in the center of the component.
    
    In the case of diagonals :
    NorthEast Diagonal : Returns NORTH
    SouthEast Diagonal : Returns EAST
    SouthWest Diagonal : Returns SOUTH
    NorthWest Diagonal : Returns WEST


    Args:
        component (Component): Component on which to find the closest side to
        port (Port): Port to find the closest side to

    Returns:
        Optional[ComponentSide]: Returns the side of the component that is closest to the port, or None if the port is in the center of the component
    """
    # Get the port coordinates in radial coordinates relative to the center of the component
    r, theta = to_polar((0, 0, component.xspan, component.yspan), (int(port.x), int(port.y)))
    
    # Check if the port is in the center
    if r == 0:
        return None
    
    #Convert negative angles to positive
    def to_positive_angle(angle):
        if angle < 0:
            return angle + 360
        return angle
    
    # Get the angles of the diagonals
    _, NORTH_EAST_ANGLE = to_polar((0, 0, component.xspan, component.yspan), (component.xspan, 0))
    _, NORTH_WEST_ANGLE = to_polar((0, 0, component.xspan, component.yspan), (0, 0))
    _, SOUTH_WEST_ANGLE = to_polar((0, 0, component.xspan, component.yspan), (0, component.yspan))
    _, SOUTH_EAST_ANGLE = to_polar((0, 0, component.xspan, component.yspan), (component.xspan, component.yspan))
    
    # Convert negative angles to positive
    theta = to_positive_angle(theta)
    NORTH_EAST_ANGLE = to_positive_angle(NORTH_EAST_ANGLE)
    NORTH_WEST_ANGLE = to_positive_angle(NORTH_WEST_ANGLE)
    SOUTH_WEST_ANGLE = to_positive_angle(SOUTH_WEST_ANGLE)
    SOUTH_EAST_ANGLE = to_positive_angle(SOUTH_EAST_ANGLE)

    # Now if theta is between pi/4 and 3pi/4 return NORTH
    if theta >= NORTH_EAST_ANGLE and theta < NORTH_WEST_ANGLE:
        return ComponentSide.NORTH 
    elif theta >= NORTH_WEST_ANGLE and theta < SOUTH_WEST_ANGLE:
        return ComponentSide.WEST
    elif theta >= SOUTH_WEST_ANGLE and theta < SOUTH_EAST_ANGLE:
        return ComponentSide.SOUTH  
    elif theta >= SOUTH_EAST_ANGLE or theta < NORTH_EAST_ANGLE:
        return ComponentSide.EAST

    

