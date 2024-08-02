import random

def roll_dice(dice):
    print(dice)
    total = 0
    num, sides = dice.split('d')
    num = int(num)
    sides = int(sides)
    for i in range(num):
        total += random.randint(1, sides)
    return(total)

def pick_preset():
    folder_preset = "Presets"
    if not os.path.exists(folder_preset):
        print("There are no presets yet \n feel free to make your own :)")
        return
    
    print("Available presets:")
    preset_files = os.listdir(folder_preset)
    for file_name in preset_files:
        print(file_name)
    choice = input('Enter desired preset: ')
    
    preset_file_path = os.path.join(folder_preset, f'{choice}.txt')
    if not os.path.exists(preset_file_path):
        print('this preset does not exist \nmaybe you spelt it wrong')
        return
    
    with open(preset_file_path, 'r') as preset_file:
        dice_arr = []
        dices = preset_file.readlines()
        for dice in dices:
            dice_arr.append(dice.strip())
        return(dice_arr)

def save_preset(dice_arr):
    folder_preset = "Presets"
    if not os.path.exists(folder_preset):
        os.makedirs(folder_preset)
    preset_name = input('Enter a name for this preset: ')
    preset_file_path = os.path.join(folder_preset, f'{preset_name}.txt')
    with open(preset_file_path, 'w') as preset_file:
        for dice in dice_arr:
            preset_file.write(f'{dice}\n')
    print(f"your preset '{preset_name}' has been saved.")
