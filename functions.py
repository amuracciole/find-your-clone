import cv2
import face_recognition as fr
import os
import numpy as np
from PIL import Image

# crear base de datos
main_path = '/Users/andresmuracciole/Desktop/Proyectos/find_your_clone/photos'
secondary_path = '/Users/andresmuracciole/Desktop/Proyectos/find_your_clone/you_photo'
photo = "/Users/andresmuracciole/Desktop/Proyectos/find_your_clone/you_photo/photo.jpg"
people_names = []
your_photo_list=[]
quality_num=40

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

#Encode list of images
def encode_complete_list(path):
    my_images = []
    people = os.listdir(path)
    for person in people:
        current_photo = cv2.imread(f'{path}/{person}')
        my_images.append(current_photo)
        people_names.append(os.path.splitext(person)[0])
    
    # Encode photos in data base
    my_images = encode(my_images)
    """
    os.chdir("/Users/andresmuracciole/Desktop/Proyectos/find_your_clone")
    file_encode_list=open("encode_list.py", "a")
    file_encode_list.write(str(my_images))
    file_people_name_list=open("name_list.py", "a")
    file_people_name_list.write(str(people_names))
    """
    return(my_images, people_names)

#Check if photo already exist
def checkExistingPhoto(people_encode_list, enconded_photo):
    found = False

    for array in people_encode_list:
        if np.array_equal(enconded_photo[0], array):
            found=True
            break
    return(found)
    
#Save image in case photo does not exits
def saveImage(image, name):
    #print("Saving image...")
    #main_path = "/Users/andresmuracciole/Desktop/Proyectos/find_your_clone/photos/"
    #personName = input("What is your name?: ")
    personName = name
    # Chack if path exists, if not, create it
    if not os.path.exists(main_path):
        os.makedirs(main_path)
    copy_path = os.path.join(main_path, personName + ".jpg")
    #shutil.copy(image, copy_path)
    img = Image.open(image)
    img.save(copy_path, optimize=True, quality=quality_num)

#Delete DS_Store files
def delete_files(path, file_name):
    file_list = os.listdir(path)

    for file in file_list:
        if file.endswith(file_name):
            ruta_completa = os.path.join(path, file)         
            try:
                os.remove(ruta_completa)
            except Exception as e:
                #print(f"No {file}: {e}")
                continue

def resize_photo():
    img = Image.open(photo)
    img.save(photo, optimize=True, quality=quality_num)
    
############################
############################
def mainFunction(personName):
    delete_files(main_path, ".DS_Store")
    delete_files(secondary_path, ".DS_Store")

    people_encode_list, people_names = encode_complete_list(main_path)

    #Check if photo is already in the list
    resize_photo()
    photo_read = cv2.imread(photo)
    your_photo_list.append(photo_read)
    encoded_photo=encode(your_photo_list)


    #Check if photo already exist
    existing=checkExistingPhoto(people_encode_list, encoded_photo)
    if existing == False:
        saveImage(photo, personName)

    for x in encoded_photo:
        matches = fr.compare_faces(people_encode_list, x)
        distance = fr.face_distance(people_encode_list, x)

        #Distance -> number betwen 0 and 1
        #Matches -> Return True or False
        #print(distance, matches)
        
        matches_index = np.argmin(distance)

        if distance[matches_index] > 0.6:
            return("Sorry. You don´t have a clone... yet")
            #print("Sorry. You don´t have a clone... yet")
        else:
            name = people_names[matches_index]
            #print("Your clone name is: " + name)

            # Show image
            photo_clon_path=main_path+"/"+name+".jpg"
            photo_clon = cv2.imread(photo_clon_path)
            cv2.imshow("Your clon: " + name, photo_clon)

            #Avoid closing windows automatically. Waiting until press a key
            cv2.waitKey(0)
            return("Your clone name is: " + name)
