from django.contrib.gis.geos import GEOSGeometry 
from django.forms.models import model_to_dict
from django.db import connection

#Importar modelo
from haikyuu.models import schools, stadiums
from scripts.p1.myLib import p1Settings2
from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

class Stadiums:

    def insert(self, d: dict):
        cur = connection.cursor()
        query = "select st_snaptogrid(st_geomfromtext(%s, %s), %s)"
        cur.execute(query, [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb = cur.fetchall()[0][0]

        g = GEOSGeometry(snapped_wkb, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {'ok': False, 'message': 'Geometría inválida', 'data': []}
        
        # Validar que no interseque con otros estadios
        query_intersect = "select id from haikyuu_stadiums where ST_relate(geom, %s, 'T********')"
        cur.execute(query_intersect, [snapped_wkb])
        r = cur.fetchall()
        if len(r) > 0:
            return {'ok': False, 'message': 'El estadio interseca con otro existente', 'data': r}

        d['geom'] = g
        # Cálculos espaciales automáticos
        d['area'] = g.area
        d['perimeter'] = g.length

        b = stadiums(**d)
        b.save()
        
        res = model_to_dict(b)
        res['geom'] = g.wkt
        return {'ok': True, 'message': 'Estadio insertado', 'data': [res]}

    def update(self, d: dict):
        cur = connection.cursor()
        cur.execute("select st_snaptogrid(st_geomfromtext(%s, %s), %s)", [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb = cur.fetchall()[0][0]

        g = GEOSGeometry(snapped_wkb, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {'ok': False, 'message': 'Geometría inválida', 'data': []}
        
        # Validar intersección excluyendo el ID actual
        query_intersect = "select id from haikyuu_stadiums where ST_relate(geom, %s, 'T********') and id != %s"
        cur.execute(query_intersect, [snapped_wkb, d['id']])
        r = cur.fetchall()
        if len(r) > 0:
            return {'ok': False, 'message': 'El estadio interseca con otro', 'data': r}

        l = list(stadiums.objects.filter(id=d['id']))
        if not l:
            return {'ok': False, 'message': f"No existe estadio con id {d['id']}", 'data': []}
        
        b = l[0]
        b.geom = g
        b.area = g.area
        b.perimeter = g.length
        b.description = d.get('description', b.description)
        b.name = d.get('name', b.name)
        b.city = d.get('city', b.city)
        b.capacity = d.get('capacity', b.capacity)
        b.surface_type = d.get('surface_type', b.surface_type)
        b.num_courts = d.get('num_courts', b.num_courts)
        b.save()
        
        return {'ok': True, 'message': 'Estadio actualizado', 'data': [{'rows_updated': 1}]}

    def delete(self, d: dict):
        l = list(stadiums.objects.filter(id=d['id']))
        if not l:
            return {"ok": False, "message": f"No existe estadio con id {d['id']}", "data": []}
            
        b = l[0]
        b.delete()
        return {'ok': True, 'message': 'Estadio borrado', 'data': [{'rows_deleted': 1}]}

    def selectAsDicts(self, d: dict):
        l = list(stadiums.objects.filter(id=d['id']))
        if not l:
            return {'ok': False, 'message': 'No encontrado', 'data': []}
            
        b = l[0]
        res = model_to_dict(b)
        res['geom'] = GEOSGeometry(res['geom']).wkt
        return {'ok': True, 'message': 'Recuperado', 'data': [res]}

    def selectAsTuples(self, d: dict):
        l = list(stadiums.objects.filter(id=d['id']))
        if not l:
            return {'ok': False, 'message': 'No encontrado', 'data': []}
            
        b = l[0]
        tup = (b.id, b.description, b.name, b.city, b.capacity, b.surface_type, b.num_courts, b.area, b.perimeter, b.geom.wkt)
        return {'ok': True, 'message': 'Recuperado como tupla', 'data': [tup]}

    def selectAll(self):
        l = list(stadiums.objects.all())
        res = []
        for b in l:
            d = model_to_dict(b)
            d['geom'] = GEOSGeometry(d['geom']).wkt
            res.append(d)
        return {'ok': True, 'message': 'Recuperados todos', 'data': res}