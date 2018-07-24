from line_segment import LineSegment
import numpy as np
import matplotlib.pyplot as plt


def get_intersection_points_of_convex_polygons(polygon1, polygon2):

    relevant_vertices = _get_all_vertices_lying_in_the_other_polygon(polygon1, polygon2)
    
    line_intersections = _get_all_line_intersections(polygon1, polygon2)
    
    intersection_points = list()
    intersection_points.extend(relevant_vertices)
    intersection_points.extend(line_intersections)
    
    return _sort_vertices_anti_clockwise_and_remove_duplicates(intersection_points)


def _get_all_vertices_lying_in_the_other_polygon(polygon1, polygon2):
    vertices_lying_in_the_other_polygon = list()
    for corner in polygon1:
        if _polygon_contains_point(polygon2, corner):
            vertices_lying_in_the_other_polygon.append(corner)
    for corner in polygon2:
        if _polygon_contains_point(polygon1, corner):
            vertices_lying_in_the_other_polygon.append(corner)
    return vertices_lying_in_the_other_polygon


def _get_all_line_intersections(polygon1, polygon2):
    line_intersections = list()
    for i in range(len(polygon1)):
        line1i = LineSegment(polygon1[i-1], polygon1[i])
        for j in range(len(polygon2)):
            line2j = LineSegment(polygon2[j-1], polygon2[j])
            point = line1i.get_intersection_point(line2j)
            if point is not None:
                line_intersections.append(point)
    return line_intersections


def _polygon_contains_point(polygon, point):
    
    for i in range(len(polygon)):
        a = np.subtract(polygon[i], polygon[i-1])
        b = np.subtract(point, polygon[i-1])
        if np.cross(a,b) < 0:
            return False
    return True


def _sort_vertices_anti_clockwise_and_remove_duplicates(polygon, tolerance=1e-7):

    polygon = sorted(polygon, key=lambda p: _get_angle_in_radians(_get_inner_point(polygon), p))

    def not_similar_to_previous(l,i):
        return i==0 or np.linalg.norm(np.subtract(l[i-1],l[i])) > tolerance

    return [p for i, p in enumerate(polygon) if not_similar_to_previous(polygon, i)]


def _get_angle_in_radians(p1, p2):
    return np.arctan2(p2[1]-p1[1], p2[0]-p1[0])


def _get_inner_point(polygon):
    x_coords = [p[0] for p in polygon]
    y_coords = [p[1] for p in polygon]
    return [(np.max(x_coords)+np.min(x_coords)) / 2.,(np.max(y_coords)+np.min(y_coords)) / 2.]


def plot_polygon(polygon):
    polygon = list(polygon)
    polygon.append(polygon[0])
    x,y = zip(*polygon)
    plt.plot(x,y,'o-')


if __name__ == '__main__':

    polygon1 = _sort_vertices_anti_clockwise_and_remove_duplicates([[np.cos(x), np.sin(x)] for x in np.random.rand(4)*2*np.pi])
    polygon2 = _sort_vertices_anti_clockwise_and_remove_duplicates([[np.cos(x), np.sin(x)] for x in np.random.rand(4)*2*np.pi])

    polygon3 = get_intersection_points_of_convex_polygons(polygon1, polygon2)

    plot_polygon(polygon1)
    plot_polygon(polygon2)
    if len(polygon3) > 0:
        plot_polygon(polygon3)
    plt.show()