from django.views.generic import View
from django.http import HttpResponse
from django.core import serializers
import json

import models
import route_interfaces
import os

class LoadBoven(View):

    def get(self, request):

        climbing_areas = models.ClimbingArea.objects.filter(name = "Waterval Boven")
        climbing_area = None
        if len(climbing_areas) == 0:
            climbing_area= models.ClimbingArea(
                name = "Waterval Boven", country = "South Africa", province = "Mpumalanga"
                )

            climbing_area.save()
        else:
            climbing_area = climbing_areas[0]

        crag_list = []

        main_crag = models.Crag(name = "The Wonderland Crags", climbing_area = climbing_area)
        main_crag = self.saveCrag(main_crag)

        sub_crag = models.Crag(name = "Tranquilitas Crag", parent_crag = main_crag, climbing_area = climbing_area)
        sub_crag = self.saveCrag(sub_crag)

        crag_list += []
        crag_list += [models.Crag(name = "Als Bells Area", parent_crag = sub_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Creche", parent_crag = sub_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Good And Evil Area", parent_crag = sub_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Malaria Area", parent_crag = sub_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Grunt Area", parent_crag = sub_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Rubiks Cube Boulder", parent_crag = sub_crag, climbing_area = climbing_area)]

        crag_list += [models.Crag(name = "Baboon Buttress", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The God No! Wall", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Disciple Wall", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Little Red Wall", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Hallucinogen Wall", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Breakfast Crag", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Reunion Wall", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Superbowl", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Left Wing", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Theatre", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Right Wing", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Stone Philosopher Area", parent_crag = main_crag, climbing_area = climbing_area)]

        main_crag = models.Crag(name = "Triple Tier Crags", climbing_area = climbing_area)
        main_crag = self.saveCrag(main_crag)

        crag_list += [models.Crag(name = "The Gym", parent_crag = main_crag, climbing_area = climbing_area)]

        sub_crag = models.Crag(name = "He-Man Area", parent_crag = main_crag, climbing_area = climbing_area)
        sub_crag = self.saveCrag(sub_crag)

        crag_list += [models.Crag(name = "Main Wall", parent_crag = sub_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Time Bomb Block", parent_crag = sub_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Skeletor Section", parent_crag = sub_crag, climbing_area = climbing_area)]

        crag_list += [models.Crag(name = "The Foundry", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Acid House", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Far Side", parent_crag = main_crag, climbing_area = climbing_area)]

        main_crag = models.Crag(name = "The Restaurant Crags", climbing_area = climbing_area)
        main_crag = self.saveCrag(main_crag)

        crag_list += [models.Crag(name = "The School", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Restaurant Crag", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Gaper Buttress", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Gaper Face", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Easter Face", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Monsoon Wall", parent_crag = main_crag, climbing_area = climbing_area)]

        main_crag = models.Crag(name = "The Island Crags", climbing_area = climbing_area)
        main_crag = self.saveCrag(main_crag)

        crag_list += [models.Crag(name = "The Boulevard", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Gulley", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Beach", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Never-never Land", parent_crag = main_crag, climbing_area = climbing_area)]

        main_crag = models.Crag(name = "Sport Valley Crags", climbing_area = climbing_area)
        main_crag = self.saveCrag(main_crag)

        crag_list += [models.Crag(name = "The Coven", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Ivory Towers", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Other Side", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The A.C.R.A. Wall", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "WB Wall", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Last Crag of the Century", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The East End", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "A good crag to do some trainspotting", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Toon Town", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Wild Side", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "ZASM Tunnel entrance - (East)", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "The Junkyard", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "ZASM Tunnel entrance - (West)", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Waterval Onder " + u'\u2014' + " Luilekker Crags", parent_crag = main_crag, climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Waterval Onder " + u'\u2014' + " The Aloes", parent_crag = main_crag, climbing_area = climbing_area)]

        for i in range(0, len(crag_list)):
            crag_list[i] = self.saveCrag(crag_list[i])


        route_interface = route_interfaces.BovenRouteInterface(crag_list)

        routes = route_interface.get_routes()
        for i in range(0, len(routes)):
            existing_routes = models.Route.objects.filter(crag = routes[i].crag, name = routes[i].name)
            if len(existing_routes) == 0:
                route = routes[i]
                route.save()

        return HttpResponse("Done Loading Boven")

    def saveCrag(self, crag):
        crags = models.Crag.objects.filter(climbing_area=crag.climbing_area, name = crag.name)
        return_crag = None
        if len(crags) == 0:
            return_crag = crag
            return_crag.save()
        else:
            return_crag = crags[0]

        return return_crag

class LoadBronkies(View):

    def get(self, request):

        climbing_areas = models.ClimbingArea.objects.filter(name = "Bronkies")
        climbing_area = None
        if len(climbing_areas) == 0:
            climbing_area= models.ClimbingArea(
                name = "Bronkies", country = "South Africa", province = "Gauteng"
                )

            climbing_area.save()
        else:
            climbing_area = climbing_areas[0]

        crag_list = []

        crag_list += [models.Crag(name = "Left Hand Side", climbing_area = climbing_area)]
        crag_list += [models.Crag(name = "Right Hand Side", climbing_area = climbing_area)]

        for i in range(0, len(crag_list)):
            crag_list[i] = self.saveCrag(crag_list[i])

        route_interface = route_interfaces.BronkiesRouteInterface(crag_list)

        routes = route_interface.get_routes()
        for i in range(0, len(routes)):
            existing_routes = models.Route.objects.filter(crag = routes[i].crag, name = routes[i].name)
            if len(existing_routes) == 0:
                route = routes[i]
                route.save()

        return HttpResponse("Done Loading Bronkies")

    def saveCrag(self, crag):
        crags = models.Crag.objects.filter(climbing_area=crag.climbing_area, name = crag.name)
        return_crag = None
        if len(crags) == 0:
            return_crag = crag
            return_crag.save()
        else:
            return_crag = crags[0]

        return return_crag
