from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.core import serializers
# Create your views here.
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

class Index(View):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return render(request, 'ClimbQueryWeb/index.html', {})

class Routes(View):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return render(request, 'ClimbQueryWeb/routes.html', {})
        
class Ranges(View):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return render(request, 'ClimbQueryWeb/route_range.html', {})