import math


def rotate_polygon(polygon, theta, center_point):
    theta = math.radians(theta)
    rotated_polygon = []
    for point in polygon:
        temp_point = point[0] - center_point[0], point[1] - center_point[1]
        temp_point = (temp_point[0] * math.cos(theta) - temp_point[1] * math.sin(theta), (temp_point[0]*math.sin(theta) + temp_point[1]*math.cos(theta)))
        temp_point = temp_point[0] + center_point[0], temp_point[1] + center_point[1]
        rotated_polygon.append(temp_point)
    return rotated_polygon
