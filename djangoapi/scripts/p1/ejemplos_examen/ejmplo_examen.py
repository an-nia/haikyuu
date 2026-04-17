'''
Contexto:
Tienes una base de datos con dos tablas: parks (polígonos) y trees (puntos).
Quieres añadir un nuevo árbol a la base de datos, pero con una regla estricta: 
el árbol solo puede plantarse si cae estrictamente dentro de algún parque existente.

EJERCICIO:
Crea una función llamada insert_tree(species: str, point_wkt: str) -> dict.
1. La función debe comprobar si el punto (point_wkt con EPSG 25830) está dentro (ST_Within) de algún polígono de la tabla parks.
2. Si no lo está, debe devolver un diccionario de error: {'ok': False, 'message': 'El árbol debe estar dentro de un parque'}.
3. Si lo está, debe insertarlo en la tabla trees y devolver {'ok': True, 'message': 'Árbol plantado', 'id': <nuevo_id>}.
'''

#=====================================
#PSYCOPG
#=====================================
import psycopg
from psycopg.rows import dict_row
#from myLib.connect2 import connect --> al haber añadido la conexión directamente hay que borrarla
from myLib.p1Settings2 import EPSG_CODE

class Trees():
    def __init__(self):
        self.conn = psycopg.connect(dbname='exam', user='postgres', password='postgres', host='postgis', port=5432) #--> conectarse a la base de datos directamente
        #self.conn = connect() --> hay que borrarlo al haber escrito lo de arriba
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()    

    def insert(self, d):
        geom_wkt = d['geom']
        
        # Comprobar geometría
        self.cur.execute("SELECT ST_IsValid(ST_SnapToGrid(ST_GeometryFromText(%s, %s), 0.0001))", [geom_wkt, EPSG_CODE])
        if not self.cur.fetchone()[0]:
            return {'ok': False, 'message': 'Error: la geometría del punto no es válida.', 'data': None}
            
        # El punto debe estar DENTRO de un polígono de la capa parks (capa de polígonos)
        check_within_query = """
            SELECT id FROM parks as p
            WHERE ST_Within(
                ST_SnapToGrid(ST_GeometryFromText(%s, %s), 0.0001), 
                p.geom)
        """
        self.cur.execute(check_within_query, [geom_wkt, EPSG_CODE])
        if len(self.cur.fetchall()) == 0:
            return {'ok': False, 'message': 'Error: el punto insertado debe estar ubicada DENTRO de un parque.', 'data': None}

        # Insertar
        insert_query = """
            INSERT INTO trees
            (species, geom)
            VALUES (%s, ST_SnapToGrid(ST_GeometryFromText(%s, %s), 0.0001))
            RETURNING id
        """
        values = [d['species'], geom_wkt, EPSG_CODE]
        try:
            self.cur.execute(insert_query, values)
            new_id = self.cur.fetchone()[0]
            self.conn.commit()
            return {'ok': True, 'message': 'Árbol plantado', 'data': [{'id': new_id}]}
        except Exception as e:
            self.conn.rollback()
            return {'ok': False, 'message': str(e), 'data': None}
 # COMANDO INSERTAR EN CONSOLA:
 # python scripts/p1/main_examen.py trees insert


#=====================================
#DJANGO
#=====================================
from django.contrib.gis.geos import GEOSGeometry 
from django.forms.models import model_to_dict
from django.db import connection
#Importar modelo
from trees.models import trees
from scripts.p1.myLib import p1Settings2
from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

class Trees:
    def insert(self, d: dict):
        cur = connection.cursor()
        cur.execute("select st_snaptogrid(st_geomfromtext(%s, %s), %s)", [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb = cur.fetchall()[0][0]

        g = GEOSGeometry(snapped_wkb, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {'ok': False, 'message': 'Geometría inválida', 'data': []}
        
        # Comprobar que no haya ya un árbol en ese punto exacto
        query_puntos = "SELECT id FROM trees WHERE ST_Intersects(geom, %s)"
        cur.execute(query_puntos, [snapped_wkb])
        if len(cur.fetchall()) > 0:
            return {'ok': False, 'message': 'Ya existe un árbol plantado en esas coordenadas', 'data': []}
                        
        #El árbol debe caer dentro de algún parque (polígono)
        query_within = "select id from parks where ST_Within(%s, geom)"
        cur.execute(query_within, [snapped_wkb])
        if len(cur.fetchall()) == 0:
            return {'ok': False, 'message': 'El árbol tiene que estar dentro de un parque', 'data': []}

        #Guardar el nuevo árbol
        d['geom'] = g
        b = trees(**d)
        b.save()
        
        res = model_to_dict(b)
        res['geom'] = g.wkt
        return {'ok': True, 'message': 'Árbol plantado', 'data': [res]}
 # IMPORTANTE: 
 #1. En settings de djangoapi, añadir el nombre de la api para este ejercicio.
 #2. En .env.dev cambiar los datos para conectarse a la base de datos.
 # COMANDO INSERTAR EN CONSOLA:
 # python manage.py runscript scripts.p1.main_examen --script-args trees insert
 
#MODELO 
#from django.db import models
#from django.contrib.gis.db import models as gis_models
#from djangoapi.settings import EPSG_FOR_GEOMETRIES

#Modelo trees: puntos
class trees(models.Model):
    species = models.CharField(max_length=500, blank=True, null=True)
    geom = gis_models.PointField(srid=int(EPSG_FOR_GEOMETRIES), blank=True, null=True)
#Modelo parques: polígonos
class parks(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    geom = gis_models.PolygonField(srid=int(EPSG_FOR_GEOMETRIES), blank=True, null=True)
 
 '''
 CONTEXTO:
 Tienes una tabla llamada cameras que representa cámaras de seguridad (puntos), con los campos id, status (texto, por defecto 'OFF') y geom. 
 Ha ocurrido un incidente en unas coordenadas concretas y necesitas encender todas las cámaras que estén cerca.
 
 EJERCICIO:
Crea una función llamada activate_cameras_nearby(incident_wkt: str, radius_meters: float) -> dict.
1. La función debe buscar todas las cámaras cuya geometría esté a una distancia 
igual o menor a radius_meters del punto incident_wkt (ST_Distance).
2. Debe actualizar el campo status de esas cámaras a 'ON'.
3. Debe devolver un diccionario indicando cuántas cámaras se han actualizado: 
{'ok': True, 'message': 'Cámaras activadas', 'updated_count': <num_filas>}.
 '''
 
#=====================================
#PSYCOPG
#=====================================
import psycopg
from psycopg.rows import dict_row
#from myLib.connect2 import connect --> al haber añadido la conexión directamente hay que borrarla
from myLib.p1Settings2 import EPSG_CODE

class Cameras():
    def __init__(self):
        self.conn = psycopg.connect(dbname='exam', user='postgres', password='postgres', host='postgis', port=5432) #--> conectarse a la base de datos directamente
        #self.conn = connect() --> hay que borrarlo al haber escrito lo de arriba
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close() 
        
    def activate_cameras_nearby(self, d):
        geom_wkt = d['geom']
        radio = d['radio']
        
        # Comprobar geometría
        self.cur.execute("SELECT ST_IsValid(ST_SnapToGrid(ST_GeometryFromText(%s, %s), 0.0001))", [geom_wkt, EPSG_CODE])
        if not self.cur.fetchone()[0]:
            return {'ok': False, 'message': 'Error: La geometría no es válida.', 'data': None}
            
        # Actualizar
        update_query = """
            UPDATE cameras 
            SET status='ON'
            WHERE ST_Distance(geom, ST_GeometryFromText(%s, %s)) <= %s
        """
        values = [geom_wkt, EPSG_CODE, d['radio']]
        try:
            self.cur.execute(update_query, values)
            rows_updated = self.cur.rowcount
            self.conn.commit()
            return {'ok': True, 'message': 'Cámaras actualizadas', 'data': [{'rows_updated': rows_updated}]}
        except Exception as e:
            self.conn.rollback()
            return {'ok': False, 'message': str(e), 'data': None}
            

    def activate_cameras_nearby(d):
        geom_wkt = d['geom']
        radio = d['radio']
        
        # Comprobar geometría
        cur.execute("SELECT ST_IsValid(ST_SnapToGrid(ST_GeometryFromText(%s, %s), 0.0001))", [geom_wkt, EPSG_CODE])
        if not cur.fetchone()[0]:
            cur.close()  # <-- CERRAR ANTES DE SALIR POR ERROR
            conn.close() # <-- CERRAR ANTES DE SALIR POR ERROR
            return {'ok': False, 'message': 'Error: La geometría no es válida.', 'data': None}
            
        # Actualizar
        update_query = """
            UPDATE cameras 
            SET status='ON'
            WHERE ST_Distance(geom, ST_GeometryFromText(%s, %s)) <= %s
        """
        values = [geom_wkt, EPSG_CODE, radio]
        
        try:
            cur.execute(update_query, values)
            rows_updated = cur.rowcount
            conn.commit()
            
            #Cerrar
            cur.close()
            conn.close()
            return {'ok': True, 'message': 'Cámara actualizadas', 'data': [{'rows_updated': rows_updated}]}
            
        except Exception as e:
            conn.rollback()
            #Cerrar
            cur.close()
            conn.close()
            return {'ok': False, 'message': str(e), 'data': None}
            
#TODO EN UNA
import psycopg
from myLib.p1Settings2 import EPSG_CODE

def activate_cameras_nearby(d):
    # 1. ABRIR: Conectamos directamente aquí
    conn = psycopg.connect(dbname='exam', user='postgres', password='postgres', host='postgis', port=5432)
    cur = conn.cursor()

    geom_wkt = d['geom']
    radio = d['radio']
    
    # Comprobar geometría
    cur.execute("SELECT ST_IsValid(ST_SnapToGrid(ST_GeometryFromText(%s, %s), 0.0001))", [geom_wkt, EPSG_CODE])
    if not cur.fetchone()[0]:
        cur.close()  # <-- CERRAMOS ANTES DE SALIR POR ERROR
        conn.close() # <-- CERRAMOS ANTES DE SALIR POR ERROR
        return {'ok': False, 'message': 'Error: La geometría no es válida.', 'data': None}
        
    # Actualizar
    update_query = """
        UPDATE cameras 
        SET status='ON'
        WHERE ST_Distance(geom, ST_GeometryFromText(%s, %s)) <= %s
    """
    values = [geom_wkt, EPSG_CODE, radio]
    
    try:
        cur.execute(update_query, values)
        rows_updated = cur.rowcount
        conn.commit()
        
        # 2. CERRAR: Todo ha ido bien, cerramos antes del return final
        cur.close()
        conn.close()
        return {'ok': True, 'message': 'Data updated', 'data': [{'rows_updated': rows_updated}]}
        
    except Exception as e:
        conn.rollback()
        # 3. CERRAR: Ha habido una excepción, cerramos antes del return final
        cur.close()
        conn.close()
        return {'ok': False, 'message': str(e), 'data': None}

 # COMANDO INSERTAR EN CONSOLA:
 # python scripts/p1/main_examen.py cameras activate_cameras_nearby
 
#=====================================
#DJANGO
#=====================================
from django.contrib.gis.geos import GEOSGeometry 
from django.forms.models import model_to_dict
from django.db import connection

#Importar modelo
from cameras.models import cameras
from scripts.p1.myLib import p1Settings2
from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

class Cameras:
    def activate_cameras_nearby(self, d: dict):
        # Extraemos el radio del diccionario
        radio = d['radio'] 

        cur = connection.cursor()
        cur.execute("select st_snaptogrid(st_geomfromtext(%s, %s), %s)", [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb = cur.fetchall()[0][0]

        g = GEOSGeometry(snapped_wkb, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {'ok': False, 'message': 'Geometría inválida', 'data': []}
        
        #cameras hace referencia al modelo no a la clase!!       
        updated_count = cameras.objects.filter(geom__distance_lte=(g, radio)).update(status='ON')
    
        return {'ok': True, 'message': 'Cámaras activadas', 'updated_count': updated_count}
        
#OTRA MANERA:
def update(d: dict):
    try:
        # 1. Validar y crear la geometría del incidente
        geom_incidente = GEOSGeometry(d['geom'], srid=EPSG_FOR_GEOMETRIES)
        
        if not geom_incidente.valid:
            return {'ok': False, 'message': 'Geometría inválida', 'updated_count': 0}

        # 2. GeoDjango ORM: Filtrar por distancia (ST_Distance implícito) y actualizar
        actualizadas = Cameras.objects.filter(
            geom__dwithin=(geom_incidente, d['radio'])
        ).update(status='ON')

        return {
            'ok': True, 
            'message': 'Cámaras activadas', 
            'updated_count': actualizadas
        }

    except Exception as e:
        return {"ok": False, "message": str(e), "updated_count": 0}

 # IMPORTANTE: 
 #1. En settings de djangoapi, añadir el nombre de la api para este ejercicio.
 #2. En .env.dev cambiar los datos para conectarse a la base de datos.
 # COMANDO INSERTAR EN CONSOLA:
 # python manage.py runscript scripts.p1.main_examen --script-args cameras activate_cameras_nearby
 
#MODELO 
#from django.db import models
#from django.contrib.gis.db import models as gis_models
#from djangoapi.settings import EPSG_FOR_GEOMETRIES

#Modelo cameras: puntos
class cameras(models.Model):
    status = models.CharField(max_length=500, blank=True, null=True)
    geom = gis_models.PointField(srid=int(EPSG_FOR_GEOMETRIES), blank=True, null=True)
