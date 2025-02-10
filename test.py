def is_point_in_polygon(point, polygon):
    """
    Determines if a point is inside a polygon using the ray-casting algorithm.

    Args:
        point (dict): A dictionary with keys 'x' and 'y' (e.g., {'x': 160, 'y': 300}).
        polygon (list): A list of dictionaries with keys 'x' and 'y' that define the vertices
                        of the polygon (in order, either clockwise or counterclockwise).

    Returns:
        bool: True if the point is inside the polygon (or exactly on an edge), False otherwise.
    """
    x, y = point['x'], point['y']
    inside = False
    n = len(polygon)
    
    p1 = polygon[0]
    for i in range(1, n + 1):
        p2 = polygon[i % n]
        # Check if point is between the y-coords of the edge
        if y > min(p1['y'], p2['y']):
            if y <= max(p1['y'], p2['y']):
                # Check if point is to the left of the edge
                if x <= max(p1['x'], p2['x']):
                    if p1['y'] != p2['y']:
                        xinters = (y - p1['y']) * (p2['x'] - p1['x']) / (p2['y'] - p1['y']) + p1['x']
                    else:
                        xinters = p1['x']
                    if p1['x'] == p2['x'] or x <= xinters:
                        inside = not inside
        p1 = p2

    return inside


def is_rectangle_in_spot(lp, spot_polygon):
    """
    Checks if the rectangle defined by lp is entirely within the spot defined by spot_polygon.
    
    Args:
        lp (tuple or list): A tuple/list containing (x1, y1, x2, y2, id, score, label).
                            Here (x1, y1) is one corner and (x2, y2) is the opposite corner.
        spot_polygon (list): A list of dictionaries representing the spot's vertices.
                             Each dictionary must have at least 'x' and 'y' keys.
    
    Returns:
        bool: True if all four corners of the rectangle are inside the polygon, False otherwise.
    """
    # Unpack the rectangle values.
    x1, y1, x2, y2, obj_id, score, label = lp

    # Optional: Quick rejection via bounding box of the polygon.
    poly_min_x = min(p['x'] for p in spot_polygon)
    poly_max_x = max(p['x'] for p in spot_polygon)
    poly_min_y = min(p['y'] for p in spot_polygon)
    poly_max_y = max(p['y'] for p in spot_polygon)
    
    # If the rectangle lies outside the overall bounding box, it cannot be fully inside.
    if x1 < poly_min_x or x2 > poly_max_x or y1 < poly_min_y or y2 > poly_max_y:
        return False

    # Define the rectangle's four corners.
    corners = [
        {'x': x1, 'y': y1},
        {'x': x2, 'y': y1},
        {'x': x2, 'y': y2},
        {'x': x1, 'y': y2}
    ]
    
    # Check if each corner is inside the polygon.
    for corner in corners:
        if not is_point_in_polygon(corner, spot_polygon):
            return False

    return True


# Example usage:
if __name__ == "__main__":
    # Define a spot as a polygon with four vertices.
    spot_polygon = [
        {'id': 21, 'x': 151, 'y': 280, 'spot': 6},
        {'id': 22, 'x': 247, 'y': 292, 'spot': 6},
        {'id': 23, 'x': 162, 'y': 362, 'spot': 6},
        {'id': 24, 'x': 56,  'y': 351, 'spot': 6}
    ]
    
    # Suppose lp is defined as follows:
    # (x1, y1, x2, y2, id, score, label)
    lp = (160, 290, 180, 310, 1, 0.9, 2)
    
    if is_rectangle_in_spot(lp, spot_polygon):
        print("The rectangle is within the spot.")
    else:
        print("The rectangle is NOT within the spot.")
