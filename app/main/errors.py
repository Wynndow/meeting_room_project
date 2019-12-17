from flask import render_template
from . import main
from ..exceptions import InvalidUsage


@main.app_errorhandler(InvalidUsage)
def handle_invalid_usage(e):
    return render_template('invalid.html', message=e.message), 400
