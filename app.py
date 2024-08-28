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

    # Specify the folder containing the CSV files
    folder_path = 'preset'
    names = []
    files = []
    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        short = filename.replace('.csv', '')
        files.append(filename)
        names.append(short)
    return render_template('index.html', combined = list(zip(files, names)))

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    input_values = request.form.getlist('dice')
    terms = {f"term{i+1}": value for i, value in enumerate(input_values)}
    dice_arr = [] #[(num_sides, roll), (sum_sides, roll)]
    total = 0
    for term in terms.values():
        roll = roll_dice(term)
        num_sides = int(term.split('d')[1]) #splits 2d4 into 2, 4 and takes the first value
        dice_arr.append((num_sides, roll))
        total += roll
    dice_results = json.dumps(dice_arr)
    return render_template('submit.html', dice_arr=dice_arr, dice_results=dice_results, total=total)


@app.route('/load_preset/<filename>')
def load_preset(filename):
    folder_path = 'preset'
    file_path = os.path.join(folder_path, filename)
    total = 0
    dice_arr = [] #[(num_sides, roll), (sum_sides, roll)]
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            dice_list = content.split(',')
            for term in dice_list:
                roll = roll_dice(term)
                num_sides = int(term.split('d')[1]) #splits 2d4 into 2, 4 and takes the first value
                total += roll
                dice_arr.append((num_sides, roll))
            dice_results = json.dumps(dice_arr)
        return render_template('preset.html', dice_arr=dice_arr, dice_results=dice_results, total=total)
    else:
        return "File not found", 404
    

@app.route('/save', methods=['POST', 'GET'])
def save():
    input_values = request.form.getlist("dice_results") 
    terms = {f"term{i+1}": value for i, value in enumerate(input_values)}
    filename = request.form['filename']
    folder_preset = 'preset'
    if not os.path.exists(folder_preset):
        os.makedirs(folder_preset)
    preset_name = filename
    preset_file_path = os.path.join(folder_preset, f'{preset_name}.csv')
    with open(preset_file_path, 'w') as preset_file:
        for term in terms.values():
                preset_file.write(f'{term}\n')
    return render_template('save.html', filename = filename)

'''
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
        for dice in dice_arr:
            preset_file.write(f'{dice}\n')
    return render_template('save.html', filename = filename)
'''


if __name__ == '__main__':
    app.run(debug=True)