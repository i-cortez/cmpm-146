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
        detail_points[endpoint_boxes[0]] = source_point
        detail_points[endpoint_boxes[1]] = destination_point
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
    #print(path, endpoint_boxes)
    return path, endpoint_boxes
