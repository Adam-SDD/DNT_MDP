from flask import Flask, request, render_template
import random
import time
from threading import Thread
from functions import roll_dice
import csv
import os
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    input_values = request.form.getlist('dice')
    terms = {f"term{i+1}": value for i, value in enumerate(input_values)}
    dice_arr = [] #[(num_sides, roll), (sum_sides, roll)]
    for term in terms.values():
        roll = roll_dice(term)
        num_sides = int(term.split('d')[1]) #splits 2d4 into 2, 4
        dice_arr.append((num_sides, roll))
    dice_results = json.dumps(dice_arr)
    return render_template('submit.html', dice_arr=dice_arr, dice_results=dice_results)



@app.route('/save', methods=['POST', 'GET'])
def save():
    input_values = request.form.getlist('dice')
    terms = {f"term{i+1}": value for i, value in enumerate(input_values)}
    dice_arr = [] #[(num_sides, roll), (sum_sides, roll)]
    for term in terms.values():
        roll = roll_dice(term)
        num_sides = int(term.split('d')[1]) #gets the 
        dice_arr.append((num_sides, roll))
    filename = request.form['filename']
    folder_preset = 'preset'
    if not os.path.exists(folder_preset):
        os.makedirs(folder_preset)
    preset_name = filename
    preset_file_path = os.path.join(folder_preset, f'{preset_name}.csv')
    with open(preset_file_path, 'w') as preset_file:
        writer = csv.writer(preset_file)
        for dice in dice_arr:
            writer.writerow(f'{dice}\n')
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)