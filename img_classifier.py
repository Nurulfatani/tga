#pemanggilan library
import numpy as np
import tensorflow.keras
from PIL import Image, ImageOps
import time

def our_image_classifier(image):#kelas yang dipanggil
    '''
            Function that takes the path of the image as input and returns the closest predicted label as output
            '''
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)
    # Load the model
    model = tensorflow.keras.models.load_model(#memuat model
        'songket.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)#pemrosesan gambar menggunakan np.ndarray dan resize menjadi (224, 224px)perkecil gambar
    size = (224, 224) #guna resize adalah untuk meringankan proses deteksi dan menyamakan dengan model training (karena model training juga menggunakan gambar 224x224px)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (#normalisasi mengurangi noise atau bagian yang tidak diperlukan pada gambar
        image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array # pendefinisian data{0} menjadi gambar hasil normalisasi
    #pendefinisian label
    labels = {0: "Bungong Delima", 1: "Bungong Meulu 1", 2 : "Bungong Meulu 2", 3 :"Bungong Meurante", 4 :"Pinto Aceh", 5 :"Pucok Mueria", 6 :"Tidak dikenali"}
    predictions = model.predict(data).tolist()#bagian prediksi (model.predict) sudah ditraining. (data)merupakan gambar inputan yang sudah dinormalisasi. 
    best_outcome = predictions[0].index(max(predictions[0]))
    print(labels[best_outcome])#print label kelas yang paling mirip(0,1,2,3,4,5 menjadi bungong delima/meulu/dst.)
    return (labels[best_outcome])

def nilai_prediksi(image):
    '''
            Function that takes the path of the image as input and returns the closest predicted label as output
            '''
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)
    # Load the model
    model = tensorflow.keras.models.load_model(
        'songket.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (
        image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    predictions = model.predict(data).tolist()
    nilai=np.array(predictions)
    listToStr = ' ' .join([str(elem) for elem in nilai])
    print(listToStr)
    return (listToStr)