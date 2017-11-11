import struct
import yaml
import binascii
import os

class Player:
    # Initialize character memory dicts
    def __init__(self, player_num, controller=None):
        self.controller = controller
        with open(os.path.dirname(__file__) + "/data/static_player_block.yaml", "r") as f:
            self.static_block_config_file = yaml.load(f.read())

        with open(os.path.dirname(__file__) + "/data/static_player_data.yaml", "r") as f:
            self.character_data_config_file = yaml.load(f.read())

        self.player_num = player_num

        self.generate_config_from_offsets()

        self.static_block_data = {}
        self.character_data = {}

        self.character_selected = False

        for i in self.static_block_config.keys():
            self.static_block_data[self.static_block_config[i]['name']] = 0

        for i in self.character_data_config.keys():
            self.character_data[self.character_data_config[i]['name']] = 0

        self.hitboxes = []
        for i in range(4):
            self.hitboxes.append(Hitbox(i+1, self.start_pos))

    # Generate the dict of addresses from start addresses and offsets, as well
    def generate_config_from_offsets(self):
        self.start_pos = self.static_block_config_file['start_pos'][self.player_num]
        self.start_pos_bin = binascii.unhexlify(self.start_pos)
        self.static_block_config = {}
        for i in self.static_block_config_file['offset'].keys():
            padded_i = i.zfill(8)
            i_bin = binascii.unhexlify(padded_i)
            final_pos = self.start_pos_bin + i_bin
            string_pos = binascii.hexlify(struct.pack(">I", struct.unpack(">I", i_bin)[0] + struct.unpack(">I", self.start_pos_bin)[0]))
            self.static_block_config[string_pos.upper().decode("utf-8")] = self.static_block_config_file['offset'][i]

        self.start_pos = self.character_data_config_file['start_pos'][self.player_num]
        self.character_data_config = {}
        for i in self.character_data_config_file['offset'].keys():
            self.character_data_config[self.start_pos.upper() + " " + i.upper()] = self.character_data_config_file['offset'][i]

    # Take data and update the player data
    def update(self, data):
        if data[0] in self.static_block_config:
            val = data[1].strip('\x00').zfill(8)
            val = struct.unpack(self.static_block_config[data[0]]['type'],
                    binascii.unhexlify(val))[self.static_block_config[data[0]]['index']]
            self.static_block_data[self.static_block_config[data[0]]['name']] = val
            return 1

        elif data[0] in self.character_data_config:
            val = data[1].strip('\x00').zfill(8)
            val = struct.unpack(self.character_data_config[data[0]]['type'],
                    binascii.unhexlify(val))[self.character_data_config[data[0]]['index']]
            self.character_data[self.character_data_config[data[0]]['name']] = val
            return 1

        for i in self.hitboxes:
            r = i.update(data)
            if r == 1:
                return r

        return 0

    def generate_locations_file(self, contents):
        contents += "# Start of p" + str(self.player_num) + " contents\n"
        contents += "# Start of static block\n"
        for i in self.static_block_config.keys():
            contents += "#" + self.static_block_config[i]['name'] + ' \n'
            contents += i + '\n'

        contents += "# Start of player data block\n"
        for i in self.character_data_config.keys():
            contents += "#" + self.character_data_config[i]['name'] + '\n'
            contents += i + '\n'

        for i in self.hitboxes:
            contents = i.generate_locations_file(contents)

        return contents

    # Print player data, this is useful for debugging
    def print_data(self):
        if self.static_block_data['state'] == 2:
            print("Player: " + str(self.player_num))
            print(self.character_data)
            print(self.static_block_data)
            for i in self.hitboxes:
                i.print_data()


class Hitbox:
    # Initialize hitbox memory dicts
    def __init__(self, hitbox_num, player_start_pos):
        with open(os.path.dirname(__file__) + "/data/hitbox.yaml", "r") as f:
            self.hitbox_config_file = yaml.load(f.read())

        self.hitbox_num = hitbox_num
        self.player_start_pos = player_start_pos

        self.generate_config_from_offsets()

        self.hitbox_data = {}
        for i in self.hitbox_data_config.keys():
            self.hitbox_data[self.hitbox_data_config[i]['name']] = 0

    # Generate the dict of addresses from start addresses and offsets, as well
    def generate_config_from_offsets(self):
        self.hitbox_data_config = {}
        self.start_pos = self.hitbox_config_file['start_pos'][self.hitbox_num]
        self.start_pos = self.start_pos.zfill(8)
        self.start_pos_bin = binascii.unhexlify(self.start_pos)
        for i in self.hitbox_config_file['offset'].keys():
            padded_i = i.zfill(8)
            i_bin = binascii.unhexlify(padded_i)
            final_pos = self.start_pos_bin + i_bin
            string_pos = binascii.hexlify(struct.pack(">I", struct.unpack(">I", i_bin)[0] + struct.unpack(">I", self.start_pos_bin)[0]))
            self.hitbox_data_config[self.player_start_pos + " " + string_pos.upper().decode('utf-8').lstrip('0')] = self.hitbox_config_file['offset'][i]

    # Generate the locations file contents
    def generate_locations_file(self, contents):
        contents += "# Start of hitbox" + str(self.hitbox_num) + " contents\n"
        for i in self.hitbox_data_config.keys():
            contents += "#" + self.hitbox_data_config[i]['name'] + ' \n'
            contents += i + '\n'

        return contents

    # Take data and update the hitbox data
    def update(self, data):
        if data[0] in self.hitbox_data_config:
            val = data[1].strip('\x00').zfill(8)
            val = struct.unpack(self.hitbox_data_config[data[0]]['type'],
                    binascii.unhexlify(val))[self.hitbox_data_config[data[0]]['index']]
            self.hitbox_data[self.hitbox_data_config[data[0]]['name']] = val
            return 1

        return 0


    # Print hitbox data, this is useful for debugging
    def print_data(self):
        if self.hitbox_data['status'] != 0:
            print("Hitbox: " + str(self.hitbox_num))
            print(self.hitbox_data)

if __name__ == "__main__":
    player = []
    for i in range(4):
        player.append(Player(i+1))
        print(player[i].static_data_loc)

