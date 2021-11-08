import os
from flask import Flask, request, jsonify, make_response, render_template
import json
import numpy as np
import pandas as pd
import hashlib
import plotly
import plotly.express as px
import plotly.figure_factory as ff
from concurrent.futures import ThreadPoolExecutor
from utils.const import UPDATE_KEY, CHARACTER_NAMES
from utils.data_util import update_data
from utils.win_rate_util import get_floor_win_rates
from utils.play_rate_util import get_floor_play_rates
from utils.matchup_util import get_floor_match_ups

app = Flask(__name__, template_folder='templates')


def preflight():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

@app.route('/update', methods=['OPTIONS','POST'])
def update():
    if request.method == 'OPTIONS':
        return preflight()
    try:
        data = request.json
        passwd = data['key']
        if hashlib.md5(passwd.encode()).digest() == UPDATE_KEY:
            with ThreadPoolExecutor(max_workers = 2) as executor:
                data = executor.submit(update_data)
        res = jsonify({"success": True})
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/stats/all/<floor>', methods=['GET'])
def all_stats(floor):
    win_rates = get_floor_win_rates(floor)
    wr_fig = px.bar(win_rates, y='char_name', x=f'win_rate_{floor}', orientation='h')
    wr_graph_json = json.dumps(wr_fig, cls=plotly.utils.PlotlyJSONEncoder)
    play_rates = get_floor_play_rates(floor)
    pr_fig = px.pie(play_rates, values=f'play_rate_{floor}', names='char_name')
    pr_graph_json = json.dumps(pr_fig, cls=plotly.utils.PlotlyJSONEncoder)
    match_ups = get_floor_match_ups(floor)
    # mu_fig = px.density_heatmap(match_ups, x='char_name', y=CHARACTER_NAMES)
    mu_fig = ff.create_annotated_heatmap(
        x=CHARACTER_NAMES, 
        y=CHARACTER_NAMES[::-1],
        z=match_ups.drop(['char_name'], axis=1).to_numpy()[::-1],
        annotation_text=np.round(match_ups.drop(['char_name'], axis=1).to_numpy()*10, decimals=1)[::-1],
        colorscale='temps',
        reversescale=True
        )
    mu_graph_json = json.dumps(mu_fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('overall_stats.html', wr_graph_json=wr_graph_json, pr_graph_json=pr_graph_json, mu_graph_json=mu_graph_json)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))