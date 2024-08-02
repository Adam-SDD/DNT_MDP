import random

def roll_dice(dice):
    total = 0
    num, sides = dice.split('d')
    num = int(num)
    sides = int(sides)
    for i in range(num):
        total += random.randint(1, sides)
    return(total)

def test_roll(terms): 
    dice_arr = [] #[(num_sides, roll), (sum_sides, roll)]
    for term in terms:
        roll = roll_dice(term)
        num_sides = int(term.split('d')[1])
        dice_arr.append((num_sides, roll))
    return dice_arr

terms = ['4d6', '5d7', '10d12']
print(test_roll(terms))