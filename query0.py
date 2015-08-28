from climb_query import *


output = open("BovenQuery.txt", "w")

#routes = findRoutes(21,18,3)
#for route in routes:
#    output.write(str(route.crag) + "\n" + str(route) + "\n\n\n")

grade_reqs = []

grade_reqs += [RouteRequirement(minimum = 15, maximum = 18, styles = ["Sport"])]
grade_reqs += [RouteRequirement(minimum = 18, maximum = 19, styles = ["Sport"])]
grade_reqs += [RouteRequirement(minimum = 19, maximum = 21, styles = ["Sport"])]
grade_reqs += [RouteRequirement(minimum = 21, maximum = 23, styles = ["Sport"])]

# grade_reqs += [RouteRequirement(minimum = 14, maximum = 17, styles = ["Sport", "Trad"])]
# grade_reqs += [RouteRequirement(minimum = 18, maximum = 20, styles = ["Sport", "Trad"])]
# grade_reqs += [RouteRequirement(minimum = 20, maximum = 20, styles = ["Sport", "Trad"])]
# grade_reqs += [RouteRequirement(minimum = 21, maximum = 23, styles = ["Sport", "Trad"])]


crag_requirement = CragRequirement(crags = ["The Wonderland Crags"])

ranges = findRouteRanges(5, grade_reqs, crag_requirement, remove_non_valid = True)

for i in range(0, len(ranges)):
    route_range = ranges[i]
    output.write("RANGE #" + str(i+1) + "\n------------------------------------------\n")
    for route in route_range:
        output.write(str(route.crag) + "\n" + str(route) + "\n\n")
    output.write("\n\n\n")

print "Work complete"
print "Zug Zug"