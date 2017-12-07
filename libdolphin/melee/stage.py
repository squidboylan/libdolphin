import struct
import yaml
import binascii
import os

class Stage:
    # Initialize stage memory dicts
    def __init__(self):
        with open(os.path.dirname(__file__) + "/data/stage_data.yaml", "r") as f:
            self.stage_data_config_file = yaml.load(f.read())

        self.generate_config_from_offsets()

        self.stage_data = {}

        for i in self.stage_data_config.keys():
            self.stage_data[self.stage_data_config[i]['name']] = 0

    def generate_config_from_offsets(self):
        self.start_pos = self.stage_data_config_file['start_pos']
        self.start_pos_bin = binascii.unhexlify(self.start_pos)
        self.stage_data_config = {}
        for i in self.stage_data_config_file['offset'].keys():
            padded_i = i.zfill(8)
            i_bin = binascii.unhexlify(padded_i)
            final_pos = self.start_pos_bin + i_bin
            string_pos = binascii.hexlify(struct.pack(">I", struct.unpack(">I", i_bin)[0] + struct.unpack(">I", self.start_pos_bin)[0]))
            self.stage_data_config[string_pos.upper().decode("utf-8")] = self.stage_data_config_file['offset'][i]

    def update(self, data):
        if data[0] in self.stage_data_config:
            val = data[1].strip('\x00').zfill(8)
            val = struct.unpack(self.stage_data_config[data[0]]['type'],
                    binascii.unhexlify(val))[self.stage_data_config[data[0]]['index']]
            self.stage_data[self.stage_data_config[data[0]]['name']] = val
            return 1

        return 0

    def generate_locations_file(self):
        contents = "# Start of stage data\n"
        for i in self.stage_data_config.keys():
            contents += "#" + self.stage_data_config[i]['name'] + ' \n'
            contents += i + '\n'

        return contents

    def print_data(self):
        print(self.stage_data)
