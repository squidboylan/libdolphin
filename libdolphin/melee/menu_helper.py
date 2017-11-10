import yaml
import libdolphin
import os

with open(os.path.dirname(__file__) + "/data/character_select.yaml", "r") as f:
    menu_data = yaml.load(f.read())

# THIS IS A HACK AND NEEDS TO BE CHANGED TO MAKE IT PERMANENT, BUT IT MAKES IT
# EASIER TO TEST IF IT EXISTS AS A HACK FOR NOW
def select_character(game, character, player):
    controller = player.controller
    x = menu_data[character]['x']
    y = menu_data[character]['y']
    x_diff = x - game.global_data['p' + str(player.player_num) + '_cursor_x']
    y_diff = y - game.global_data['p' + str(player.player_num) + '_cursor_y']

    if abs(x_diff) >= 1.24:
        if x_diff > 0:
            x_vel = 1
        elif x_diff < 0:
            x_vel = 0
    else:
        x_vel = 0.5

    if abs(y_diff) >= 1.24:
        if y_diff < 0:
            y_vel = 0
        elif y_diff > 0:
            y_vel = 1
    else:
        y_vel = 0.5

    if abs(x_diff) >= 1.24 or abs(y_diff) >=1.24:
        controller.set_stick(libdolphin.controller.Buttons.main_stick.value,
                x_vel, y_vel, 1)

    else:
        if player.character_selected == False:
            controller.set_stick(libdolphin.controller.Buttons.main_stick.value,
                    x_vel, y_vel, 1)
            controller.press_button(libdolphin.controller.Buttons.A.value,
                    libdolphin.controller.Buttons.press.value, 1)
            controller.press_button(libdolphin.controller.Buttons.A.value,
                    libdolphin.controller.Buttons.release.value, 0)
            player.character_selected = True

def start_and_select_random_stage(game):
    for i in game.players:
        if i.controller:
            controller = i.controller

    #controller.empty_queue()

    controller.press_button(libdolphin.controller.Buttons.START.value,
            libdolphin.controller.Buttons.release.value, 60)
    controller.press_button(libdolphin.controller.Buttons.START.value,
            libdolphin.controller.Buttons.press.value, 30)
    controller.press_button(libdolphin.controller.Buttons.START.value,
            libdolphin.controller.Buttons.release.value, 60)
    controller.press_button(libdolphin.controller.Buttons.START.value,
            libdolphin.controller.Buttons.press.value, 30)
    controller.press_button(libdolphin.controller.Buttons.START.value,
            libdolphin.controller.Buttons.release.value, 30)
