import cv2
import face_recognition as fr

#Cargar imagenes
foto_control = fr.load_image_file("/Users/andresmuracciole/Desktop/Proyectos/find-your-clone/Fotos/Cosmo Kramer.jpg")
foto_prueba = fr.load_image_file("/Users/andresmuracciole/Desktop/Proyectos/find-your-clone/George Constanza.jpg")

#pasar imagenes a RGB
foto_control=cv2.cvtColor(foto_control,cv2.COLOR_BGR2RGB)
foto_prueba=cv2.cvtColor(foto_prueba,cv2.COLOR_BGR2RGB)

#Localizar caras control
lugar_cara_control=fr.face_locations(foto_control)[0]
lugar_cara_prueba=fr.face_locations(foto_prueba)[0]

#Codificar cara
cara_codificada_control = fr.face_encodings(foto_control)[0]
cara_codificada_prueba = fr.face_encodings(foto_prueba)[0]

#Crear rectangulo con la foto
cv2.rectangle(foto_control,
              (lugar_cara_control[3], lugar_cara_control[0]),
              (lugar_cara_control[1], lugar_cara_control[2]),
              (0,255,0),
              2)

cv2.rectangle(foto_prueba,
              (lugar_cara_prueba[3], lugar_cara_prueba[0]),
              (lugar_cara_prueba[1], lugar_cara_prueba[2]),
              (0,255,0),
              2)

#realizar comparacion
resultado=fr.compare_faces([cara_codificada_control], cara_codificada_prueba)
print(resultado)


#mostrar imagenes
cv2.imshow("Foto Control", foto_control)
cv2.imshow("Foto Prueba", foto_prueba)

#Para no cerrar enseguida
cv2.waitKey(0)