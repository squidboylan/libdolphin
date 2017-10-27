import struct
import yaml
import binascii

class Player:
    # Initialize character memory dicts
    def __init__(self, player_num):
        with open("melee/data/static_player_block.yaml", "r") as f:
            self.static_block_config_file = yaml.load(f.read())

        with open("melee/data/static_player_data.yaml", "r") as f:
            self.character_data_config_file = yaml.load(f.read())

        self.player_num = player_num

        self.generate_config_from_offsets()

        self.static_block_data = {}
        self.character_data = {}

        for i in self.static_block_config.keys():
            self.static_block_data[self.static_block_config[i]['name']] = 0

        for i in self.character_data_config.keys():
            self.character_data[self.character_data_config[i]['name']] = 0

    # Generate the dict of addresses from start addresses and offsets, as well
    def generate_config_from_offsets(self):
        start_pos = self.static_block_config_file['start_pos'][self.player_num]
        start_pos = binascii.unhexlify(start_pos)
        self.static_block_config = {}
        for i in self.static_block_config_file['offset'].keys():
            padded_i = i.zfill(8)
            i_bin = binascii.unhexlify(padded_i)
            final_pos = start_pos + i_bin
            string_pos = binascii.hexlify(struct.pack(">I", struct.unpack(">I", i_bin)[0] + struct.unpack(">I", start_pos)[0]))
            self.static_block_config[string_pos.upper().decode("utf-8")] = self.static_block_config_file['offset'][i]

        start_pos = self.character_data_config_file['start_pos'][self.player_num]
        self.character_data_config = {}
        for i in self.character_data_config_file['offset'].keys():
            self.character_data_config[start_pos.upper() + " " + i.upper()] = self.character_data_config_file['offset'][i]

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

        return contents

    # Print player data, this is useful for debugging
    def print_data(self):
        if self.static_block_data['state'] == 2:
            print("Player: " + str(self.player_num))
            print(self.character_data)
            print(self.static_block_data)

if __name__ == "__main__":
    player = []
    for i in range(4):
        player.append(Player(i+1))
        print(player[i].static_data_loc)
