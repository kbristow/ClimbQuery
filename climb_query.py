def isValidRoute(route, maxRoute, minRoute, minStars, maxStars):
    if route.stars >= minStars and route.grade >= minRoute and route.grade <= maxRoute:
        return True
    return False

def getRange(range_length, routes, index):
    range_crag = routes[index].crag
    range_routes = [routes[index]]
    for i in range(index + 1, min (len(routes), index + range_length)):
        if routes[i].crag == range_crag:
            range_routes += [routes[i]]
        else:
            break
    return range_routes

def getStarAverage(routes):
    
    stars = 0
    
    average = 0
    
    for route in routes:
        stars += route.stars
        
    if len(routes) > 0:
        average = float(stars)/(len(routes))
    
    return average

def validateRange(route_range, required_grades, star_requirements):
    valid_routes = []
    required_grades_clone = required_grades[:]
    for route in route_range:
        for i in range(len(required_grades_clone)-1, -1, -1):
            if required_grades_clone[i].route_valid(route):
                required_grades_clone.pop(i)
        for route_req in required_grades:  
            if route_req.route_valid(route):
                valid_routes += [route]
                break
    
    valid_stars = True
    
    for star_requirement in star_requirements:
        valid_stars = valid_stars and star_requirement.valid_range(valid_routes)

    return len(required_grades_clone) == 0 and valid_stars, valid_routes

def findRoutes(route_interface, maxRoute= 1000, minRoute = 0, minStars = 0, maxStars = 10):
    #input = open("Boven.txt", "r")
    all_routes = route_interface.get_routes()
    current_crag = None
    routes = []
    for route in all_routes:
        if isValidRoute(route, maxRoute, minRoute, minStars, maxStars):
            routes += [route]

    return routes

def findRouteRanges(route_interface, range_length, required_grades, crag_requirements, star_requirements = [], remove_non_valid = False):
    ranges = []
    range_star_averages = []
    ranges_valid_routes = []

    routes = findRoutes(route_interface)
    
    last_index = -1
    for i in range(0, len(routes)):
        route_range = getRange(range_length, routes, i)
        valid_range, valid_routes = validateRange(route_range, required_grades, star_requirements)
        #Test for duplicates before inserting
        if not last_index == -1:
            removal_test = compare_range_similarity(ranges_valid_routes[last_index], valid_routes)
            if removal_test == 1:
                range_star_averages.pop(last_index)
                ranges_valid_routes.pop(last_index)
                ranges.pop(last_index)
            elif removal_test == 2:
                valid_range = False
        
        if valid_range and crag_requirements.cragValid(route_range[0].crag):
            if remove_non_valid:
                for i in range(len(route_range)-1, -1, -1):
                    if not route_range[i] in valid_routes:
                        route_range.pop(i)
            
            
            star_average = getStarAverage(valid_routes)
            index = 0
            
            for j in range(0, len(range_star_averages)):
                if star_average > range_star_averages[j]:
                    index = j
                    break
                if j == len(range_star_averages) - 1:
                    index = j + 1
            
            ranges.insert(index, route_range)
            ranges_valid_routes.insert(index,valid_routes)
            range_star_averages.insert(index, star_average)
            
            last_index = index
    
    return ranges

def compare_range_similarity(range1_valid_routes, range2_valid_routes):
    potential_removal = 1
    range_set_small = range1_valid_routes
    range_set_large = range2_valid_routes
    if len(range2_valid_routes) <= len(range1_valid_routes):
        potential_removal = 2
        range_set_small = range2_valid_routes
        range_set_large = range1_valid_routes
    
    valid = False
    for route in range_set_small:
        if not route in range_set_large:
            valid = True
            break
    
    if valid:
        return 0
    elif potential_removal == 1:
        return 1
    else:
        return 2