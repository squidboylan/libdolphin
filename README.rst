libdolphin
==========

The aim of libdolphin is to provide a simple way to interact with games
emulated in the dolphin emulator. The first game and main game being targeted
is Super Smash Bros. Melee.

In order to use libdolphin you must compile a custom version of dolphin that
lets you read memory from the GameCube while the game runs. Clone
https://github.com/squidboylan/dolphin/tree/memorywatcher-fork and compile it
using the instructions in the README.

Currently libdolphin is tested on Linux, but may also work on Mac OS. It will
not work on Windows and there are no current plans to support it.

Super Smash Bros. Melee
~~~~~~~~~~~~~~~~~~~~~~~

In order to use the Melee submodule you must have a copy of Super Smash Bros.
Melee v1.02.

The Melee memory locations and meanings are being drawn from
https://docs.google.com/spreadsheets/d/1JX2w-r2fuvWuNgGb6D3Cs4wHQKLFegZe2jhbBuIhCG8/edit#gid=12
which is a spreasheet maintained by the community of that information.
