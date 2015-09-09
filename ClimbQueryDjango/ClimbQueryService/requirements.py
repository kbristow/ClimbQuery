import models

class RouteRequirement(object):
    def __init__(self, min_grade = 0, max_grade = 50, min_stars = 0, styles = []):
        self.min_grade = min_grade
        self.max_grade = max_grade
        self.min_stars = min_stars
        self.styles = styles

    def routeValid(self, route):
        if not self.styles == [] and route.climbing_style not in self.styles:
            return False
        if self.min_stars > route.stars:
            return False
        if self.min_grade <= route.grade and self.max_grade >= route.grade:
            return True
        return False


class CragRequirement(object):
    def __init__(self,  climbing_area, crags = []):
        self.crags = crags
        self.climbing_area = climbing_area

    def getValidCrags(self):
        valid_crags = []
        if len(self.crags) > 0:
            for crag in self.crags:
                valid_crags.extend(self._extractLeafChildren(crag))

        else:
            valid_crags = models.Crag.objects.filter(climbing_area = self.climbing_area)

        return valid_crags

    def _extractLeafChildren(self, crag):
        valid_crags = []
        children_crags = models.Crag.objects.filter(parent_crag = crag.id)
        if len(children_crags) > 0:
            for child_crag in children_crags:
                valid_crags.extend(self._extractLeafChildren(child_crag))
        else:
            valid_crags = [crag]

        return valid_crags

class StarRequirement(object):
    def __init__(self, min_stars, route_count = 1):
        self.route_count = route_count
        self.min_stars = min_stars

    def validRange(self, valid_climbs):
        valid_routes = 0
        for route in valid_climbs:
            if route.stars >= self.min_stars:
                valid_routes += 1
        
        return valid_routes >= self.route_count