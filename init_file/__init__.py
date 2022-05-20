from flask import Flask

app = Flask(__name__)
app.config.from_object('init_file.config')

from init_file.view import entries