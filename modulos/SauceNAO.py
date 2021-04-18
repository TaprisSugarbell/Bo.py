import os
import string
import random
import urllib
import tkinter
import requests
import youtube_dl
from dotenv import load_dotenv
from selenium import webdriver
from tkinter import filedialog
from selenium.webdriver.common.keys import Keys


load_dotenv()
# Variables
key = os.getenv("key")
TOKEN = os.getenv("TOKEN")


def SearchSauceNAO():
    root = tkinter.Tk()
    root.withdraw()
    pimg = filedialog.askopenfilename()
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://saucenao.com/")

    img_upload = driver.find_elements_by_xpath("//input[@type='file']")
    img_upload[0].send_keys(pimg)

    search = driver.find_element_by_xpath("//input[@id='searchButton']")
    search.click()
    print("Cargando imagenes similares")


def Shortpy(short):
    print(short)
    alias = input("Ingresa alias - ")
    url = urllib.parse.quote(f"{short}")
    name = f"{alias}"
    r = requests.get(
        "http://cutt.ly/api/api.php?key={}&short={}&name={}".format(key, url, name)
    )
    data = r.json()["url"]
    if data["status"] == 7:
        sl = data["shortLink"]
        print("Link Acortado:", sl)
    else:
        print("[!] Error Acortando el Link:", data)


def Password():
    print("~~ Menú ~~")
    print("1. Alfabeto")
    print("2. Mayúsculas")
    print("3. Minúsculas")
    print("4. Números")
    print("5. Alfanumérico")
    print("6. Alfanumérico y Símbolos")

    s = ""
    mn = input("Ingresa parametros: ")
    afn = mn.split()
    m = int(afn[0])
    try:
        n = int(afn[1])
    except IndexError:
        n = 8

    if m == 1:
        c = list(string.ascii_letters)
    elif m == 2:
        c = list(string.ascii_uppercase)
    elif m == 3:
        c = list(string.ascii_lowercase)
    elif m == 4:
        c = list(string.digits)
    elif m == 5:
        c = list(string.hexdigits)
    elif m == 6:
        c = list(string.printable)
        c = c[:-6]

    for i in range(n):
        s += random.choice(c)

    print("Tu contraseña es:", s)


def mp3():
    """
    Esto es para pedir la dirección absoluta de una carpeta
    import tkinter
    from tkinter import filedialog
    root = tkinter.Tk()
    root.withdraw()
    op = filedialog.askdirectory()
    """

    # Pedimos la URL de input al usuario
    # input_url = input('Ingrese la URL del video que desea convertir: ')

    url = input("Ingresa URL - ")

    # Obtenemos el titulo del video
    video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
    video_title = video_info["title"]

    # Setear las opciones para la descarga del video
    opciones = {
        "format": "bestaudio/best",
        "outtmpl": f"C:/Users/sayu/Downloads/Music/{video_title}.mp3",  # Seteamos la ubicación deseada
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    # Descargar el Video
    with youtube_dl.YoutubeDL(opciones) as ydl:
        ydl.download([url])
