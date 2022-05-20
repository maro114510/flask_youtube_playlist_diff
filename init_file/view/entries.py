from flask import request,redirect,url_for,render_template,flash,session
from init_file import app
from models import operation_db,video_list
import os

new_data = video_list.video_titles(video_list.video_ids)

if not os.path.join(os.getcwd(),'youtube.db'):
  operation_db.create_db(new_data)

@app.route('/')
def show_entries():
  return render_template('entries/index.html')

@app.route('/entries')
def entry():

  entry={
    }
  return render_template('entries/playlist.html',entry=entry)

@app.route('/entries/add')
def add_playlist():
  return render_template('entries/_add.html')

@app.route('/entries/delete')
def delete_playlist():
  return render_template('entries/_delete.html')

@app.route('/entries/edit2',methods=['POST'])
def edit2():
  return 'to push register'

@app.route('/entries/<int:id>',methods=['GET'])
def notify(id):
  return f'to push {id}'
