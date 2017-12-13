import yaml
import libdolphin
import os
import math

with open(os.path.dirname(__file__) + "/data/character_select.yaml", "r") as f:
    character_select_data = yaml.load(f.read())

with open(os.path.dirname(__file__) + "/data/stage_select.yaml", "r") as f:
    stage_select_data = yaml.load(f.read())

with open(os.path.dirname(__file__) + "/data/character_select_options.yaml", "r") as f:
    character_select_options = yaml.load(f.read())

def select_character(game, character, player):
    if player.character_selected == False:
        controller = player.controller
        x = character_select_data[character]['x']
        y = character_select_data[character]['y']
        x_diff = x - game.global_data['p' + str(player.player_num) + '_cursor_x']
        y_diff = y - game.global_data['p' + str(player.player_num) + '_cursor_y']

        mod = .4

        angle = math.atan(y_diff/x_diff)

        if x_diff > 0 and y_diff > 0:
            x_vel = 0.5 + math.cos(angle) * mod
            y_vel = 0.5 + math.sin(angle) * mod

        elif x_diff < 0 and y_diff > 0:
            x_vel = 0.5 + -(math.cos(angle) * mod)
            y_vel = 0.5 + -(math.sin(angle) * mod)

        elif x_diff > 0 and y_diff < 0:
            x_vel = 0.5 + math.cos(angle) * mod
            y_vel = 0.5 + math.sin(angle) * mod

        elif x_diff < 0 and y_diff < 0:
            x_vel = 0.5 + -(math.cos(angle) * mod)
            y_vel = 0.5 + -(math.sin(angle) * mod)

        if abs(x_diff) > 1.24 or abs(y_diff) > 1.24:
            controller.empty_queue()
            controller.set_stick(libdolphin.controller.Buttons.main_stick.value,
                    x_vel, y_vel, 0)

        else:
            controller.empty_queue()
            controller.set_stick(libdolphin.controller.Buttons.main_stick.value,
                    0.5, 0.5, 0)
            controller.press_button(libdolphin.controller.Buttons.A.value,
                    libdolphin.controller.Buttons.release.value, 0)
            controller.press_button(libdolphin.controller.Buttons.A.value,
                    libdolphin.controller.Buttons.press.value, 1)
            controller.press_button(libdolphin.controller.Buttons.A.value,
                    libdolphin.controller.Buttons.release.value, 0)
            player.character_selected = True

def change_to_cpu(game, player):
    if player.set_cpu == False:
        controller = player.controller
        x = character_select_options['p' + str(player.player_num)]['type_change']['x']
        y = character_select_options['p' + str(player.player_num)]['type_change']['y']
        x_diff = x - game.global_data['p' + str(player.player_num) + '_cursor_x']
        y_diff = y - game.global_data['p' + str(player.player_num) + '_cursor_y']

        x_vel = 0.5
        y_vel = 0.5

        mod = .4

        if y_diff != 0 and x_diff != 0:
            angle = math.atan(y_diff/x_diff)

        elif y_diff == 0 and x_diff != 0:
            if x_diff > 0:
                x_vel = 0.5 + mod
            else:
                x_vel = 0.5 - mod

        elif x_diff == 0 and y_diff != 0:
            if y_diff > 0:
                y_vel = 0.5 + mod
            else:
                y_vel = 0.5 - mod

        if x_diff > 0 and y_diff > 0:
            x_vel = 0.5 + math.cos(angle) * mod
            y_vel = 0.5 + math.sin(angle) * mod

        elif x_diff < 0 and y_diff > 0:
            x_vel = 0.5 + -(math.cos(angle) * mod)
            y_vel = 0.5 + -(math.sin(angle) * mod)

        elif x_diff > 0 and y_diff < 0:
            x_vel = 0.5 + math.cos(angle) * mod
            y_vel = 0.5 + math.sin(angle) * mod

        elif x_diff < 0 and y_diff < 0:
            x_vel = 0.5 + -(math.cos(angle) * mod)
            y_vel = 0.5 + -(math.sin(angle) * mod)

        player.controller.empty_queue()
        controller.set_stick(libdolphin.controller.Buttons.main_stick.value,
                x_vel, y_vel, 0)

        if abs(x_diff) < 1.24 and abs(y_diff) < 1.24:
            player.controller.empty_queue()
            controller.set_stick(libdolphin.controller.Buttons.main_stick.value,
                    0.5, 0.5, 0)
            if game.global_data['p' + str(player.player_num) + '_char_mode'] == 0:
                controller.press_button(libdolphin.controller.Buttons.A.value,
                        libdolphin.controller.Buttons.release.value, 1)
                controller.press_button(libdolphin.controller.Buttons.A.value,
                        libdolphin.controller.Buttons.press.value, 1)
                controller.press_button(libdolphin.controller.Buttons.A.value,
                        libdolphin.controller.Buttons.release.value, 1)

            elif game.global_data['p' + str(player.player_num) + '_char_mode'] == 3:
                controller.press_button(libdolphin.controller.Buttons.A.value,
                        libdolphin.controller.Buttons.release.value, 1)
                controller.press_button(libdolphin.controller.Buttons.A.value,
                        libdolphin.controller.Buttons.press.value, 1)
                controller.press_button(libdolphin.controller.Buttons.A.value,
                        libdolphin.controller.Buttons.release.value, 1)
                controller.press_button(libdolphin.controller.Buttons.A.value,
                        libdolphin.controller.Buttons.press.value, 1)
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

def start_game(game):
    for i in game.players:
        if i.controller:
            controller = i.controller
            break

    controller.press_button(libdolphin.controller.Buttons.START.value,
            libdolphin.controller.Buttons.release.value, 15)
    controller.press_button(libdolphin.controller.Buttons.START.value,
            libdolphin.controller.Buttons.press.value, 15)
    controller.press_button(libdolphin.controller.Buttons.START.value,
            libdolphin.controller.Buttons.release.value, 0)

def select_stage(stage, game):
    if game.global_data['menu'] == 2160820320:
        for i in game.players:
            if i.controller:
                controller = i.controller
                break

        x = stage_select_data[stage]['x']
        y = stage_select_data[stage]['y']
        x_diff = x - game.global_data["stage_select_x"]
        y_diff = y - game.global_data["stage_select_y"]

        mod = .4

        angle = math.atan(y_diff/x_diff)

        if x_diff > 0 and y_diff > 0:
            x_vel = 0.5 + math.cos(angle) * mod
            y_vel = 0.5 + math.sin(angle) * mod

        elif x_diff < 0 and y_diff > 0:
            x_vel = 0.5 + -(math.cos(angle) * mod)
            y_vel = 0.5 + -(math.sin(angle) * mod)

        elif x_diff > 0 and y_diff < 0:
            x_vel = 0.5 + math.cos(angle) * mod
            y_vel = 0.5 + math.sin(angle) * mod

        elif x_diff < 0 and y_diff < 0:
            x_vel = 0.5 + -(math.cos(angle) * mod)
            y_vel = 0.5 + -(math.sin(angle) * mod)

        if abs(x_diff) > 1.24 or abs(y_diff) > 1.24:
            controller.empty_queue()
            controller.set_stick(libdolphin.controller.Buttons.main_stick.value,
                    x_vel, y_vel, 0)
            return False

        else:
            controller.empty_queue()
            controller.set_stick(libdolphin.controller.Buttons.main_stick.value,
                    0.5, 0.5, 0)
            controller.press_button(libdolphin.controller.Buttons.A.value,
                    libdolphin.controller.Buttons.release.value, 30)
            controller.press_button(libdolphin.controller.Buttons.A.value,
                    libdolphin.controller.Buttons.press.value, 1)
            controller.press_button(libdolphin.controller.Buttons.A.value,
                    libdolphin.controller.Buttons.release.value, 0)
            return True
    return False
