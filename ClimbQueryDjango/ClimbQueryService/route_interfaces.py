import re
import models


class RouteInterface(object):
    def __init__(self, file_name):
        self.file_handle = open(file_name, 'r')
        self.crag_location = 0

    def get_routes(self):
        raise NotImplementedError("getRoutes function not implemented.")


class BovenRouteInterface(RouteInterface):
    def __init__(self, crag_list):
        self._initialise_crags(crag_list)
        super(BovenRouteInterface, self).__init__("ClimbQueryService/Route Guides/Boven.txt")

    def _initialise_crags(self, crag_list):
        self.crags = {}

        for crag in crag_list:
            self.crags[crag.name.lower()] = crag

    def _get_crag(self, line):
        if line.lower() in self.crags:
            return self.crags[line.lower()]

        return None

    def _get_route(self, line, crag):
        route_regex = r'(.*)\s+([0-9]+)\s*(\*+)\s*(?:(?:\[|\()(.*?)(?:\]|\)))?([\s,\S]*?)$'

        route_match = re.search(route_regex, line, re.M | re.I)

        if route_match is not None:
            name = route_match.group(1).strip()
            grade = int(route_match.group(2))
            stars = len(route_match.group(3))
            draws = 0
            style_match = route_match.group(4)
            if style_match == "Trad":
                style = "Trad"
            else:
                style = "Sport"
                if style_match is not None:
                    draw_match = re.search(r"([0-9]+)", style_match)
                    if draw_match is not None:
                        draws = int(draw_match.group(1))

            description = route_match.group(5).strip().replace("\n","")
            if description.startswith('.'):
                description = description[1:].strip()

            route = models.Route(
                name=name, crag=crag, grade=grade, stars=stars,
                description=description, climbing_style=style,
                crag_location=self.crag_location, draws=draws, pitch=1
            )

            self.crag_location += 1

            return route

        return None

    def get_routes(self):
        routes = []
        current_crag = None
        running_line = ""
        for line in self.file_handle:
            line = line.decode('utf-8').strip()
            running_line += line + " "
            
            new_crag = self._get_crag(line)
            if new_crag is not None:
                current_crag = new_crag
                self.crag_location = 1
                running_line = ""
            elif len(line) == 0:
                route = self._get_route(running_line, current_crag)
                if route is not None:
                    routes += [route]
                running_line = ""

        return routes


class BronkiesRouteInterface(RouteInterface):
    crag_location = 1

    def __init__(self, crag_list):
        self._initialise_crags(crag_list)
        super(BronkiesRouteInterface, self).__init__("ClimbQueryService/Route Guides/Bronkies.txt")

    def _initialise_crags(self, crag_list):
        self.crags = {}

        for crag in crag_list:
            self.crags[crag.name.lower()] = crag

    def _get_crag(self, line):
        if line.lower() in self.crags:
            return self.crags[line.lower()]

        return None

    def _get_route(self, line, crag):
        route_regex = r'(.*?)([0-9]+)\s*?(\**)\s+([0-9]+(?:[a-zA-Z])|\.|Trad).*?\.?\t(.*?)(?:\n|$)'

        route_match = re.search(route_regex, line, re.M | re.I)

        if route_match is not None:
            name = route_match.group(1).strip()
            grade = int(route_match.group(2))
            stars = len(route_match.group(3))
            draws = 0
            style_match = route_match.group(4)
            if style_match == "Trad":
                style = "Trad"
            else:
                style = "Sport"
                draw_match = re.search(r'([0-9]+)', style_match)
                if draw_match is not None:
                    draws = int(draw_match.group(1))

            description = route_match.group(5).strip()
            if description.startswith('.'):
                description = description[1:].strip()

            route = models.Route(
                name=name, crag=crag, grade=grade, stars=stars,
                description=description, climbing_style=style,
                crag_location=self.crag_location, draws=draws, pitch=1
            )

            self.crag_location += 1

            return route

        return None

    def get_routes(self):
        routes = []
        current_crag = None
        for line in self.file_handle:
            line = unicode(line.strip(), errors='replace')
            new_crag = self._get_crag(line)
            if new_crag is not None:
                current_crag = new_crag
                self.crag_location = 1
            else:
                route = self._get_route(line, current_crag)
                if route is not None:
                    routes += [route]

        return routes
