from flask import Flask, render_template, jsonify
from datetime import datetime

# List tempat menyimpan data dari setiap titik
db = [{
	'response': 'success',
    'id_server': 1,
    'date-modified': '2016-06-01 00:00:00.000000',
    'clients': [
        {'id_client': 1, 'merah': 0, 'hijau': 0, 'kuning': 0},
        {'id_client': 2, 'merah': 0, 'hijau': 0, 'kuning': 0},
        {'id_client': 3, 'merah': 0, 'hijau': 0, 'kuning': 0},
        {'id_client': 4, 'merah': 0, 'hijau': 0, 'kuning': 0}
    ]
}]

app = Flask(__name__)

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
