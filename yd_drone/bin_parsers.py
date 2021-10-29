import numpy as np
from struct import unpack

adc_sensors = 24
motors_num = 14

def read_mission_bin_file(file_name):
    dtype = np.dtype([('lat',np.float64),('lon',np.float64),('alt',np.float32),('r',np.float32),('time',np.int32),('hs',np.float32),
                    ('vs',np.float32),('plat',np.float64),('plon',np.float64),('ph',np.float32),('pa',np.float32),('flags',np.uint32),
                    ('photo',np.uint8),('psc',np.uint8),('pda',np.float32),('pp',np.float32),('pr',np.float32),('typ',np.uint8)])


    with open(file_name, "rb") as bin_file:
        num_data = np.fromfile(bin_file, dtype)
    
    list_num_data = num_data.tolist()
    return list_num_data

def read_log_bin_file(file_name):
    pattern = "<BL{0}f12f{1}h3B5fB25f2d19f5B2df2d5f2d3fL3fh35BH".format(adc_sensors, motors_num+18)

    with open(file_name, "rb") as bin_file:
        point = []
        while True:
            litera = bin_file.read(3)
            if litera == b'':
                break
            point.append(bin_file.read(1533))
        
        for p in point:
            res = unpack(pattern, p[0:573])
            print(res)