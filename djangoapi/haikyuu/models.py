from django.db import models
from django.contrib.gis.db import models as gis_models
from djangoapi.settings import EPSG_FOR_GEOMETRIES
# Importar  los codelists
from codelist.models import SurfaceType, VehicleType, Prefecture, City, SchoolType

#Modelo schools: puntos
class Schools(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    name=models.CharField(max_length=500, blank=True, null=True)
    principal_name=models.CharField(max_length=200, blank=True, null=True)
    students=models.FloatField(blank=True, null=True)
    volleyball_club_name=models.CharField(max_length=500, blank=True, null=True)
    captain=models.CharField(max_length=200, blank=True, null=True)
    # LLamada a la tabla Prefecture para establecer la relación: clave foránea
    prefecture = models.ForeignKey(Prefecture, on_delete=models.PROTECT, blank=True, null=True)
    # LLamada a la tabla SchoolType para establecer la relación: clave foránea
    school_type = models.ForeignKey(SchoolType, on_delete=models.PROTECT, blank=True, null=True)
    geom = gis_models.PointField(srid=int(EPSG_FOR_GEOMETRIES), blank=True, null=True)

#Modelo stadiums: polígonos
class Stadiums(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    name=models.CharField(max_length=500, blank=True, null=True)
    # LLamada a la tabla City para establecer la relación: clave foránea
    city = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True)
    capacity=models.FloatField(blank=True, null=True)
    # LLamada a la tabla SurfaceType para establecer la relación: clave foránea
    surface_type = models.ForeignKey(SurfaceType, on_delete=models.PROTECT, blank=True, null=True)
    num_courts=models.FloatField(blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    perimeter = models.FloatField(blank=True, null=True)
    geom = gis_models.PolygonField(srid=int(EPSG_FOR_GEOMETRIES), blank=True, null=True)

#Modelo nationals_travel: líneas
class Nationals_travel(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    team_name=models.CharField(max_length=500, blank=True, null=True)
    # LLamada a la tabla Prefecture para establecer la relación: clave foránea
    origin_prefecture = models.ForeignKey(Prefecture, on_delete=models.PROTECT, blank=True, null=True)
    # LLamada a la tabla VehicleType para establecer la relación: clave foránea
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.PROTECT, blank=True, null=True)
    stops_made=models.FloatField(blank=True, null=True)
    total_cost_yen=models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    geom = gis_models.LineStringField(srid=int(EPSG_FOR_GEOMETRIES), blank=True, null=True)
