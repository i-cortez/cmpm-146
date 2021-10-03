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

    path = []
    boxes = {}
    endpoint_boxes = []
    box_path = []
    detail_points = {}

    
    print("source point", source_point)
    print("destination point", destination_point)
    #print(mesh['adj'])
    for box in mesh['boxes']:
        if source_point[0] <= box[1] and source_point[0] >= box[0] and source_point[1] >= box[2] and \
           source_point[1] <= box[3]:
                endpoint_boxes.insert(0,box)
        if destination_point[0] <= box[1] and destination_point[0] >= box[0] and destination_point[1] >= box[2] and \
             destination_point[1] <= box[3]:
                endpoint_boxes.insert(1,box)

    
    # Start breadth first search
    queue = None
    parent = None
    

    if len(endpoint_boxes) < 2:
        print("No path!")

    else:
        detail_points[endpoint_boxes[0]] = [source_point[1], source_point[0]]
        detail_points[endpoint_boxes[1]] = [destination_point[1], destination_point[0]]
        queue = [endpoint_boxes[0]] 
        parent = {endpoint_boxes[0]: None}
        while queue:
            current_box = queue.pop(0)
            if current_box == endpoint_boxes[1]:
                while current_box is not None:  #Finds path by going backwards
                    box_path.insert(0, current_box)
                    current_box = parent[current_box]  
            else:
                for adj in mesh['adj'][current_box]:
                    if adj not in parent:
                        parent[adj] = current_box
                        queue.append(adj)        
        if len(box_path) < 1 or box_path[-1] is not endpoint_boxes[1]:
            print("No path!")

    print(box_path)
    print(endpoint_boxes[0])
    
    index = 0

    while index < len(box_path) - 1:
        x_left = max(box_path[index][2], box_path[index + 1][2])
        x_right = min(box_path[index][3], box_path[index + 1][3])
        y_down = max(box_path[index][0], box_path[index + 1][0])
        y_up = min(box_path[index][1], box_path[index + 1][1])
        px = detail_points[box_path[index]][0]
        py = detail_points[box_path[index]][1]

        detail_points[box_path[index + 1]] = [None, None]
        

        if px < x_left:  #if src x < b2x1
            if py >= y_down and py <= y_up:  # if src y in between b2y1 and b2y2
                detail_points[box_path[index + 1]][0] = x_left
                detail_points[box_path[index + 1]][1] = py
            elif py < y_down:
                detail_points[box_path[index + 1]][0] = x_left
                detail_points[box_path[index + 1]][1] = y_down
            else:
                detail_points[box_path[index + 1]][0] = x_left
                detail_points[box_path[index + 1]][1] = y_up

        elif px >= x_left and px <= x_right:    #if b2x1 <= px <= b2x2
            detail_points[box_path[index + 1]][0] = px
            detail_points[box_path[index + 1]][1] = y_down
        
        else:
            if py >= y_down and py <= y_up:  # if src y in between b2y1 and b2y2
                detail_points[box_path[index + 1]][0] = x_right
                detail_points[box_path[index + 1]][1] = py
            elif py < y_down:
                detail_points[box_path[index + 1]][0] = x_right
                detail_points[box_path[index + 1]][1] = y_down
            else:
                detail_points[box_path[index + 1]][0] = x_right
                detail_points[box_path[index + 1]][1] = y_up
       # print(box_path[index],  "completed")
        index += 1

    #print("DETAIL POINTS:", detail_points)
    
    
    detail_points[endpoint_boxes[1]] = [destination_point[1],destination_point[0]]
    if len(detail_points) == 1:
        print([source_point[0],source_point[1]])
        print([destination_point[0],destination_point[1]])
    index = 0
    for box in box_path:
        print(detail_points[box])
        path.append(detail_points[box][::-1]) 
        index += 1

   # path.append([source_point[0], source_point[1]])
   # path.append([destination_point[0], destination_point[1]])
    print("path", path)
    print("endpoint_boxes", endpoint_boxes)
    #print(path, endpoint_boxes)
    return path, endpoint_boxes

