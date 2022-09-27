import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from PIL import Image, ImageOps
import numpy as np
import cv2
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io 
import tensorflow.keras
import numpy as np
from img_classifier import our_image_classifier, nilai_prediksi
import time
import sqlite3

st.set_page_config( 
layout="wide",  
initial_sidebar_state="auto",
page_title= "Deteksi Songket",
)

# db management
import sqlite3
conn = sqlite3.connect("data.db")
c = conn.cursor()



def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT, password TEXT)')

def add_userdata(username, password):
    c.execute('INSERT INTO usertable(username, password) VALUES (?,?)', (username, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM usertable WHERE username =? AND password =?', (username, password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data


def main():
    profile = Image.open("./Images/logo.png")
    st.sidebar.image(profile, width=300 )
    menu = ("Masuk", "Daftar")
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Masuk":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type= "password")
        if st.sidebar.checkbox("Login"):
            create_usertable()
            result = login_user(username, password)
            if result:
                st.info("Masuk sebagai {}".format(username))
                choose = option_menu("Menu", ["Home", "Identifikasi", "Jenis Motif", "Tentang", "TM Canny"],
                        icons=['house', 'camera fill', 'kanban','book','eye'],
                        menu_icon="cast", 
                        default_index=0, 
                        orientation="vertical",
                        styles={
                            "container": {"padding": "5!important", "background-color": "#f6cc53"},
                            "icon": {"color": "white", "font-size": "20px"}, 
                            "nav-link": {"font-size": "14px", "color":"white", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
                            "nav-link-selected": {"background-color": "black"},
                        }
                )
                if choose == "Home":
                    profile = Image.open("./Images/logo.png")
                    col1, col2 = st.columns( [0.8, 0.2])
                    with col1:               # To display the header text using css style
                        st.markdown(""" <style> .font {
                        font-size:35px ; font-family: 'Cooper Black'; color: #f6cc53;} 
                        </style> """, unsafe_allow_html=True)
                        st.markdown('<p class="font">Penerapan Metode Deteksi Tepi Canny Dan Template Matching Pada Pengenalan Motif Songket Aceh</p>', unsafe_allow_html=True)    

                    with col2: 
                        st.image(profile, width=200 )
                        
                # menu indentifikasi    
                elif choose == "Identifikasi":
                    st.subheader("Upload Gambar:")
                    uploaded_file = st.file_uploader(
                        "Pilih gambar dari direktori kamu...", 
                        type=["jpg", "jpeg", "png", "bmp"]
                    )

                    # Thresholds
                    st.subheader("Terapkan thresholding:")
                    low_thresh = st.number_input(
                        "Masukkan nomor untuk threshold bawah (bawaan=15)."
                    )
                    upper_thresh = st.number_input(
                        "Masukkan nomor untuk threshold atas (bawaan=200)."
                    )
                    # Detect edges button
                    edge_button = st.button("Deteksi")
                    # App development info
                    st.markdown(
                        "Dibuat oleh Nurul Fatani"
                    )

                    # Original image
                    if uploaded_file is None:
                        image = Image.open("./Images/demo.jpg")
                        st.image (image, caption="Gambar demo", width=300)
                    else:
                        image = Image.open(uploaded_file)
                        st.image (image, caption="Gambar yang diupload", width=300)


                    # Edge Image
                    if edge_button:
                        array = np.asarray(image)
                        gray = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
                        blurry = cv2.GaussianBlur(gray, (5, 5), 0)
                        if low_thresh == 0 and upper_thresh == 0:
                            edged = cv2.Canny(blurry, 15, 200)
                        else:
                            edged = cv2.Canny(blurry, low_thresh, upper_thresh)
                        st.image(edged, caption="Gambar Canny", width=300)
                        st.write("")
                        try:
                            with st.spinner("Mendeteksi...."):
                                label = our_image_classifier(image)
                                nilaiprediksi = nilai_prediksi(image)
                                time.sleep(8)
                            st.success("Motifnya adalah: "+label)
                            st.markdown("Nilai deteksi: "+nilaiprediksi+" x 100")
                            st.markdown('Urutan nilai prediksi = Bungog Delima, Bungong Meulu 1, Bungong Meulu 2, Bungong Meurante, Pinto Aceh, Pucok Mueria, Tidak dikenali')
                        except:
                            st.error("Maaf ada yang salah 🙇🏽‍♂️")

                        
                        # Download button
                        im = Image.fromarray(edged)
                        im.save("Edge_image.png")
                        with open("Edge_image.png", "rb") as file:
                            btn = st.download_button(
                                    label="Download Image",
                                    data=file,
                                    file_name="Edge_image.png",
                                    mime="image/png"
                                )
                # Menu jenis motif
                elif choose == "Jenis Motif":
                #Add a file uploader to allow users to upload their project plan file
                    st.markdown(""" <style> .font {
                    font-size:35px ; font-family: 'Cooper Black'; color: #f6cc53;} 
                    </style> """, unsafe_allow_html=True)
                    st.markdown('<p class="font">Jenis Motif Pada Songket Aceh</p>', unsafe_allow_html=True)
                    st.markdown('Pada program ini terdapat 5 jenis kain songket Aceh Nyakmu, diantaranya:')
                    col1,col2,col3= st.columns(3)
                    with col1:st.write("")
                    with col2:
                            st.markdown('1. Bungong Delima')
                            path_img1_jpg = r"./Images/delima.jpg"
                            st.image(path_img1_jpg, width=300, caption="Bungong Delima")
                            st.markdown('2. Bungong Meulu')
                            path_img2_jpg = r"./Images/meulu.jpg"
                            st.image(path_img2_jpg, width=300, caption="Bungong Meulu")
                            st.markdown('3. Bungong Meurante')
                            path_img3_jpg = r"./Images/meurante.jpg"
                            st.image(path_img3_jpg, width=300, caption="Bungong Meurante")
                            st.markdown('4. Pinto Aceh')
                            path_img4_jpg = r"./Images/pinto aceh.jpg"
                            st.image(path_img4_jpg, width=300, caption="Pinto Aceh")
                            st.markdown('5. Pucok Meuria')
                            path_img6_jpg = r"./Images/pucok meuria.jpg"
                            st.image(path_img6_jpg, width=300, caption="Pucok Meuria")
                    with col3:st.write("")
                # halaman tentang
                elif choose == "Tentang":
                    col1, col2 = st.columns( [0.8, 0.2])
                    with col1:               # To display the header text using css style
                        st.markdown(""" <style> .font {
                        font-size:35px ; font-family: 'Cooper Black'; color: #f6cc53;} 
                        </style> """, unsafe_allow_html=True)
                        st.markdown('<p class="font">Biodata</p>', unsafe_allow_html=True)    
                    with col2: 
                        st.image("./Images/foto_about.jpeg", width=200 )
                    col1,col2,col3= st.columns(3)
                    with col1:st.write('')
                    with col2:
                        st.markdown('Nama :  Nurul Fatani')
                        st.markdown('Nim: 1857301060')
                        st.markdown('Tempat lahir : Gampong u blang asan')
                        st.markdown('Tgl lahir : 10 mei 2001')
                        st.markdown('No hp : 082161449439')
                        st.markdown('Email : nurulfatani3@gmail.com')
                        st.markdown('Prodi : Teknik informatika')
                        st.markdown('Jenis kelamin : perempuan')
                    with col3:st.write('')
                    
                    
                #Menu Template Matching
                elif choose == "TM Canny":
                    st.markdown(""" <style> .font {
                    font-size:35px ; font-family: 'Cooper Black'; color: #f6cc53;} 
                    </style> """, unsafe_allow_html=True)
                    st.markdown('<p class="font">Template Matching dengan Edge Detection Canny</p>', unsafe_allow_html=True)
                    
                    st.subheader("Upload Gambar dan Template:")
                    uploaded_file = st.file_uploader(
                        "Pilih gambar dari direktori kamu...", 
                        type=["jpg", "jpeg", "png", "bmp"]
                    )
                    
                    template_file = st.file_uploader(
                        "Pilih template dari direktori kamu...", 
                        type=["jpg", "jpeg", "png", "bmp"]
                    )

                    # Thresholds
                    st.subheader("Terapkan thresholding:")
                    low_thresh = st.number_input(
                        "Masukkan nomor untuk threshold bawah (bawaan=15)."
                    )
                    upper_thresh = st.number_input(
                        "Masukkan nomor untuk threshold atas (bawaan=200)."
                    )
                    
                    if uploaded_file is not None:
                        image = Image.open(uploaded_file)
                        st.image (image, caption="Gambar yang diupload", width=300)
                        st.subheader("Nilai Array Gambar Sebelum Canny")
                        st.write(np.asarray(image))
                    else:
                        st.error("Upload gambar terlebih dahulu 🙇🏽‍♂️")
                        
                            
                    if template_file is not None:                   
                        image_template = Image.open(template_file)
                        st.image (image_template, caption="Gambar template", use_column_width=True, width=200)
                        image_template.save("template.png")
                        st.subheader("Nilai Array Gambar Template Sebelum Canny")
                        st.write(np.asarray(image_template ))
                    else:
                        st.error("Upload gambar template terlebih dahulu 🙇🏽‍♂️")  

                    tm_button = st.button("Template Matching")
                    
                    if tm_button:
                        array = np.asarray(image)
                        if low_thresh == 0 and upper_thresh == 0:
                            edged = cv2.Canny(array, 15, 200)
                        else:
                            edged = cv2.Canny(array, low_thresh, upper_thresh)
                        st.subheader("Hasil Gambar Edge Detection Canny:")
                        st.image(edged, caption="Gambar Canny", width=300)
                        st.write("")
                        st.subheader("Nilai Array Gambar Canny")
                        st.write(np.asarray(edged))
                        st.write("")
                        
                        # template = cv2.imread("./Images/template_demo.jpg",0)
                        template = cv2.imread("template.png",0)
                        if low_thresh == 0 and upper_thresh == 0:
                            edged_template = cv2.Canny(template, 15, 200)
                        else:
                            edged_template = cv2.Canny(template, low_thresh, upper_thresh)
                            
                        st.subheader("Nilai Array Gambar Template")
                        st.image(edged_template, caption="Gambar Template Canny")
                        st.write(np.asarray(edged_template)) 
                        st.write("") 
                        w, h = template.shape[::-1]        
                        res = cv2.matchTemplate(edged,edged_template,cv2.TM_CCOEFF_NORMED)
                        (_, max_val, _, max_loc) = cv2.minMaxLoc(res)
                        
                        # Specify a threshold
                        threshold = 0.2
                        loc = np.where( res >= threshold)
                        for pt in zip(*loc[::-1]):
                            cv2.rectangle(array, pt, (pt[0] + w, pt[1] + h), (255,0,0), 2)
                        st.image(array, caption="Gambar Template terdeteksi atau tidak")
                        st.write("")            

                    
    elif choice == "Daftar":
        st.subheader("Silahkan Buat Akun Baru")
        new_username = st.sidebar.text_input("User Name")
        new_password = st.sidebar.text_input("Password", type= "password")

        if st.sidebar.button("Daftar"):
            create_usertable()
            add_userdata(new_username, new_password)
            st.success("Anda telah berhasil membuat akun")
            st.info("Buka Menu Masuk untuk Masuk")


if __name__ == "__main__":
    main()