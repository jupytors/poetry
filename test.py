from flask import Flask, render_template, request, jsonify
from config import config
from database import init_db
from models import PoemModel
import os




env = os.environ.get('FLASK_ENV', 'development')
#app.config.from_object(config[env])


poem = PoemModel.get_by_id(1)

print(poem)