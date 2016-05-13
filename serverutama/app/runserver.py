from flask import Flask, render_template, request, jsonify
from datetime import datetime

# List tempat menyimpan data dari setiap titik
db = [
    {
		'response': 'success',
        'id_server': 1,
        'date-modified': '2016-05-19 16:09:17.564000',
        'clients': [
            {'id_client': 1, 'merah': 30, 'hijau': 20, 'kuning': 10},
            {'id_client': 2, 'merah': 0, 'hijau': 0, 'kuning': 0},
            {'id_client': 3, 'merah': 0, 'hijau': 0, 'kuning': 0},
            {'id_client': 4, 'merah': 0, 'hijau': 0, 'kuning': 0}
        ]
    },
    {
		'response': 'success',
        'id_server': 2,
        'date-modified': 'str(datetime.now())',
        'clients': [
            {'id_client': 1, 'merah': 0, 'hijau': 0, 'kuning': 0},
            {'id_client': 2, 'merah': 0, 'hijau': 0, 'kuning': 0},
            {'id_client': 3, 'merah': 0, 'hijau': 0, 'kuning': 0},
            {'id_client': 4, 'merah': 0, 'hijau': 0, 'kuning': 0}
        ]
    },
]

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')

# @app.route('/delete/<int:id>', methods=['POST'])
# def delete():
# 	""" Menghapus titik yang telah terdaftar """
# 	pass
#
# @app.route('/add/' methods=['POST'])
# def add():
# 	""" Menambahkan titik lampu merah yang akan di monitoring """
# 	titik = {'titik': 1, 'jalur': [{'merah': 10, 'hijau': 5, 'kuning': 5}]
# 	clients.append(titik)
# 	pass
#
# @app.route('/edit/<int:id>' methods=['POST'])
# def edit():
# 	""" Mengedit titik lampu merah yang terdapat di database """
# 	pass


""" Show data API """
@app.route('/data/<int:id_server>/', methods=['GET'])
def get_data(id_server):
	""" Menampilkan data dalam bentuk JSON """
	is_exist = False
	for database in db:
		if database['id_server'] == id_server:
			is_exist = True
			return jsonify(database)
	if is_exist == False:
		return jsonify({'response': 'error'})

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
