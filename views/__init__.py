from flask import render_template, jsonify

import utilities
from vtk_bike import app


@app.route('/')
def home_page():
    #total_distance = utilities.get_overall_distance()
    #today_distance = utilities.get_today_distance()
    return render_template('distance.html')


@app.route('/distances')
def get_distances():
    return jsonify({
        "total": 0,
        "today": 0,
        "session": 0
    })
    result = {
        "total": utilities.get_overall_distance(),
        "today": utilities.get_today_distance(),
        "session": utilities.get_current_session_distance()
    }
    return jsonify(result)


@app.route('/session/new', methods=['POST'])
def start_new_session():
    utilities.start_new_session()
    return jsonify({"ok": True})


@app.route('/control')
def control_page():
    return render_template('control.html')
