# -*- coding: utf-8 -*-
import sys
import os
from xsl_upload import app
from flask import render_template, request, flash, redirect, url_for, make_response
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['xsl', 'csv', 'docx'])
PATH_FOR_UPLOADS = 'xsl_upload/uploads'
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
		flash('')
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
			path = PATH_FOR_UPLOADS + filename
			return download(path)
		else:
			flash('Please check the file extension. Accepted file types: xsl, csv')
			return redirect('index')
	return 'no post?'

@app.route('/download')
def download(file_path):
	csv = 'foo, ' + file_path
	response = make_response(csv)
	cd = 'attachment; filename=key_words.csv'
	response.headers['Content-Disposition'] = cd
	response.mimetype = 'text/csv'
	return response