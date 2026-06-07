#Django imports
from django.http import JsonResponse
from django.views import View
from core.myLib.baseDjangoView import BaseDjangoView
import json

# Imports para seguridad
from django.contrib.auth.mixins import LoginRequiredMixin
from core.myLib.manageUsers import getUserGroups

#Importar archivos con los métodos
from haikyuu.haikyuu_django.nationals_travel_django import NationalsTravel as NT
from haikyuu.haikyuu_django.schools_django import Schools as SC
from haikyuu.haikyuu_django.stadiums_django import Stadiums as ST


# Clase prueba
class HelloHaikyuu(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Haikyuu. Miau", "data":[]},status=200)

# Clase para la tabla de líneas: nationals_travel
class NationalsTravel(LoginRequiredMixin, BaseDjangoView):
    #Constructor
    def __init__(self):
        self.n=NT()
    
    #OPERACIONES GET
    #Llama a la función selectAsDicts del archivo nationals_travel_django.py dentro de la carpeta haikyuu_django de la appi
    def selectone(self, id):
        return JsonResponse(self.n.selectAsDicts({'id': id}))
    
    #Llama a la función selectAll del archivo nationals_travel_django.py dentro de la carpeta haikyuu_django de la appi
    def selectall(self):
        return JsonResponse(self.n.selectAll())
    
    #OPERACIONES POST
    #Llama a la función insert del archivo nationals_travel_django.py dentro de la carpeta haikyuu_django de la appi
    def insert(self, request):
        # Seguridad: solo los usuarios con el grupo 'editor' pueden insertar.
        grupos = getUserGroups(request.user)
        if 'editor' not in grupos:
            return JsonResponse({"ok": False, "message": "No tienes permisos de editor", "data": []})

        body_data={}
        #CASO 1: form-data o x-www-form-urlencoded
        if request.POST:
            body_data = request.POST.dict()
        #CASO 2: raw json
        #Para obtener el diccionario del body de la petición
        else:
            body_data=json.loads(request.body)
        return JsonResponse(self.n.insert(body_data))
    
    #Llama a la función update del archivo nationals_travel_django.py dentro de la carpeta haikyuu_django de la appi
    def update(self, request, id):
        # Seguridad: solo los usuarios con el grupo 'editor' pueden actualizar.
        grupos = getUserGroups(request.user)
        if 'editor' not in grupos:
            return JsonResponse({"ok": False, "message": "No tienes permisos de editor", "data": []})
        
        body_data={}
        if request.POST:
            body_data = request.POST.dict()
        else:
            body_data=json.loads(request.body)
        return JsonResponse(self.n.update(body_data))    
    
    #Llama a la función delete del archivo nationals_travel_django.py dentro de la carpeta haikyuu_django de la appi
    def delete(self, request, id):
        # Seguridad: solo los usuarios con el grupo 'editor' pueden eliminar.
        grupos = getUserGroups(request.user)
        if 'editor' not in grupos:
            return JsonResponse({"ok": False, "message": "No tienes permisos de editor", "data": []})
        return JsonResponse(self.n.delete({'id': id}))

    
# Clase para la tabla de polígonos: schools
class Schools(LoginRequiredMixin, BaseDjangoView):
    #Constructor
    def __init__(self):
        self.sc=SC()
    
    #OPERACIONES GET
    #Llama a la función selectAsDicts del archivo schools_django.py dentro de la carpeta haikyuu_django de la appi
    def selectone(self, id):
        return JsonResponse(self.sc.selectAsDicts({'id': id}))
    
    #Llama a la función selectAll del archivo schools_django.py dentro de la carpeta haikyuu_django de la appi
    def selectall(self):
        return JsonResponse(self.sc.selectAll())
    
    #OPERACIONES POST
    #Llama a la función insert del archivo schools_django.py dentro de la carpeta haikyuu_django de la appi
    def insert(self, request):
        grupos = getUserGroups(request.user)
        if 'editor' not in grupos:
            return JsonResponse({"ok": False, "message": "No tienes permisos de editor", "data": []})

        body_data={}
        #CASO 1: form-data o x-www-form-urlencoded
        if request.POST:
            body_data = request.POST.dict()
        #CASO 2: raw json
        #Para obtener el diccionario del body de la petición
        else:
            body_data=json.loads(request.body)
        return JsonResponse(self.sc.insert(body_data))
    
    #Llama a la función update del archivo schools_django.py dentro de la carpeta haikyuu_django de la appi
    def update(self, request, id):
        grupos = getUserGroups(request.user)
        if 'editor' not in grupos:
            return JsonResponse({"ok": False, "message": "No tienes permisos de editor", "data": []})

        body_data={}
        if request.POST:
            body_data = request.POST.dict()
        else:
            body_data=json.loads(request.body)
        return JsonResponse(self.sc.update(body_data))    
    
    #Llama a la función delete del archivo schools_django.py dentro de la carpeta haikyuu_django de la appi
    def delete(self, request, id):
        grupos = getUserGroups(request.user)
        if 'editor' not in grupos:
            return JsonResponse({"ok": False, "message": "No tienes permisos de editor", "data": []})
        return JsonResponse(self.sc.delete({'id': id}))


class Stadiums(LoginRequiredMixin, BaseDjangoView):
    #Constructor
    def __init__(self):
        self.st=ST()
    
    #OPERACIONES GET
    #Llama a la función selectAsDicts del archivo stadiums_django.py dentro de la carpeta haikyuu_django de la appi
    def selectone(self, id):
        return JsonResponse(self.st.selectAsDicts({'id': id}))
    
    #Llama a la función selectAll del archivo stadiums_django.py dentro de la carpeta haikyuu_django de la appi
    def selectall(self):
        return JsonResponse(self.st.selectAll())
    
    #OPERACIONES POST
    #Llama a la función insert del archivo stadiums_django.py dentro de la carpeta haikyuu_django de la appi
    def insert(self, request):
        grupos = getUserGroups(request.user)
        if 'editor' not in grupos:
             return JsonResponse({"ok": False, "message": "No tienes permisos de editor", "data": []})

        body_data={}
        #CASO 1: form-data o x-www-form-urlencoded
        if request.POST:
            body_data = request.POST.dict()
        #CASO 2: raw json
        #Para obtener el diccionario del body de la petición
        else:
            body_data=json.loads(request.body)
        return JsonResponse(self.st.insert(body_data))
    
    #Llama a la función update del archivo stadiums_django.py dentro de la carpeta haikyuu_django de la appi
    def update(self, request, id):
        grupos = getUserGroups(request.user)
        if 'editor' not in grupos:
            return JsonResponse({"ok": False, "message": "No tienes permisos de editor", "data": []})

        body_data={}
        if request.POST:
            body_data = request.POST.dict()
        else:
            body_data=json.loads(request.body)
        return JsonResponse(self.st.update(body_data))    
    
    #Llama a la función delete del archivo stadiums_django.py dentro de la carpeta haikyuu_django de la appi
    def delete(self, request, id):
        grupos = getUserGroups(request.user)
        if 'editor' not in grupos:
            return JsonResponse({"ok": False, "message": "No tienes permisos de editor", "data": []})
        return JsonResponse(self.st.delete({'id': id}))