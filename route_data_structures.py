class Crag(object):

    def __init__(self, crag, area, sub_area):
        self.crag = crag
        self.area = area
        self.sub_area = sub_area

    def __repr__(self):
        return_str = self.crag.encode("utf-8")
        if len(self.area) > 0:
            return_str += " : " + self.area.encode("utf-8")

        if len(self.sub_area) > 0:
            return_str += " : " + self.sub_area.encode("utf-8")
        
        return return_str

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