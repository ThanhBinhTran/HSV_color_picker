import json
import numpy as np
from types import SimpleNamespace
from collections import namedtuple

class HSV_values:
    def __init__(self, hl=0, hh=179, sl=0, sh=255, vl=0, vh=255) -> None:
        self.hh = hh
        self.hl = hl
        self.sh = sh
        self.sl = sl
        self.vh = vh
        self.vl = vl
    def print(self):
        print ("Lower: H:{0}, S:{1}, V:{2}".format(self.hl, self.sl, self.vl))
        print ("Upper: H:{0}, S:{1}, V:{2}".format(self.hh, self.sh, self.vh))
    def set_hh(self, x): self.hh = x
    def set_hl(self, x): self.hl = x
    def set_sh(self, x): self.sh = x
    def set_sl(self, x): self.sl = x
    def set_vh(self, x): self.vh = x
    def set_vl(self, x): self.vl = x
    def set_values(self, hh, hl, sh, sl, vh, vl):
        self.set_hh(hh)
        self.set_hl(hl)
        self.set_sh(sh)
        self.set_sl(sl)
        self.set_vh(vh)
        self.set_vl(vl)
    def set_values_by_offset(self, hsv_pixel=[10,10,10],hsv_offset = [0,0,0]):
        self.hl, self.sl, self.vl = np.subtract(hsv_pixel, hsv_offset)
        self.hh, self.sh, self.vh = np.add(hsv_pixel, hsv_offset)

    def get_upper(self):
        return np.array((self.hh, self.sh, self.vh))
    def get_lower(self):
        return np.array((self.hl, self.sl, self.vl))

    def save_json(self, file_name):
        data = self.__dict__
        print (data)
        with open(file_name, 'w') as f:
            json.dump(data, f)
    
    def read_json(self, file_name):
        f = open(file_name)
 
        # returns JSON object as a dictionary
        data = json.load(f)
        #result = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        result = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

        # Closing file
        f.close()