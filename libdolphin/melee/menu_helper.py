import yaml
import libdolphin
import os

with open(os.path.dirname(__file__) + "/data/character_select.yaml", "r") as f:
    character_select_data = yaml.load(f.read())

with open(os.path.dirname(__file__) + "/data/character_select_options.yaml", "r") as f:
    character_select_options = yaml.load(f.read())

# THIS IS A HACK AND NEEDS TO BE CHANGED TO MAKE IT PERMANENT, BUT IT MAKES IT
# EASIER TO TEST IF IT EXISTS AS A HACK FOR NOW
def select_character(game, character, player):
    controller = player.controller
    x = character_select_data[character]['x']
    y = character_select_data[character]['y']
    x_diff = x - game.global_data['p' + str(player.player_num) + '_cursor_x']
    y_diff = y - game.global_data['p' + str(player.player_num) + '_cursor_y']

    if abs(x_diff) >= 1.24:
        if x_diff > 0:
            x_vel = .65
        elif x_diff < 0:
            x_vel = .35
    else:
        x_vel = 0.5

    if abs(y_diff) >= 1.24:
        if y_diff < 0:
            y_vel = .35
        elif y_diff > 0:
            y_vel = .65
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

def change_to_cpu(game, player):
    controller = player.controller
    x = character_select_options['p' + str(player.player_num)]['type_change']['x']
    y = character_select_options['p' + str(player.player_num)]['type_change']['y']
    x_diff = x - game.global_data['p' + str(player.player_num) + '_cursor_x']
    y_diff = y - game.global_data['p' + str(player.player_num) + '_cursor_y']

    if abs(x_diff) >= 1.24:
        if x_diff > 0:
            x_vel = .35
        elif x_diff < 0:
            x_vel = .65
    else:
        x_vel = 0.5

    if abs(y_diff) >= 1.24:
        if y_diff < 0:
            y_vel = .35
        elif y_diff > 0:
            y_vel = .65
    else:
        y_vel = 0.5

    controller.set_stick(libdolphin.controller.Buttons.main_stick.value,
            x_vel, y_vel, 1)

    if abs(x_diff) < 1.24 and abs(y_diff) < 1.24:
        if player.set_cpu == False:
            player.controller.empty_queue()
            print("set_cpu")
            if game.global_data['p' + str(player.player_num) + '_char_mode'] == 0:
                print("mode 0")
                controller.press_button(libdolphin.controller.Buttons.A.value,
                        libdolphin.controller.Buttons.press.value, 4)
                controller.press_button(libdolphin.controller.Buttons.A.value,
                        libdolphin.controller.Buttons.release.value, 1)

            elif game.global_data['p' + str(player.player_num) + '_char_mode'] == 3:
                print("mode 3")
                controller.press_button(libdolphin.controller.Buttons.A.value,
                        libdolphin.controller.Buttons.press.value, 4)
                controller.press_button(libdolphin.controller.Buttons.A.value,
                        libdolphin.controller.Buttons.release.value, 1)
                controller.press_button(libdolphin.controller.Buttons.A.value,
                        libdolphin.controller.Buttons.press.value, 4)
                controller.press_button(libdolphin.controller.Buttons.A.value,
                        libdolphin.controller.Buttons.release.value, 1)
            player.set_cpu = True

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
