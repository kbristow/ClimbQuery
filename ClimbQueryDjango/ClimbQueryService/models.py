from django.db import models

# Create your models here.
class ClimbingArea(models.Model):
    name = models.TextField()
    country = models.TextField()
    province = models.TextField()

    """
    @classmethod
    def create(cls, name, country, province):
        climbing_area = cls(
            name=name, country=country, province=province
            )
        return climbing_area
    """

class Crag(models.Model):
    name = models.TextField()
    parent_crag = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    climbing_area = models.ForeignKey('ClimbingArea', on_delete=models.CASCADE, null=True, blank=True)

    """
    @classmethod
    def create(cls, name, climbing_area, parent_crag=None):
        crag = cls(
            name=name, climbing_area=climbing_area, parent_crag=parent_crag
            )
        return crag
    """

class Route(models.Model):
    name = models.TextField()
    pitch = models.IntegerField()
    crag = models.ForeignKey('Crag', on_delete=models.CASCADE)
    crag_location = models.FloatField()
    grade = models.IntegerField()
    stars = models.IntegerField()
    draws = models.IntegerField()
    climbing_style = models.TextField()
    description = models.TextField()
    
    """
    @classmethod
    def create(cls, name, crag, grade, stars, description, climbing_style, crag_location, draws = 0, pitch = 1):
        route = cls(
            name=name, crag=crag, grade=grade, stars=stars, description=description,
            climbing_style = climbing_style, crag_location=crag_location, draws=draws, pitch=pitch
            )
        return route
    """