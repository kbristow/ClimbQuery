import re
from route_data_structures import *

class Route_Interface(object):

    def __init__(self, file_name):
        self.file_handle = open(file_name, 'r')

    def getRoutes(self):
        raise NotImplementedError("getRoutes function not implemented.")


class Boven_Route_Interface(Route_Interface):

    def __init__(self):
        self._initialiseCrags()
        super(Boven_Route_Interface, self).__init__("Route Guides/Boven.txt")

    def _initialiseCrags(self):
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
         
        self.crags = {}

        for crag in crag_list:
            if not crag.sub_area == "":
                self.crags[crag.sub_area.lower()] = crag
            else:
                self.crags[crag.area.lower()] = crag


    def _getCrag(self, line):
        if line.lower() in self.crags:
            return self.crags[line.lower()]

        return None

    def _getRoute(self, line, crag):
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

    def getRoutes(self):
        routes = []
        current_crag = None
        for line in self.file_handle:
            line = line.decode('utf-8').strip()
            new_crag = self._getCrag(line)
            if not new_crag == None:
                current_crag = new_crag
            else:
                route = self._getRoute(line, current_crag)
                if not route == None:
                    routes += [route]

        return routes


class Bronkies_Route_Interface(Route_Interface):

    def __init__(self):
        self._initialiseCrags()
        super(Bronkies_Route_Interface, self).__init__("Route Guides/Bronkies.txt")

    def _initialiseCrags(self):
        crag_list = [
            Crag("Left Hand Side", "", ""),
            Crag("Right Hand Side", "", ""),
        ]
         
        self.crags = {}

        for crag in crag_list:
            self.crags[crag.crag.lower()] = crag


    def _getCrag(self, line):
        if line.lower() in self.crags:
            return self.crags[line.lower()]

        return None

    def _getRoute(self, line, crag):
        numberRegex = r'([0-9]+)\s*\**\s+(?:[0-9]|\.)'
        starRegex = r'[0-9]+\s*(\**)\s+(?:[0-9]|\.)'
        styleRegex = r'[0-9]+\s*\**\s+(Trad)'

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
            #style = "Sport"
            return Route(line, routeGrade, stars, style, crag)

        return None

    def getRoutes(self):
        routes = []
        current_crag = None
        for line in self.file_handle:
            line = unicode(line.strip(), errors='replace')
            new_crag = self._getCrag(line)
            if not new_crag == None:
                current_crag = new_crag
            else:
                route = self._getRoute(line, current_crag)
                if not route == None:
                    routes += [route]

        return routes