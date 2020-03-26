import requests
import openslide
import pycurl
from multiprocessing.pool import ThreadPool

FILE_FIELD = "file-location"
NAME_FIELD = "case_id"
URL = "http://172.20.11.223:9099/services/Camic_TCIA/Image/query/find"
IIP_BASE = "http://tcia-path-a1/fcgi-bin/iipsrv.fcgi?FIF="
IM_SIZE = 200
THREADS = 10

def gen_thumbnail(filename, slide, size, imgtype="png"):
    dest = filename + "." + imgtype
    print(dest)
    slide.get_thumbnail([size, size]).save(dest, imgtype.upper())

def process(record):
    file = record[FILE_FIELD]
    name = record[NAME_FIELD]
    try:
        slide = openslide.OpenSlide(file)
        gen_thumbnail(name, slide, IM_SIZE, imgtype="png")
        return ""
    except BaseException as e:
        try:
             url = IIP_BASE + file + "&WID=200&CVT=png"
             c = pycurl.Curl()
             c.setopt(c.URL, url)
             with open(name+".png", "wb") as f:
                 c.setopt(c.WRITEFUNCTION, f.write)
                 c.perform()
        except BaseException as y:
             return [name, y]

# do it
manifest = requests.get(URL).json()
print(manifest[0])

res = ThreadPool(THREADS).imap_unordered(process, manifest)
print([x for x in filter(None,[r for r in res])])
