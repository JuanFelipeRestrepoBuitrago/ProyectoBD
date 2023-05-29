from .models import *
def buscar_estudiante_documento(documento):
    pipeline = [
      {'$match': {'documento_identidad' : int(documento)}}
    ]

    return pipeline

def next_id(modelo):
    pipeline = [
    {'$group': {'_id': 'null', 'maxId': { '$max': "$id_estudiante"}}},
    {'$project': {'nextId': { '$add': ["$maxId", 1]}}}
    ]
    siguiente_id = -1

    if modelo == 'Estudiantes':
        resultados = Estudiantes.objects.aggregate(pipeline)
    else: raise SyntaxError

    for resultado in resultados:
        siguiente_id = resultado['nextId']

    if siguiente_id == -1: raise SyntaxError

    return  siguiente_id


