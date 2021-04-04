import json
import tkinter
import requests
from tkinter import filedialog

root = tkinter.Tk()
root.withdraw()
pimg = filedialog.askopenfilename()

searchUrl = 'https://yandex.ru/images/search'
files = {'upfile': ('blob', open(pimg, 'rb'), 'image/jpeg')}
params = {'rpt': 'imageview', 'format': 'json', 'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
response = requests.post(searchUrl, params=params, files=files)
query_string = json.loads(response.content)['blocks'][0]['params']['url']
img_search_url= searchUrl + '?' + query_string
print(img_search_url)
