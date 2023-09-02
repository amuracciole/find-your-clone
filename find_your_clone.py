import cv2
import face_recognition as fr
import os
import numpy as np
from datetime import datetime
import time
import shutil

# crear base de datos
ruta = '/Users/andresmuracciole/Desktop/Proyectos/find_your_clone/photos'
mis_imagenes = []
nombres_empleados = []
lista_empleados = os.listdir(ruta)

for nombre in lista_empleados:
    imagen_actual = cv2.imread(f'{ruta}/{nombre}')
    mis_imagenes.append(imagen_actual)
    nombres_empleados.append(os.path.splitext(nombre)[0])

# codificar imagenes
def codificar(imagenes):

    # crear una lista nueva
    lista_codificada = []

    # pasar todas las imagenes a rgb
    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        # codificar
        codificado = fr.face_encodings(imagen)[0]

        # agregar a la lista
        lista_codificada.append(codificado)

    # devolver lista codificada
    return lista_codificada

def checkExistingPhoto(lista_empleados_codificada, foto_codificada):
    print("Checking...")
    print(lista_empleados_codificada)
    #print("·······················")
    print(foto_codificada)
    # Variable para realizar la búsqueda
    encontrado = False

    # Iterar sobre la lista de arrays

    for array in lista_empleados_codificada:
        if np.array_equal(foto_codificada[0], array):
            print("El array está en la lista.")
            encontrado=True
            break
        else:
            print("El array no está en la lista.")
        return(encontrado)
    
def saveImage(image):
    print("Saving image...")
    directorio_destino = "/Users/andresmuracciole/Desktop/Proyectos/find_your_clone/photos/"
    personName = input("What is your name?: ")
    # Comprobar si el directorio de destino existe, si no, créalo
    if not os.path.exists(directorio_destino):
        print("dentro")
        os.makedirs(directorio_destino)
    ruta_copia = os.path.join(directorio_destino, personName + ".jpg")
    print(ruta_copia)
    print(image)
    shutil.copy(image, ruta_copia)

#Codifico las fotos que hay en la base de datos
lista_empleados_codificada = codificar(mis_imagenes)

#Tomo la foto de prueba para comparar
photo_test_list=[]
photo = "/Users/andresmuracciole/Desktop/Proyectos/find_your_clone/you_photo/Andres Muracciole.jpg"
photo_test = cv2.imread(photo)
photo_test_list.append(photo_test)
foto_codificada=codificar(photo_test_list)
#print("FOTO PRUEBA CODIFICADA")
#print(foto_codificada_2)

#Compruebo queesa foto ya no exista:
existing=checkExistingPhoto(lista_empleados_codificada, foto_codificada)
if existing == False:
    #Guardo la foto en la base de datos si no existe aún
    saveImage(photo)
else:
    print("La foto ya existe")

for x in foto_codificada:
    coincidencias = fr.compare_faces(lista_empleados_codificada, x)
    distancias = fr.face_distance(lista_empleados_codificada, x)

    #print(distancias, coincidencias)
    
    indice_coincidencia = np.argmin(distancias)

    # Mostrar coincidencias si las hay
    if distancias[indice_coincidencia] > 0.6:
        print("No tienes ningun clon")
    else:
        print("Hay coincidencia!")
        nombre = nombres_empleados[indice_coincidencia]
        print("Tu clon se llama: " + nombre)

        # Mostrar la imagen obtenida
        foto_clon_path=ruta+"/"+nombre+".jpg"
        foto_clon = cv2.imread(foto_clon_path)
        cv2.imshow("Tu clon:", foto_clon)

        #Para no cerrar enseguida
        cv2.waitKey(0)
