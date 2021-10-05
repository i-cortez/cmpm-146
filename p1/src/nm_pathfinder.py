from heapq import heappop, heappush
from math import sqrt
def find_path (source_point, destination_point, mesh):
    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """

    # List of points from source to destination is returned by the function
    path = []
    # A list of boxes explored by the algorithm is returned by the function
    visited_boxes = []
    # Box the source point is found in
    source_box = None
    # Box the destination point is found in
    destination_box = None
    # Keeps track of the precise (x, y) position within a box
    detail_points = {}

    # Iterate through all boxes in the image checking for source and destination points
    for box in mesh["boxes"]:
        # Check if the source point is within bounds of the current box
        if box[0] <= source_point[0] <= box[1] and box[2] <= source_point[1] <= box[3]:
            source_box = box
            visited_boxes.insert(0, source_box)
            print("source point: ", source_point)
            print("source box: ", source_box)
        # Check if the destinatin point is within bounds of the current box
        if source_point != destination_point and box[0] <= destination_point[0] <= box[1] and box[2] <= destination_point[1] <= box[3]:
            destination_box = box
            print("destination point: ", destination_point)
            print("destination box: ", destination_box)
    
    # Verify that the boxes are valid
    if source_box == None or destination_box == None:
        print("invalid box coordinates: no path found")
        return None, None
    
    # Verify that the source and destination points are not in the same box
    if source_box == destination_box:
        path.append(source_point)
        path.append(destination_point)
        visited_boxes.append(destination_box)
        return path, visited_boxes

    # Begin A* Forward Search
    #
    # Maps boxes and the distance to the source box
    dist = {source_point: 0}
    # Maps boxes and previous-hop boxes
    parents = {source_box: None}

    heuristic = get_distance(source_point, destination_point)
    # Queue maintains a list of pairs (box, cost to previous)
    # Begin by making the source box the first to visit
    unvisited_boxes = [(source_box, heuristic)]
    detail_points.update({source_box: source_point})
    heappush(unvisited_boxes, unvisited_boxes[0])

    while unvisited_boxes:
        current = heappop(unvisited_boxes)
        if current[0] == destination_box:
            visited_boxes.append[current[0]]
            path.append(destination_point)
            # Construct the path by iterating through all parents
            while current[0]:
                print("current: ", current[0])
                print("parent: ", parents[current[0]])
                if parents[current[0]]:
                    path.append(detail_points[current[0]])
                current = (parents[current[0]], None)
            path.append(source_point)
            path.reverse()
            print("path: ", path)
            print("boxes: ", visited_boxes)
            return path, visited_boxes
        else:
            neighborhood = mesh["adj"]
            neighbors = neighborhood[current[0]]
            for next_box in neighbors:
                if next_box not in parents:
                    # Calculate the next point to move to
                    # 
                    # print("Path",path)
                    # print("Detail points", detail_points)
                    # print("boxes", boxes)
                    # 
                    next_point = get_dest_point(next_box, current[0], detail_points)
                    current_point = detail_points.get(current[0])
                    distance = dist.get(current_point) + get_distance(current_point, next_point)
                    
                # if distance < cost to previous or distance is None
                if distance < current[1]:
                    parents.update({next_box: current[0]})
                    detail_points.update({next_box: next_point})
                    dist.update({next_point: distance})
                    heuristic = get_distance(next_point, destination_point)
                    heappush(unvisited_boxes, (next_box, distance + heuristic))
                else:
                    print("error: no path found")
    return None, None

def get_distance(a, b):
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def get_dest_point(a, b, box_points):
    x1 = max(a[0], b[0])
    x2 = min(a[1], b[1])
    y1 = max(a[2], b[2])
    y2 = min(a[3], b[3])

    start_point = box_points[b]
    px = start_point[0]
    py = start_point[1]

    #if x1 <= px <= x2:

    if px < x1:  #if src x < b2x1
        if py >= y1 and py <= y2:  # if src y in between b2y1 and b2y2
            x = x1
            y = py
        elif py < y1:
            x = x1
            y = y1
        else:
            x = x1
            y = y2

    elif px >= x1 and px <= x2:    #if b2x1 <= px <= b2x2
        x = px
        y = y1
        
    else:
        if py >= y1 and py <= y2:  # if src y in between b2y1 and b2y2
            x = x2
            y = py
        elif py < y1:
            x = x2
            y = y1
        else:
            x = x2
            y = y2

    #x = box_points[b][0]
    #y = box_points[b][1]

    return (x,y)

