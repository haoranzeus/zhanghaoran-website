from flask import render_template 
from ..models import Entries

from . import main

@main.route('/', methods=['GET'])
def index():
    entries = Entries.query.all()
    return render_template('index.html', entries=entries)

@main.route('/blog/<int:id>')
def article(id):
    entry = Entries.query.get_or_404(id)
    return render_template('article.html', entry=entry)
