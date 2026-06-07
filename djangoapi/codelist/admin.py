from django.contrib import admin
from .models import SurfaceType, VehicleType, Prefecture, City, SchoolType

# Lista de modelos de codelist 
codelists = [
    SurfaceType, 
    VehicleType, 
    Prefecture, 
    City, 
    SchoolType
]

# Bucle para registrar cada modelo automáticamente
for model in codelists:
    admin.site.register(model)
