# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 09:00:54 2020

@author: neete
"""

import os
from flask_bootstrap import Bootstrap
from preprocessing import text_preprocessing 
from custom_search import getResult
from similarity import findSimByTfCos
from pycode_simi import processpyfiles
from text_similarity import sentence_similarity
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

# Initialicze the Flask application
app = Flask(__name__)
Bootstrap(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

files_path=os.path.join(BASE_DIR,'uploaded_files')
#files_path=r"C:\Windows\System32\virtual_workspace\demo_project\demo_project\spiders\uploaded_files"
path=os.path.join(BASE_DIR,'uploaded_query_file')
#path=r"C:\Windows\System32\virtual_workspace\demo_project\demo_project\spiders\uploaded_query_file"
pypath=os.path.join(BASE_DIR,'temp_py_file')
#pypath = r'C:\Windows\System32\virtual_workspace\demo_project\demo_project\spiders\temp_py_file'

cmp_query_folder_name=''
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'py'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



#
## Route that will process the file upload
#@app.route('/uploadfiles', methods=['POST'])
           
#method to upload files from folder
def uploadfiles(request):
    app.config['UPLOAD_FOLDER'] = files_path
    for file in os.listdir(files_path):
        os.remove(files_path+"\\"+file)
   
    uploaded_files = request.files.getlist("files[]")
    print("len",len(uploaded_files))
    filenames = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
    return find_similarity()
    
    

    



#@app.route('/uploadqueryfile', methods=['POST'])
#method used to upload a file that is used to find similarity from files(folder)
def uploadqueryfile(request):
    global cmp_query_file_name
    app.config['UPLOAD_FOLDER'] = path
    for file in os.listdir(path):
        os.remove(path+"\\"+file)
    if request.method == 'POST':
        file = request.files['upfile']
        print("fil name "+file.filename)
        cmp_query_file_name = ""+file.filename
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "query file sucessfully upload"
    
    
    
 # method to find similarity of a file among multiple files   
def find_similarity():
    file_text=[]
    raw_files=os.listdir(path)
    for file in raw_files:
        fp = open(path+'\\'+file,encoding="utf8")
        filetext = fp.readlines()
        fp.close()
        file_text.append(text_preprocessing(" ".join(filetext)))
    raw_files=os.listdir(files_path)
    for file in raw_files:
        fp = open(files_path+'\\'+file,encoding="utf8")
        filetext = fp.readlines()
        file_text.append(text_preprocessing(" ".join(filetext)))
    fp.close()
    result = raw_files[findSimByTfCos(file_text)]
    if result!= 1000: 
        val = -1
        for i in range(0, 2): 
            val = result.find('_', val + 1) 
        return render_template("cmp_files.html", file_name=cmp_query_file_name,folder_name=result[:val],result = cmp_query_file_name+" is similar to "+result[val+1:])
    else:
        return render_template("cmp_files.html", file_name=cmp_query_file_name,folder_name=result[:val],result = "plagiarised");
    
    


#url to find source website from internet
@app.route('/uploadText', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      data_from_client = request.form['uptext']
      result_url=getResult(data_from_client[:280])
      return render_template("search_online.html",result = result_url);
		

#url to compare file from folder
@app.route('/upload', methods=['POST'])
def upload():
    uploadqueryfile(request)
    return uploadfiles(request)
   
  
    
#url to find python code similarity among mutiple python source code files
@app.route('/uploadpythonfile', methods=['POST'])
def uploadpythonfile():
    app.config['UPLOAD_FOLDER'] = pypath
    for file in os.listdir(pypath):
        os.remove(pypath+"\\"+file)
    if request.method == 'POST':
       file = request.files['upfile']
       if file.filename == '':
           return render_template("python_plag.html",result="please select file");

       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           return render_template("python_plag.html",result=processpyfiles());
       return render_template("python_plag.html",result="SOMETHING WENT WRONG PLESE RELOAD THE PAGE");
        
    


#url to find similarity between text files
@app.route('/uploadtxtfiles', methods=['POST'])
def uploadtxtfiles():
    if request.method == 'POST':
        text1 = request.form['text1']
        text2 = request.form['text2']
        if len(text1)==0:
            return "insufficient data in textarea1"
        elif len(text2)==0:
            return "insufficient data in textarea2"
        #return sentence_similarity(text1,text2)
        return render_template("text_similarity.html", result = "similarity between given texts is "+str(sentence_similarity(text1,text2))+"%");
  

#flask main method 
if __name__ == '__main__':
    app.run(
#        debug=True,
        port=3000
        
   )
    