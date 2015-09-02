import re

class Crag(object):

    def __init__(self, crag, area, sub_area):
        self.crag = crag
        self.area = area
        self.sub_area = sub_area

    def __repr__(self):
        return self.crag.encode("utf-8") + " : " + self.area.encode("utf-8") + " : " + self.sub_area.encode("utf-8")

class Route(object):

    def __init__(self, description, grade, stars, style = "None", crag = None):
        self.description = description
        self.grade = grade
        self.stars = stars
        self.crag = crag
        self.style = style

    def __repr__(self):
        return self.description.encode("utf-8")

class RouteRequirement(object):
    def __init__(self, minimum = 0, maximum = 50, star_requirement = 0,styles = []):
        self.minimum = minimum
        self.maximum = maximum
        self.star_requirement = star_requirement
        self.styles = styles

    def routeValid(self, route):
        if not self.styles == [] and route.style not in self.styles:
            return False
        if self.star_requirement > route.stars:
            return False
        if self.minimum <= route.grade and self.maximum >= route.grade:
            return True
        return False


class CragRequirement(object):
    def __init__(self, crags = [], areas = [], sub_areas = []):
        self.crags = crags
        self.areas = areas
        self.sub_areas = sub_areas


    def cragValid(self, crag):
        if self.crags == [] and self.areas == [] and self.sub_areas == []:
            return True
            
        return crag.sub_area in self.sub_areas or crag.area in self.areas or crag.crag in self.crags


class StarRequirement(object):
    def __init__(self, star_count, route_count = 1):
        self.route_count = route_count
        self.star_count = star_count

    def validRange(self, valid_climbs):
        validRoutes = 0
        for route in valid_climbs:
            if route.stars >= self.star_count:
                validRoutes += 1
        
        return validRoutes >= self.route_count

crag_list = [
    Crag("The Wonderland Crags", "Tranquilitas Crag", "Als Bells Area"),
    Crag("The Wonderland Crags", "Tranquilitas Crag", "The Creche"),
    Crag("The Wonderland Crags", "Tranquilitas Crag", "Good And Evil Area"),
    Crag("The Wonderland Crags", "Tranquilitas Crag", "Malaria Area"),
    Crag("The Wonderland Crags", "Tranquilitas Crag", "Grunt Area"),
    Crag("The Wonderland Crags", "Tranquilitas Crag", "Rubiks Cube Boulder"),
    Crag("The Wonderland Crags", "Tranquilitas Crag", "Als Bells Area"),

    Crag("The Wonderland Crags", "Baboon Buttress", ""),
    Crag("The Wonderland Crags", "The God No! Wall", ""),
    Crag("The Wonderland Crags", "The Disciple Wall", ""),
    Crag("The Wonderland Crags", "The Little Red Wall", ""),
    Crag("The Wonderland Crags", "Hallucinogen Wall", ""),
    Crag("The Wonderland Crags", "Breakfast Crag", ""),
    Crag("The Wonderland Crags", "Reunion Wall", ""),
    Crag("The Wonderland Crags", "The Superbowl", ""),
    Crag("The Wonderland Crags", "The Left Wing", ""),
    Crag("The Wonderland Crags", "The Theatre", ""),
    Crag("The Wonderland Crags", "The Right Wing", ""),
    Crag("The Wonderland Crags", "The Stone Philosopher Area", ""),

    Crag("Triple Tier Crags", "The Gym", ""),
    Crag("Triple Tier Crags", "He-Man Area", "Main Wall"),
    Crag("Triple Tier Crags", "He-Man Area", "The Time Bomb Block"),
    Crag("Triple Tier Crags", "He-Man Area", "Skeletor Section"),
    Crag("Triple Tier Crags", "The Foundry", ""),
    Crag("Triple Tier Crags", "The Acid House", ""),
    Crag("Triple Tier Crags", "The Far Side", ""),

    Crag("The Restaurant Crags", "The School", ""),
    Crag("The Restaurant Crags", "The Restaurant Crag", ""),
    Crag("The Restaurant Crags", "Gaper Buttress", ""),
    Crag("The Restaurant Crags", "Gaper Face", ""),
    Crag("The Restaurant Crags", "Easter Face", ""),
    Crag("The Restaurant Crags", "Monsoon Wall", ""),

    Crag("The Island Crags", "The Boulevard", ""),
    Crag("The Island Crags", "The Gulley", ""),
    Crag("The Island Crags", "The Beach", ""),
    Crag("The Island Crags", "Never-never Land", ""),

    Crag("Sport Valley Crags", "The Coven", ""),
    Crag("Sport Valley Crags", "Ivory Towers", ""),
    Crag("Sport Valley Crags", "The Other Side", ""),
    Crag("Sport Valley Crags", "The A.C.R.A. Wall", ""),
    Crag("Sport Valley Crags", "WB Wall", ""),
    Crag("Sport Valley Crags", "The Last Crag of the Century", ""),
    Crag("Sport Valley Crags", "The East End", ""),
    Crag("Sport Valley Crags", "A good crag to do some trainspotting", ""),
    Crag("Sport Valley Crags", "Toon Town", ""),
    Crag("Sport Valley Crags", "ZASM Tunnel entrance - (East)", ""),
    Crag("Sport Valley Crags", "The Junkyard", ""),
    Crag("Sport Valley Crags", "ZASM Tunnel entrance - (West)", ""),
    Crag("Sport Valley Crags", "Waterval Onder " + u'\u2014' + " Luilekker Crags", ""),
    Crag("Sport Valley Crags", "Waterval Onder " + u'\u2014' + " The Aloes", "")
]
 
crags = {}

for crag in crag_list:
    if not crag.sub_area == "":
        crags[crag.sub_area.lower()] = crag
    else:
        crags[crag.area.lower()] = crag


def getCrag(line):
    if line.lower() in crags:
        return crags[line.lower()]

    return None

def getRoute(line, crag):
    numberRegex = r'([0-9]+)'
    starRegex = r'[0-9]\s*(\*+)\s*\['
    styleRegex = r'\[.*?Trad.*?\]'

    numberMatch = re.search(numberRegex, line, re.M|re.I)
    starMatch = re.search(starRegex, line, re.M|re.I)

    if not numberMatch == None and not starMatch == None:
        routeGrade = int(numberMatch.group(1))
        stars = len(starMatch.group(1))
        styleMatch = re.search(styleRegex, line, re.M|re.I)
        if styleMatch == None:
            style = "Sport"
        else:
            style = "Trad"

        return Route(line, routeGrade, stars, style, crag)

    return None

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
            if required_grades_clone[i].routeValid(route):
                required_grades_clone.pop(i)
        for route_req in required_grades:  
            if route_req.routeValid(route):
                valid_routes += [route]
                break
    
    valid_stars = True
    
    for star_requirement in star_requirements:
        valid_stars = valid_stars and star_requirement.validRange(valid_routes)

    return len(required_grades_clone) == 0 and valid_stars, valid_routes

def findRoutes(maxRoute= 1000, minRoute = 0, minStars = 0, maxStars = 10):
    input = open("Boven.txt", "r")
    routes = []
    current_crag = None
    for line in input:
        line = line.decode('utf-8').strip()
        new_crag = getCrag(line)
        if not new_crag == None:
            current_crag = new_crag
        else:
            route = getRoute(line, current_crag)
            if not route == None and isValidRoute(route, maxRoute, minRoute, minStars, maxStars):
                routes += [route]

    return routes

def findRouteRanges(range_length, required_grades, crag_requirements, star_requirements = [], remove_non_valid = False):
    ranges = []
    range_star_averages = []
    ranges_valid_routes = []
    routes = findRoutes()
    
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