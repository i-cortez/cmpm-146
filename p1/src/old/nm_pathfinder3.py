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
    boxes = []
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
            boxes.insert(0, source_box)
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
        boxes.append(destination_box)
        return path, boxes

    # Begin Dijkstra's Forward Search
    #
    # Maps boxes and the distance to the source box
    dist = {source_point: 0}
    # Maps boxes and previous-hop boxes
    prev = {source_box: None}
    # Queue maintains a list of pairs (box, cost to previous)
    queue = [(0, source_box)]      ###############
    detail_points.update({source_box: source_point})
    heappush(queue, (0, source_box))      ###############

    while queue:
        current = heappop(queue)
        # Check if the current box is the destination box
        if current[1] == destination_box:           ###############
            boxes.append(current[1])           ###############
            path.append(destination_point)
            #print("prev list", prev)
            # Construct the path by iterating through all previous boxes
            while current[1]:       ###############
                print("current: ", current[1])        ###############
                print("previous: ", prev[current[1]])      ###############
                if prev[current[1]]:      ###############
                    print("if: ", current[1])    ###############
                    path.append(detail_points[current[1]])   ###############
                current = (None, prev[current[1]])     ###############
            path.append(source_point)
            path.reverse()
            #print("path: ", path)
            #print("boxes: ", boxes)
            return path, boxes
        else:
            for next_box in mesh["adj"][current[1]]:     ###############
                if next_box not in prev or distance < dist[next_point]:
                    prev.update({next_box: current[1]})    ###############
                    # Calculate the next point to move to
                    
                    #print("Path",path)
                    #print("Detail points", detail_points)
                    #print("boxes", boxes)

                    next_point = get_dest_point(next_box, current[1], detail_points)    ###############
                    current_point = detail_points[current[1]]      ###############
                    distance = dist[current_point] + get_distance(current_point, next_point)
                    detail_points.update({next_box: next_point})
                    dist.update({next_point: distance})
                    boxes.append(current[1])      ###############
                    heappush(queue, (distance, next_box))      ###############
                """"             
                else:
                    current_point = detail_points[current[1]]   ###############
                    next_point = detail_points[next_box]
                    distance = dist[current_point] + get_distance(current_point, next_point)
                    if distance < dist[next_point]:
                        dist.update({next_box: distance})
                        prev[next_box] = current[1]     ###############
                        #for box in queue:
                        #    if box[0] == next_box:
                        #        box[1] = distance
                        heappush(queue,(distance, next_box))    ###############
                """
                
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
    
    """
    if x1 < x2: x = x1
    else: x = x2
    if y1 < y2: y = y1
    else: y = y2
    """

    return (x,y)
