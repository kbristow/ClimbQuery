from django.views.generic import View
from django.http import HttpResponse
from django.core import serializers
import models


class GetClimbingAreas(View):
    def get(self, request):
        data = serializers.serialize("json", models.ClimbingArea.objects.all())
        return HttpResponse(data, content_type='application/json')
