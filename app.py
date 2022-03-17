'''
ALUMNOS:
Elmer Aarón De la Peña López
Irving Iván Cano Paniagua
Ricardo Trillo Garcia
'''

from pydoc import doc
from flask import Flask, render_template, session, url_for, redirect,request
from flask_pymongo import PyMongo as pymongo
from pymongo import MongoClient
from bson import ObjectId
import pprint
import os


#INCIO DE SESION
username = input('Username: ')
password = input('Password: ')
os.system('clear')

boolFlag = True
secondBoolFlag = True
db = None
rol = None
items = {}
client = None

#INCIO DE SESION Y CREACION DE UNA INSTANCIA DE CLIENTE
try:
    client = MongoClient(f"mongodb://{username}:{password}@localhost:27017/")
except Exception as e:
    print(e)

#OBTENCION DEL ROL DEL USUARIO LOGGEADO Y OBTENCION DE LA BD QUE MANEJA
c = client.admin.get_collection('system.users')
cr = c.find({'user':username})
for thing in cr:
    items = thing
roles = items['roles']
dbAdmin = roles[0]['db']
rol = roles[0]['role']

#OBTENCION DE LOS NOMBRES DE BASES DE DATOS
dbNames = client.list_database_names()

#INICIO DE LA APP
while boolFlag:
    print(f'USERNAME:{username}                 adminAT:{dbAdmin}                               ROL:{rol}\n')
    option = int(input('\nSeleccione una opcion \nNo la escriba \n \n 1- Ver BD \n 2- Seleccionar Bd \n 3- Salir \n \n'))

    if option == 1:
        cont = 1
        os.system("clear")
        print(f'USERNAME:{username}                 adminAT:{dbAdmin}                               ROL:{rol}\n')
        for name in dbNames:            
            print(f'{cont}',name)
            cont+=1

        input('\nPresione una tecla para volver')
        os.system('clear')
    
    if option == 2:
        selectedDb = input('Escriba la BD que desea abordar: \n')
        if selectedDb in dbNames:
            try:
                db = client[selectedDb]
                collection = db['registros']
                print(f'{selectedDb} en uso \n')
                while secondBoolFlag:
                    os.system('clear')
                    print(f'USERNAME:{username}                 adminAT:{dbAdmin}                               ROL:{rol}\n')
                    cursor = collection.find({})
                    items = {}
                    item ={}
                    print('Users: \n')

                    for document in cursor:
                        items = document
                        pprint.pprint(document)

                    try:
                        items.pop('_id')
                    except:
                        print(items)
                    
                    item.items

                    opcion = int(input('\nSeleccione una opcion \nNo la escriba \n \n 1- Agregar registro \n 2- Eliminar registro \n 3- Volver \n \n'))
                    if opcion == 1:
                        record = {}
                        for i,k in items.items():
                            item[i]= input(f'Inserte el valor de {i}: ')
                            print(item)
                        try:
                            if len(items) != 0:
                                collection.insert_one(item)
                            else:
                                collection.insert_one({'address': 'test@test.com',
                                                        'apellido_1': 'trillo',
                                                        'apellido_2': 'garcia',
                                                        'city': 'Chihuahua',
                                                        'nombre': 'ricardo',
                                                        'password': '12345678@A',
                                                        'phone': '614-662-6262',
                                                        'state': 'Chihuahua',
                                                        'username': 'nword'})
                        except:
                            print('No se cuentan los privilegios necesarios')
                        
                        input('Se ha insertado un nuevo registro, presione una tecla para continuar')
                        os.system('clear')


                    if opcion == 2:
                        selectedUser = input('¿Que usuario desea eliminar por id? ')
                        try:
                            collection.delete_one({'_id':ObjectId(selectedUser)})
                            input('Se ha eliminado el usuario,presione una tecla para volver')                        
                        except Exception as e:
                            print(e)

                    if opcion == 3:
                        os.system("clear")
                        break

            except Exception as e:
                print(e)
        else:
            input('No existe la BD, presione una tecla para volver')
            os.system('clear')
    
    if option == 3:
        os.system("clear")
        break