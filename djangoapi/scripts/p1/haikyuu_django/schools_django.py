from django.contrib.gis.geos import GEOSGeometry 
from django.forms.models import model_to_dict
from django.db import connection

#Importar modelo
from haikyuu.models import schools
from scripts.p1.myLib import p1Settings2
from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

class Schools:

    def insert(self, d: dict):
        cur = connection.cursor()
        cur.execute("select st_snaptogrid(st_geomfromtext(%s, %s), %s)", [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb = cur.fetchall()[0][0]

        g = GEOSGeometry(snapped_wkb, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {'ok': False, 'message': 'Geometría inválida', 'data': []}
        
        # Los puntos deben caer dentro de algún estadio (polígono)
        query_within = "select id from haikyuu_stadiums where ST_Within(%s, geom)"
        cur.execute(query_within, [snapped_wkb])
        r = cur.fetchall()
        if len(r) == 0:
            return {'ok': False, 'message': 'La escuela debe estar dentro de un estadio (polígono)', 'data': []}

        d['geom'] = g
        b = schools(**d)
        b.save()
        
        res = model_to_dict(b)
        res['geom'] = g.wkt
        return {'ok': True, 'message': 'Escuela insertada', 'data': [res]}

    def update(self, d: dict):
        cur = connection.cursor()
        cur.execute("select st_snaptogrid(st_geomfromtext(%s, %s), %s)", [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb = cur.fetchall()[0][0]

        g = GEOSGeometry(snapped_wkb, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {'ok': False, 'message': 'Geometría inválida', 'data': []}
        
        query_within = "select id from haikyuu_stadiums where ST_Within(%s, geom)"
        cur.execute(query_within, [snapped_wkb])
        r = cur.fetchall()
        if len(r) == 0:
            return {'ok': False, 'message': 'La escuela debe estar dentro de un estadio (polígono)', 'data': []}

        l = list(schools.objects.filter(id=d['id']))
        if not l:
            return {'ok': False, 'message': f"No existe escuela con id {d['id']}", 'data': []}
        
        b = l[0]
        b.geom = g
        b.description = d.get('description', b.description)
        b.name = d.get('name', b.name)
        b.principal_name = d.get('principal_name', b.principal_name)
        b.students = d.get('students', b.students)
        b.volleyball_club_name = d.get('volleyball_club_name', b.volleyball_club_name)
        b.captain = d.get('captain', b.captain)
        b.save()
        
        return {'ok': True, 'message': 'Escuela actualizada', 'data': [{'rows_updated': 1}]}

    def delete(self, d: dict):
        l = list(schools.objects.filter(id=d['id']))
        if not l:
            return {"ok": False, "message": f"No existe escuela con id {d['id']}", "data": []}
            
        b = l[0]
        b.delete()
        return {'ok': True, 'message': 'Escuela borrada', 'data': [{'rows_deleted': 1}]}

    def selectAsDicts(self, d: dict):
        l = list(schools.objects.filter(id=d['id']))
        if not l:
            return {'ok': False, 'message': 'No encontrado', 'data': []}
            
        b = l[0]
        res = model_to_dict(b)
        res['geom'] = GEOSGeometry(res['geom']).wkt
        return {'ok': True, 'message': 'Recuperado', 'data': [res]}

    def selectAsTuples(self, d: dict):
        l = list(schools.objects.filter(id=d['id']))
        if not l:
            return {'ok': False, 'message': 'No encontrado', 'data': []}
            
        b = l[0]
        tup = (b.id, b.description, b.name, b.principal_name, b.students, b.volleyball_club_name, b.captain, b.geom.wkt)
        return {'ok': True, 'message': 'Recuperado como tupla', 'data': [tup]}

def run():
    op = Schools()
    print(op.selectAsTuples({'id': 1}))