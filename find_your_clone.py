import cv2
import face_recognition as fr
import os
import numpy as np
import shutil

# crear base de datos
main_path = '/Users/andresmuracciole/Desktop/Proyectos/find_your_clone/photos'
my_images = []
people_names = []
your_photo_list=[]

# Encode images
def encode(images):
    encode_list = []

    # Images to rgb
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Enconding
        encode = fr.face_encodings(image)[0]

        # Add to list
        encode_list.append(encode)

    return encode_list

#Check if photo already exist
def checkExistingPhoto(people_encode_list, enconded_photo):
    #print(people_encode_list)
    #print(enconded_photo)
    found = False

    for array in people_encode_list:
        if np.array_equal(enconded_photo[0], array):
            found=True
            break
        return(found)
    
#Save image in case photo does not exits
def saveImage(image):
    print("Saving image...")
    #main_path = "/Users/andresmuracciole/Desktop/Proyectos/find_your_clone/photos/"
    personName = input("What is your name?: ")
    # Chack if path exists, if not, create it
    if not os.path.exists(main_path):
        os.makedirs(main_path)
    copy_path = os.path.join(main_path, personName + ".jpg")
    shutil.copy(image, copy_path)


############################
############################

people = os.listdir(main_path)

for person in people:
    current_photo = cv2.imread(f'{main_path}/{person}')
    my_images.append(current_photo)
    people_names.append(os.path.splitext(person)[0])
  
# Encode photos in data base
people_encode_list = encode(my_images)

#Check if photo is already in the list
photo = "/Users/andresmuracciole/Desktop/Proyectos/find_your_clone/you_photo/Andres_Muracciole.jpg"
photo_read = cv2.imread(photo)
your_photo_list.append(photo_read)
encoded_photo=encode(your_photo_list)

#Check if photo already exist
existing=checkExistingPhoto(people_encode_list, encoded_photo)
if existing == False:
    saveImage(photo)

for x in encoded_photo:
    matches = fr.compare_faces(people_encode_list, x)
    distance = fr.face_distance(people_encode_list, x)

    #print(distance, matches)
    
    matches_index = np.argmin(distance)

    if distance[matches_index] > 0.6:
        print("Sorry. You don´t have a clone... yet")
    else:
        name = people_names[matches_index]
        print("Your clone name is: " + name)

        # Show image
        photo_clon_path=main_path+"/"+name+".jpg"
        photo_clon = cv2.imread(photo_clon_path)
        cv2.imshow("Tu clon:", photo_clon)

        #Avoid closing windosw automatically. Waiting until press a key
        cv2.waitKey(0)
