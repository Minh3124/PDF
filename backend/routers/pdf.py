from os import listdir
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from PyPDF2 import PdfFileReader, PdfFileMerger, PdfFileWriter
import PyPDF2 as pdf2
import requests
from typing import Optional, List
from pydantic import BaseModel
import json
from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from fpdf import FPDF
import webbrowser
import urllib.request


BASE_URL = "http://localhost:1337"
VALID_HOST_URL = "/upload"
VERTICAL_REDACTION_OFFSET = 0  # -0.5

router = APIRouter()


# mergePDF()
class Document:

    def __init__(self):
        self.api_url = "http://localhost:1337"

    def all(self):
        r = requests.get(self.api_url + "/documents")
        return r.json()
    def doc(self,id):
        r = requests.get(self.api_url + "/documents/"+str(id))

    def create(self, params):
        r = requests.post(self.api_url + "/documents",
                          data=json.dumps({
                              'file_name': params["file_name"],
                              'add_prefix_page': params["add_prefix_page"],
                              'file':params['file']
                          }),
                          headers={
                              'Content-Type': 'application/json'
                          })

    def update(self, id, params):
        r = requests.put(self.api_url + "/documents/" + str(id),
                         data=json.dumps({
                             'add_prefix_page': params["add_prefix_page"]
                         }),
                         headers={
            'Content-Type': 'application/json'
        })

class MergePDFs:

    def __init__(self):
        self.api_url = "http://localhost:1337"

    def all(self):
        r = requests.get(self.api_url + "/merge-pd-fs")
        return r.json()
    def doc(self,id):
        r = requests.get(self.api_url + "/merge-pd-fs/"+str(id))

    def create(self, params):
        r = requests.post(self.api_url + "/merge-pd-fs",
                          data=json.dumps({
                              'merge_file': params["merge_file"]

                              
                          }),
                          headers={
                              'Content-Type': 'application/json'
                          })


@router.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/upload")
async def create_upload_multiple_files(files: List[UploadFile] = File(...)):

    myfiles= []
    for file in files:
        filetuple = ('files', (file.filename, await file.read(), 'application/pdf'))
        myfiles.append(filetuple)
    response= requests.post(BASE_URL+VALID_HOST_URL,{'Content-Type':'application/form-data'} ,files=myfiles)  
    print(response.json()[0]['name'])
    for r in response.json():
        data = {'file_name':r['name'],'file': r,'add_prefix_page':False}
        docu= Document()
        docu.create(data)

    return files


@router.post("/uploadfile/")
async def create_upload_single_file(file: UploadFile = File(...)):
    files = [('files', (file.filename, await file.read(), 'application/pdf'))]
    response2 = requests.post(BASE_URL+VALID_HOST_URL, {'Content-Type':'application/form-data'}, files=files)
    print(response2.json()[0]['url'])
    data = {'file_name':file.filename,'file': response2.json(),'add_prefix_page':False}
    docu= Document()
    print(docu.create(data))
    return data


@router.delete("/upload/files/")
async def delete(id): 
    return requests.delete('http://localhost:1337/upload/files/',param ={'id': id})

@router.post("/PDF/merge/")
# input_dir = "D:/Final project/frontend/test_pdfs/"
async def merge_PDF(selectedid: List[int]):
    docu = Document()
    merger = PdfFileMerger()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(200,10, txt ="Table of content", ln=1, align='C')
    x=2
    for id in selectedid:
        response = requests.get('http://localhost:1337/documents/'+str(id))
        name = response.json()['file_name']

        pdf.cell(200,10, txt =response.json()['file_name'], ln=x, align='L')
        download_file(BASE_URL+response.json()['file'][0]['url'],name)
        print(response.json()['add_prefix_page'])
        if (response.json()['add_prefix_page']== True):
            add_page(name, name)
            merger.append("prefix.pdf")
        

        merger.append(name)
        x=x+1
    
    pdf.output("hello.pdf")
    merger.append("hello.pdf")

    

    merger.write("D:/Final project/frontend/test_pdfs/test/merger.pdf")
    merger.close()

    files = {'files': ("merger.pdf",open('D:/Final project/frontend/test_pdfs/test/merger.pdf', 'rb') , 'application/pdf')}

    response1 = requests.post(BASE_URL+VALID_HOST_URL, {'Content-Type':'application/form-data'}, files=files )
    
    data = {'merge_file': response1.json()}

    
    mergefile = MergePDFs()
    mergefile.create(data)

    return response1.json()
    
# async def merge_PDF(files: List[UploadFile] = File(...)):

#     merger = PdfFileMerger()

#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size = 15)
#     pdf.cell(200,10, txt ="Table of content", ln=1, align='C')
#     for file in files:   
#         pdf.cell(200,10, txt =file.filename, ln=files.index(file)+1, align='L')

#     pdf.output("hello.pdf")
    
#     merger.append("hello.pdf")

#     for file in files:   
#         merger.append(file.file)
    

#     merger.write("D:/Final project/frontend/test_pdfs/test/merger.pdf")
#     merger.close()
#     files = {'files': ("merger.pdf",open('D:/Final project/frontend/test_pdfs/test/merger.pdf', 'rb') , 'application/pdf')}

#     response = requests.post(BASE_URL+VALID_HOST_URL, {'Content-Type':'application/form-data'}, files=files )


#     return files

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)    
    file = open(filename, 'wb')
    file.write(response.read())
    file.close()
 

def add_page(name,filename):
    pdf = FPDF()
    merger= PdfFileMerger()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(200,10, txt = filename, ln=1, align='C')
    pdf.output("prefix.pdf")
    merger.append("prefix.pdf")
    merger.append(name)
    merger.write("pp.pdf")


def splitIntoBundles(file, bundleSize):

    # get parameter from frontend- bundle size: if count page-> mb <= bundlesize= split put into another pdf <remember which documents was use to merge into the big bundles>=> continue with the rest
    pdf = PdfFileReader(file)

