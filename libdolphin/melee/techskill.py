import libdolphin.controller

def wavedash(direction, controller, jump_squat):
    if direction == "right":
        controller.press_button(libdolphin.controller.Buttons.X.value, libdolphin.controller.Buttons.press.value, 1)
        controller.press_button(libdolphin.controller.Buttons.X.value, libdolphin.controller.Buttons.release.value, jump_squat)
        controller.set_stick(libdolphin.controller.Buttons.main_stick.value, 1, .3, 0)
        controller.press_button(libdolphin.controller.Buttons.L.value, libdolphin.controller.Buttons.press.value, 5)
        controller.set_stick(libdolphin.controller.Buttons.main_stick.value, .5, .5, 0)
        controller.press_button(libdolphin.controller.Buttons.L.value, libdolphin.controller.Buttons.release.value, 10)

    elif direction == "left":
        controller.press_button(libdolphin.controller.Buttons.X.value, libdolphin.controller.Buttons.press.value, 1)
        controller.press_button(libdolphin.controller.Buttons.X.value, libdolphin.controller.Buttons.release.value, jump_squat)
        controller.set_stick(libdolphin.controller.Buttons.main_stick.value, 0, .3, 0)
        controller.press_button(libdolphin.controller.Buttons.L.value, libdolphin.controller.Buttons.press.value, 5)
        controller.set_stick(libdolphin.controller.Buttons.main_stick.value, .5, .5, 0)
        controller.press_button(libdolphin.controller.Buttons.L.value, libdolphin.controller.Buttons.release.value, 10)
