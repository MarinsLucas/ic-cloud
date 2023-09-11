from flask import Flask,render_template,request
import requests
import os
import pyvista
from io import StringIO
import shutil


app = Flask(__name__)
static_image_path = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = static_image_path


#faz o "get"
def make_request(secret_message, url):
    #url = 'https://25e2-34-29-3-38.ngrok-free.app/get_data'  # Substitua pelo URL fornecido pelo Ngrok
    url = url+"get_data"
    try:
        PARAMS = {'value': 2, 'message' :secret_message}
        response = requests.get(url, params=PARAMS, stream=True)
        if response.status_code == 200:
            #data = response.json()
            with open("temp.vtu", 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            return #data#['message']
        
        else:
            print("Erro na requisição:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Erro na conexão:", e)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/data/', methods = ['POST', 'GET'])
def data():
    form_data = request.form
    print(form_data.getlist('mensagem'))
    make_request(form_data['mensagem'], str(form_data['url']))
    reader = pyvista.read("temp.vtu")
    filename = 'cabo.png'
    filepath = os.path.join(static_image_path, filename)
    reader.plot(off_screen=True, window_size=(500,500), screenshot=filepath)
    print('/' + filepath.replace("\\", "/"))
    return render_template('data.html', image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)) #os.path.join('imagens', filename)

""" @app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        return render_template("data.html") """
 
app.run(host='localhost', port=5000, debug=True)