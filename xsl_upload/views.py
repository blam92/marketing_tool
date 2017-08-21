# -*- coding: utf-8 -*-
import sys
import os
from xsl_upload import app
from agrupador import agrupador
from flask import render_template, request, flash, redirect, url_for, make_response, send_from_directory
from werkzeug import secure_filename
import csv

ALLOWED_EXTENSIONS = set(['xls', 'csv', 'docx', 'xlsx'])
PATH_FOR_UPLOADS = 'xsl_upload/uploads'
PATH_FOR_DOWNLOAD = 'xsl_upload/download/grouped_key_words.csv'
app.secret_key = 'super_secret'

def allowed_file(filename):
	return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/upload_correct', methods = ['GET', 'POST'])
def upload_correct():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect('index')

		f = request.files['file']
		if f.filename == '':
			flash('Please upload a file')
			return redirect('index')
		if f and allowed_file(f.filename):
			filename = secure_filename(f.filename)
			f.save(os.path.join(PATH_FOR_UPLOADS, filename))
			path = PATH_FOR_UPLOADS + '/' + filename
			return download(path)
		else:
			flash('Please check the file extension. Accepted file types: xsl, csv')
			return redirect('index')
	return 'no post?'

@app.route('/download')
def download(file_path):
	agrupador(file_path)
	return send_from_directory(directory= 'download/', filename= 'grouped_key_words.csv')

def create_csv_string(dir_csv):
	csv_string = ''
	with open(dir_csv, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			csv_string += row[0] + ', ' + row[1] + '\n'
	return csv_string



