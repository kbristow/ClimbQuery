from django.views.generic import View
from django.http import HttpResponse
from django.core import serializers
import json
import models
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Crags(View):

    def get(self, request):
        data = serializers.serialize("json", models.Crag.objects.all())
        return HttpResponse(data, content_type='application/json')

    def post(self, request):
        data = json.loads(request.body)
        crags = []

        if not data['climbingArea'] == None:
            crags = serializers.serialize("python", models.Crag.objects.filter(climbing_area = int(data['climbingArea'])))

        return HttpResponse(json.dumps(crags), content_type='application/json')