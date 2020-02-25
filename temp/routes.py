from flask import render_template, request, Blueprint, redirect, url_for, flash, send_from_directory

temp = Blueprint('temp',__name__)


@temp.route("/temp_file/<path:filename>")
def temp_file(filename):
    temp_file_folder = r'Z:\CLARENCE\RESEARCH AND DEVELOPMENT\SOFTWARE\PYTHON\Flask_project\flask_project\temp'
    return send_from_directory(temp_file_folder,filename, as_attachment= True)
