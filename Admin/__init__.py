from flask import Blueprint

admin = Blueprint('Admin',__name__,static_url_path="/static", static_folder="static", template_folder="templates")

from . import views