import libdolphin.controller

def wavedash(direction, player):
    jump_squat = player.character_data['jump_squat']
    controller = player.controller

    if direction == "right":
        controller.press_button(libdolphin.controller.Buttons.X.value, libdolphin.controller.Buttons.press.value, 1)
        controller.press_button(libdolphin.controller.Buttons.X.value,
                libdolphin.controller.Buttons.release.value, jump_squat-1)
        controller.set_stick(libdolphin.controller.Buttons.main_stick.value, 1, .35, 0)
        controller.press_button(libdolphin.controller.Buttons.L.value, libdolphin.controller.Buttons.press.value, 5)
        controller.set_stick(libdolphin.controller.Buttons.main_stick.value, .5, .5, 0)
        controller.press_button(libdolphin.controller.Buttons.L.value, libdolphin.controller.Buttons.release.value, 10)

    elif direction == "left":
        controller.press_button(libdolphin.controller.Buttons.X.value, libdolphin.controller.Buttons.press.value, 1)
        controller.press_button(libdolphin.controller.Buttons.X.value,
                libdolphin.controller.Buttons.release.value, jump_squat-1)
        controller.set_stick(libdolphin.controller.Buttons.main_stick.value, 0, .35, 0)
        controller.press_button(libdolphin.controller.Buttons.L.value, libdolphin.controller.Buttons.press.value, 5)
        controller.set_stick(libdolphin.controller.Buttons.main_stick.value, .5, .5, 0)
        controller.press_button(libdolphin.controller.Buttons.L.value, libdolphin.controller.Buttons.release.value, 10)
