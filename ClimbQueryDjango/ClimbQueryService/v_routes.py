from django.views.generic import View
from django.http import HttpResponse
from django.core import serializers
import json

from requirements import *


class GetRoutes(View):
    # def get(self, request):
    #     crag_requirement = CragRequirement(crags = [],
    #       climbing_area = models.ClimbingArea.objects.filter(name = "Waterval Boven").first())
    #     valid_crags = crag_requirement.getValidCrags()
    #     routes = findRoutes(validCrags = valid_crags, maxGrade = 20, minGrade = 15, minStars = 4)
    #     return HttpResponse(serializers.serialize("json", routes), content_type='application/json')

    def post(self, request):
        data = json.loads(request.body)
        crags = []
        if data['crags'] is not None:
            data['crags'] = map(int, data['crags'])
            crags = list(models.Crag.objects.filter(pk__in=data['crags']))

        crag_requirement = CragRequirement(crags=crags, climbing_area=models.ClimbingArea.objects.filter(
            pk=data["climbingArea"]).first())
        valid_crags = crag_requirement.get_valid_crags()
        routes = find_routes(valid_crags=valid_crags, max_grade=int(data["maxGrade"]), min_grade=int(data["minGrade"]),
                             min_stars=int(data["minStars"]), climbing_style=data["style"])
        return HttpResponse(serializers.serialize("json", routes), content_type='application/json')


class GetRange(View):
    def post(self, request):
        # Currently hardcoded for some testing purposes
        crag_requirement = CragRequirement(crags=[], climbing_area=models.ClimbingArea.objects.filter(
            name="Waterval Boven").first())
        # valid_crags = crag_requirement.getValidCrags()

        grade_reqs = []
        grade_reqs += [RouteRequirement(min_grade=15, max_grade=19, min_stars=1, styles=["Sport"])]

        star_reqs = []
        star_reqs += [StarRequirement(min_stars=1, route_count=4)]

        route_ranges = find_route_ranges(6, required_grades=grade_reqs, crag_requirements=crag_requirement,
                                         star_requirements=star_reqs, remove_non_valid=True)

        json_data = []

        for route_range in route_ranges:
            route_range['routes'] = serializers.serialize("python", route_range['routes'])
            route_range['crag'] = serializers.serialize("python", [route_range['crag']])
            json_data += [route_range]

        return HttpResponse(json.dumps(json_data), content_type='application/json')


def get_valid_crags(climbing_area, crags):
    valid_crags = crags
    if len(crags) == 0:
        valid_crags = models.Crag.objects.filter(climbing_area=climbing_area, parent_crag__isnull=True)
    return valid_crags


def find_routes(valid_crags, max_grade=1000, min_grade=0, min_stars=0, climbing_style=""):
    routes = models.Route.objects.filter(grade__gte=min_grade, grade__lte=max_grade, stars__gte=min_stars,
                                         crag__in=valid_crags).order_by("crag", "crag_location")
    if len(climbing_style) is not 0:
        routes = routes.filter(climbing_style=climbing_style)

    return routes


def get_range(range_length, routes, index):
    range_crag = routes[index].crag
    range_routes = [routes[index]]
    for i in range(index + 1, min(len(routes), index + range_length)):
        if routes[i].crag == range_crag:
            range_routes += [routes[i]]
        else:
            break
    return range_routes


def get_star_average(routes):
    stars = 0

    average = 0

    for route in routes:
        stars += route.stars

    if len(routes) > 0:
        average = float(stars) / (len(routes))

    return average


def validate_range(route_range, required_grades, star_requirements):
    valid_routes = []
    required_grades_clone = required_grades[:]
    for route in route_range:
        for i in range(len(required_grades_clone) - 1, -1, -1):
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


def find_route_ranges(range_length, required_grades, crag_requirements, star_requirements=None, remove_non_valid=False):
    if not star_requirements:
        star_requirements = []
    ranges = []
    range_star_averages = []
    ranges_valid_routes = []

    valid_crags = crag_requirements.get_valid_crags()

    routes = find_routes(valid_crags)

    last_index = -1
    for i in range(0, len(routes)):
        route_range = get_range(range_length, routes, i)
        valid_range, valid_routes = validate_range(route_range, required_grades, star_requirements)
        # Test for duplicate ranges before inserting
        if not last_index == -1:
            removal_test = compare_range_similarity(ranges_valid_routes[last_index], valid_routes)
            if removal_test == 1:
                range_star_averages.pop(last_index)
                ranges_valid_routes.pop(last_index)
                ranges.pop(last_index)
            elif removal_test == 2:
                valid_range = False

        if valid_range:
            if remove_non_valid:
                for j in range(len(route_range) - 1, -1, -1):
                    if not route_range[j] in valid_routes:
                        route_range.pop(j)

            star_average = get_star_average(valid_routes)
            index = 0

            for j in range(0, len(range_star_averages)):
                if star_average > range_star_averages[j]:
                    index = j
                    break
                if j == len(range_star_averages) - 1:
                    index = j + 1

            ranges.insert(index, route_range)
            ranges_valid_routes.insert(index, valid_routes)
            range_star_averages.insert(index, star_average)

            last_index = index

    return_ranges = []
    for i in range(0, len(ranges)):
        return_ranges += [{
            'star_average': range_star_averages[i],
            'crag': ranges[i][0].crag,
            'routes': ranges[i]
        }]

    return return_ranges


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
        if route not in range_set_large:
            valid = True
            break

    if valid:
        return 0
    elif potential_removal == 1:
        return 1
    else:
        return 2
