from flask import Flask,render_template,request
import requests
import os
import pyvista
from io import StringIO
import shutil


app = Flask(__name__)
static_image_path = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = static_image_path

def createIniInformation(data):
    ini = ""
    ini = ini + "[main]\n"
    ini = ini + "num_threads=" + str(data["num_threads"]) + '\n'
    ini = ini + "dt_pde=" + str(data["dt_pde"]) + "\n"
    ini = ini + "simulation_time=" + str(data["simulation_time"]) + "\n"
    ini = ini + "abort_on_no_activity=false\nuse_adaptivity=false\n\n"

    ini= ini + "[update_monodomain]\nmain_function=update_monodomain_default\n\n[save_result]"
    ini= ini + "\nprint_rate=" + str(data["print_rate"]) + '\n'
    ini= ini + "output_dir=./outputs/temp\n"
    ini= ini + "main_function=save_as_vtu\ninit_function=init_save_as_vtk_or_vtu\nend_function=end_save_as_vtk_or_vtu\nsave_pvd=true\nextra_function_1=save_vm_matrix\nfile_prefix=V\ncompress=false\nbinary=true\n"
    ini = ini + "\n[assembly_matrix]\n"
    ini = ini + "sigma_x=" + str(data["sigma_x"]) + '\n'
    ini = ini + "sigma_y=" + str(data["sigma_y"]) + '\n'
    ini = ini + "sigma_z=" + str(data["sigma_z"]) + '\n'
    ini = ini + "library_file=shared_libs/libdefault_matrix_assembly.so\nmain_function=homogeneous_sigma_assembly_matrix\ninit_function=set_initial_conditions_fvm\n"
    ini = ini + "\n[linear_system_solver]\ntolerance=1e-16\nuse_preconditioner=no\nuse_gpu=yes\nmax_iterations=200\nlibrary_file=shared_libs/libdefault_linear_system_solver.so\nmain_function=conjugate_gradient\ninit_function=init_conjugate_gradient\nend_function=end_conjugate_gradient\n"
    
    ini = ini + "\n[domain]\n"
    ini = ini + "name=" + str(data["domain_name"]) + '\n'
    ini = ini + "start_dx=" + str(data["start_dx"]) + '\n'
    ini = ini + "start_dy=" + str(data["start_dy"]) + '\n'
    ini = ini + "start_dz=" + str(data["start_dz"]) + '\n'
    ini = ini + "cable_length=" + str(data["cable_length"]) + '\n'
    ini = ini + "main_function=" + str(data["main_function_domain"]) + '\n'
    ini = ini + "[ode_solver]\ndt=0.02\nuse_gpu=yes\ngpu_id=0\nlibrary_file=./shared_libs/libten_tusscher_3_endo.so\n\n[stim_plain]\nstart = 1.0\nduration = 2.0\ncurrent = -38.0\nx_limit = 500.0\nmain_function=stim_if_x_less_than\nperiod=400.0\n\n[extra_data]\natpi=2.0\nKo=8.9\nVm_modifier=1.7\nGNa_multiplicator=0.875\nGCaL_multiplicator=0.875\nmain_function=set_extra_data_for_fibrosis_plain\n"

    return ini


def make_request(data):
    url = data['url']+"get_data"
    data = createIniInformation(data)
    print(data)
    try:
        PARAMS = {'ini': data}
        response = requests.get(url, params=PARAMS, stream=True)
        if response.status_code == 200:
            with open("temp.zip", 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            return 
        
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
    make_request(form_data)
    #mesh = pyvista.read("temp.vtu")
    """ filename = 'cabo.png'
    filepath = os.path.join(static_image_path, filename) """
    #reader.plot(off_screen=False, window_size=(500,500), screenshot=filepath)



    return render_template('data.html') 

 
app.run(host='localhost', port=5000, debug=True)