from climb_query import *
from route_data_structures import *
import route_interfaces

output = open("Query.txt", "w")

#routes = findRoutes(21,18,3)
#for route in routes:
#    output.write(str(route.crag) + "\n" + str(route) + "\n\n\n")

grade_reqs = []

grade_reqs += [RouteRequirement(minimum = 14, maximum = 17, star_requirement = 1, styles = ["Sport"])]
grade_reqs += [RouteRequirement(minimum = 18, maximum = 19, star_requirement = 1, styles = ["Sport"])]
grade_reqs += [RouteRequirement(minimum = 20, maximum = 21, star_requirement = 1, styles = ["Sport"])]
#grade_reqs += [RouteRequirement(minimum = 22, maximum = 23, star_requirement = 1, styles = ["Sport"])]

# grade_reqs += [RouteRequirement(minimum = 14, maximum = 17, star_requirement = 2, styles = ["Sport", "Trad"])]
# grade_reqs += [RouteRequirement(minimum = 18, maximum = 20, star_requirement = 2, styles = ["Sport", "Trad"])]
# grade_reqs += [RouteRequirement(minimum = 20, maximum = 20, star_requirement = 2, styles = ["Sport", "Trad"])]
# grade_reqs += [RouteRequirement(minimum = 21, maximum = 23, star_requirement = 2, styles = ["Sport", "Trad"])]

star_reqs = []
#star_reqs += [StarRequirement(star_count = 3, route_count = 1)]


crag_requirement = CragRequirement(crags = [])

#route_interface = route_interfaces.Boven_Route_Interface()
route_interface = route_interfaces.Bronkies_Route_Interface()

ranges = findRouteRanges(route_interface, 5, grade_reqs, crag_requirement, star_requirements = star_reqs, remove_non_valid = True)

for i in range(0, len(ranges)):
    route_range = ranges[i]
    output.write("RANGE #" + str(i+1) + "\n------------------------------------------\n")
    for route in route_range:
        output.write(str(route.crag) + "\n" + str(route) + "\n\n")
    output.write("\n\n\n")

print "Work complete"
print "Zug Zug"