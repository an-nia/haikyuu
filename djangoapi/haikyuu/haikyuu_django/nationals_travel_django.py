from django.contrib.gis.geos import GEOSGeometry 
from django.forms.models import model_to_dict
from django.db import connection

#Importar modelo
from haikyuu.models import nationals_travel
from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

class NationalsTravel:

    def insert(self, d: dict):
        cur = connection.cursor()
        cur.execute("select st_snaptogrid(st_geomfromtext(%s, %s), %s)", [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb = cur.fetchall()[0][0]

        g = GEOSGeometry(snapped_wkb, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {'ok': False, 'message': 'Geometría inválida', 'data': []}
        
        # Validar intersección con otras líneas
        query_intersect = "select id from haikyuu_nationals_travel where ST_Intersects(geom, %s)"
        cur.execute(query_intersect, [snapped_wkb])
        r = cur.fetchall()
        if len(r) > 0:
            return {'ok': False, 'message': 'El viaje interseca con otra ruta', 'data': r}

        d['geom'] = g
        # Cálculo de la longitud de la línea
        d['longitud'] = g.length

        b = nationals_travel(**d)
        b.save()
        
        res = model_to_dict(b)
        res['geom'] = g.wkt
        return {'ok': True, 'message': 'Viaje insertado', 'data': [res]}

    def update(self, d: dict):
        cur = connection.cursor()
        cur.execute("select st_snaptogrid(st_geomfromtext(%s, %s), %s)", [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb = cur.fetchall()[0][0]

        g = GEOSGeometry(snapped_wkb, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {'ok': False, 'message': 'Geometría inválida', 'data': []}
        
        query_intersect = "select id from haikyuu_nationals_travel where ST_Intersects(geom, %s) and id != %s"
        cur.execute(query_intersect, [snapped_wkb, d['id']])
        r = cur.fetchall()
        if len(r) > 0:
            return {'ok': False, 'message': 'El viaje interseca con otra ruta', 'data': r}

        l = list(nationals_travel.objects.filter(id=d['id']))
        if not l:
            return {'ok': False, 'message': f"No existe viaje con id {d['id']}", 'data': []}
        
        b = l[0]
        b.geom = g
        b.longitud = g.length
        b.description = d.get('description', b.description)
        b.team_name = d.get('team_name', b.team_name)
        b.origin_prefecture = d.get('origin_prefecture', b.origin_prefecture)
        b.vehicle_type = d.get('vehicle_type', b.vehicle_type)
        b.stops_made = d.get('stops_made', b.stops_made)
        b.total_cost_yen = d.get('total_cost_yen', b.total_cost_yen)
        b.save()
        
        return {'ok': True, 'message': 'Viaje actualizado', 'data': [{'rows_updated': 1}]}

    def delete(self, d: dict):
        l = list(nationals_travel.objects.filter(id=d['id']))
        if not l:
            return {"ok": False, "message": f"No existe viaje con id {d['id']}", "data": []}
            
        b = l[0]
        b.delete()
        return {'ok': True, 'message': 'Viaje borrado', 'data': [{'rows_deleted': 1}]}

    def selectAsDicts(self, d: dict):
        l = list(nationals_travel.objects.filter(id=d['id']))
        if not l:
            return {'ok': False, 'message': 'No encontrado', 'data': []}
            
        b = l[0]
        res = model_to_dict(b)
        res['geom'] = GEOSGeometry(res['geom']).wkt
        return {'ok': True, 'message': 'Recuperado', 'data': [res]}

    def selectAsTuples(self, d: dict):
        l = list(nationals_travel.objects.filter(id=d['id']))
        if not l:
            return {'ok': False, 'message': 'No encontrado', 'data': []}
            
        b = l[0]
        tup = (b.id, b.description, b.team_name, b.origin_prefecture, b.vehicle_type, b.stops_made, b.total_cost_yen, b.longitud, b.geom.wkt)
        return {'ok': True, 'message': 'Recuperado como tupla', 'data': [tup]}
    
    def selectAll(self):
        l = list(nationals_travel.objects.all())
        res = []
        for b in l:
            d = model_to_dict(b)
            d['geom'] = GEOSGeometry(d['geom']).wkt
            res.append(d)
        if not res:
            return {'ok': False, 'message': 'No hay viajes registrados', 'data': []}
        else:
            return {'ok': True, 'message': 'Todos los viajes recuperados', 'data': res}
    

