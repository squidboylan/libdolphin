import struct
import yaml
import binascii

class Player:
    def __init__(self, player_num):
        with open("melee/data/static_player_data.yaml", "r") as f:
            self.config_from_file = yaml.load(f.read())

        self.player_num = player_num
        self.generate_config_from_offsets()
        self.data = {}
        for i in self.static_data_loc.keys():
            self.data[self.static_data_loc[i]['name']] = 0

    def generate_config_from_offsets(self):
        start_pos = self.config_from_file['start_pos'][self.player_num]
        start_pos = binascii.unhexlify(start_pos)
        self.static_data_loc = {}
        for i in self.config_from_file['offset'].keys():
            padded_i = i.zfill(8)
            i_bin = binascii.unhexlify(padded_i)
            final_pos = start_pos + i_bin
            string_pos = binascii.hexlify(struct.pack(">I", struct.unpack(">I", i_bin)[0] + struct.unpack(">I", start_pos)[0]))
            self.static_data_loc[string_pos.upper().decode("utf-8")] = self.config_from_file['offset'][i]

    def update(self, data):
        if data[0] in self.static_data_loc.keys():
            val = data[1].strip('\x00').zfill(8)
            val = struct.unpack(self.static_data_loc[data[0]]['type'],
                    binascii.unhexlify(val))[self.static_data_loc[data[0]]['index']]
            self.data[self.static_data_loc[data[0]]['name']] = val

    def print_data(self):
        if self.data['state'] == 2:
            print("Player: " + str(self.player_num))
            print(self.data)

if __name__ == "__main__":
    player = []
    for i in range(4):
        player.append(Player(i+1))
        print(player[i].static_data_loc)
