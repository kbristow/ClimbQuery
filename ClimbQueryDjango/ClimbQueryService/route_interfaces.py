import re
import models

class Route_Interface(object):

    def __init__(self, file_name):
        self.file_handle = open(file_name, 'r')

    def getRoutes(self):
        raise NotImplementedError("getRoutes function not implemented.")

class Boven_Route_Interface(Route_Interface):

    def __init__(self, crag_list):
        self._initialiseCrags(crag_list)
        super(Boven_Route_Interface, self).__init__("ClimbQueryService/Route Guides/Boven.txt")

    def _initialiseCrags(self, crag_list):
        self.crags = {}

        for crag in crag_list:
            self.crags[crag.name.lower()] = crag


    def _getCrag(self, line):
        if line.lower() in self.crags:
            return self.crags[line.lower()]

        return None

    def _getRoute(self, line, crag):
        routeRegex = r'(.*)\s+([0-9]+)\s*(\*+)\s*(?:\[|\()(.*?)(?:\]|\))(.*)(?:\n|$)'

        routeMatch = re.search(routeRegex, line, re.M|re.I)

        if not routeMatch == None:
            name = routeMatch.group(1).strip()
            grade = int(routeMatch.group(2))
            stars = len(routeMatch.group(3))
            style = ''
            draws = 0
            styleMatch = routeMatch.group(4)
            if styleMatch == "Trad":
                style = "Trad"
            else:
                style = "Sport"
                draw_match = re.search(r'([0-9]+)', styleMatch)
                if not draw_match == None:
                    draws = int(draw_match.group(1))
            
            description = routeMatch.group(5).strip()
            if description.startswith('.'):
                description = description[1:].strip()

            route = models.Route(
                name = name, crag = crag, grade = grade, stars = stars, 
                description = description, climbing_style = style,
                crag_location = self.crag_location, draws = draws, pitch = 1
                )

            self.crag_location += 1

            return route

        return None

    def getRoutes(self):
        routes = []
        current_crag = None
        for line in self.file_handle:
            line = line.decode('utf-8').strip()
            new_crag = self._getCrag(line)
            if not new_crag == None:
                current_crag = new_crag
                self.crag_location = 1
            else:
                route = self._getRoute(line, current_crag)
                if not route == None:
                    routes += [route]

        return routes

class Bronkies_Route_Interface(Route_Interface):

    crag_location = 1

    def __init__(self, crag_list):
        self._initialiseCrags(crag_list)
        super(Bronkies_Route_Interface, self).__init__("ClimbQueryService/Route Guides/Bronkies.txt")

    def _initialiseCrags(self, crag_list):
        self.crags = {}

        for crag in crag_list:
            self.crags[crag.name.lower()] = crag


    def _getCrag(self, line):
        if line.lower() in self.crags:
            return self.crags[line.lower()]

        return None

    def _getRoute(self, line, crag):
        routeRegex = r'(.*?)([0-9]+)\s*?(\**)\s+([0-9]+(?:[a-zA-Z])|\.|Trad).*?\.?\t(.*?)(?:\n|$)'

        routeMatch = re.search(routeRegex, line, re.M|re.I)

        if not routeMatch == None:
            name = routeMatch.group(1).strip()
            grade = int(routeMatch.group(2))
            stars = len(routeMatch.group(3))
            style = ''
            draws = 0
            styleMatch = routeMatch.group(4)
            if styleMatch == "Trad":
                style = "Trad"
            else:
                style = "Sport"
                draw_match = re.search(r'([0-9]+)', styleMatch)
                if not draw_match == None:
                    draws = int(draw_match.group(1))
            
            description = routeMatch.group(5).strip()
            if description.startswith('.'):
                description = description[1:].strip()

            route =models.Route(
                name = name, crag = crag, grade = grade, stars = stars, 
                description = description, climbing_style = style,
                crag_location = self.crag_location, draws = draws, pitch = 1
                )

            self.crag_location += 1

            return route

        return None

    def getRoutes(self):
        routes = []
        current_crag = None
        for line in self.file_handle:
            line = unicode(line.strip(), errors='replace')
            new_crag = self._getCrag(line)
            if not new_crag == None:
                current_crag = new_crag
                self.crag_location = 1
            else:
                route = self._getRoute(line, current_crag)
                if not route == None:
                    routes += [route]

        return routes