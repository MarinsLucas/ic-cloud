from Flask import Flask,render_template,request
import requests
 
app = Flask(__name__)

#faz o "get"
def make_request(secret_message, url):
    #url = 'https://25e2-34-29-3-38.ngrok-free.app/get_data'  # Substitua pelo URL fornecido pelo Ngrok
    url = url+"get_data"
    try:
        PARAMS = {'value': 2, 'message' :secret_message}
        response = requests.get(url, params=PARAMS)
        if response.status_code == 200:
            data = response.json()
            return data['message']
        else:
            print("Erro na requisição:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Erro na conexão:", e)

@app.route('/')
def form():
    return render_template('form.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        print(form_data.getlist('mensagem'))
        return make_request(form_data['mensagem'], str(form_data['url']))
 
 
app.run(host='localhost', port=5000, debug=True)