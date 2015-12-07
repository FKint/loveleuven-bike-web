from flask import render_template, jsonify

import utilities
from vtk_bike import app


@app.route('/')
def home_page():
    total_distance = utilities.get_overall_distance()
    today_distance = utilities.get_today_distance()
    return render_template('distance.html', total_distance=total_distance, today_distance=today_distance)


@app.route('/distances')
def get_distances():
    result = {
        "total": utilities.get_overall_distance(),
        "today": utilities.get_today_distance(),
        "session": utilities.get_current_session_distance()
    }
    return jsonify(result)


@app.route('/session/new')
def start_new_session():
    utilities.start_new_session()
