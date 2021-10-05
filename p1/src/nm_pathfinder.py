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
        # Check if the destinatin point is within bounds of the current box
        if source_point != destination_point and box[0] <= destination_point[0] <= box[1] and box[2] <= destination_point[1] <= box[3]:
            destination_box = box
            boxes.append(destination_box)
    
    # Verify that the boxes are valid
    if source_box is None or destination_box is None:
        print("invalid box coordinates: no path found")
        return None, None
    
    # Verify that the source and destination points are not in the same box
    if source_box == destination_box:
        path.append(source_point)
        path.append(destination_point)
        return path, boxes

    # Begin Dijkstra's Forward Search
    #
    # Maps boxes and the distance to the source box
    forward_dist = {source_point: 0}
    backward_dist = {destination_point: 0}

    # Maps boxes and previous-hop boxes
    forward_prev = {source_box: None}
    backward_prev = {destination_box: None}


    heuristic = get_distance(source_point, destination_point)
    forward_dist.update({source_point: 0})
    backward_dist.update({destination_point: 0})
    # Queue maintains a list of pairs (box, cost to previous)
    queue =  [(0, source_box, 'destination'), (0, destination_box, 'source')] #[(heuristic, source_box)]      ###############

    detail_points.update({source_box: source_point})
    detail_points.update({destination_box: destination_point})

    heappush(queue, (0, source_box, 'destination'))      ###############
    heappush(queue, (0, destination_box, 'source'))

    #print("queue", queue)
    while queue:
        current = heappop(queue) #current = (priority, curr_box, curr_goal)
        
        #If path on its way to destination
        if (current[2] == 'destination' and current[1] in backward_prev) or (current[1] == 'source' and current[1] in forward_prev):
            boxes.append(current[1])           ###############
                
            box = current[1]
            while box != source_box:
                path.append(detail_points[box]) #path.insert(0, detail_points[box])
                box = forward_prev[box]  
            path.append(source_point)
            path.reverse() 

            box = backward_prev[current[1]]
            while box != destination_box:
                path.append(detail_points[box])
                box = backward_prev[box]
            path.append(destination_point)
            return path, boxes
        
        else:
            for next_box in mesh["adj"][current[1]]:     ###############
                if current[2] == 'destination':

                    if next_box not in forward_prev:  
                        #prev.update({next_box: current[1]})    ###############
                        # Calculate the next point to move to

                        next_point = get_dest_point(next_box, current[1], detail_points)    ###############
                        current_point = detail_points.get(current[1])
                        distance = forward_dist.get(current_point) + get_distance(current_point, next_point)
                        #if distance < current[0]:
                        heuristic = get_distance(next_point, destination_point)
                        forward_prev.update({next_box: current[1]})
                        forward_dist.update({next_point: distance})
                        detail_points.update({next_box: next_point})
                        boxes.append(current[1])      ###############
                        heappush(queue, (distance + heuristic, next_box, 'destination'))      ###############

                elif current[2] == 'source':
                    if next_box not in backward_prev: 
                        next_point = get_dest_point(next_box, current[1], detail_points)    ###############
                        
                        current_point = detail_points.get(current[1])
                        if backward_dist.get(current_point) is None:
                            distance = get_distance(current_point, next_point)
                        else:
                            distance = backward_dist.get(current_point) + get_distance(current_point, next_point)
                        #if distance < current[0]:
                        heuristic = get_distance(next_point, source_point)
                        backward_prev.update({next_box: current[1]})
                        backward_dist.update({next_point: distance})
                        detail_points.update({next_box: next_point})
                        boxes.append(current[1])      ###############
                        heappush(queue, (distance + heuristic, next_box, 'source'))      ###############
                    
                
    return path, boxes

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


    return (x,y)

