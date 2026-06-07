from django.db import models


class VehicleType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class SurfaceType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True) 

    def __str__(self):
        return self.name
    
class Prefecture(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True) 

    def __str__(self):
        return self.name

class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True) 

    def __str__(self):
        return self.name

class SchoolType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name