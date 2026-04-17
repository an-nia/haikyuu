from django.db import models
from django.contrib.gis.db import models as gis_models
from djangoapi.settings import EPSG_FOR_GEOMETRIES


#Modelo schools: puntos
class schools(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    name=models.CharField(max_length=500, blank=True, null=True)
    principal_name=models.CharField(max_length=200, blank=True, null=True)
    students=models.FloatField(blank=True, null=True)
    volleyball_club_name=models.CharField(max_length=500, blank=True, null=True)
    captain=models.CharField(max_length=200, blank=True, null=True)
    geom = gis_models.PointField(srid=int(EPSG_FOR_GEOMETRIES), blank=True, null=True)

#Modelo stadiums: polígonos
class stadiums(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    name=models.CharField(max_length=500, blank=True, null=True)
    city=models.CharField(max_length=200, blank=True, null=True)
    capacity=models.FloatField(blank=True, null=True)
    surface_type=models.CharField(max_length=500, blank=True, null=True)
    num_courts=models.FloatField(blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    perimeter = models.FloatField(blank=True, null=True)
    geom = gis_models.PolygonField(srid=int(EPSG_FOR_GEOMETRIES), blank=True, null=True)

#Modelo nationals_travel: líneas
class nationals_travel(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    team_name=models.CharField(max_length=500, blank=True, null=True)
    origin_prefecture=models.CharField(max_length=200, blank=True, null=True)
    vehicle_type=models.CharField(blank=True, null=True)
    stops_made=models.FloatField(blank=True, null=True)
    total_cost_yen=models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    geom = gis_models.LineStringField(srid=int(EPSG_FOR_GEOMETRIES), blank=True, null=True)
