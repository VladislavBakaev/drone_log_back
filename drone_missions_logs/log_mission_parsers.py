import numpy as np
from struct import unpack
import os
from pymavlink import DFReader

adc_sensors = 24
motors_num = 14
mission_byte_count = 79

param_types_parse_for_mavlink = ["GPS"]
count_parsing_log_file = 20

def parse_yd_mission_bin_file(file_name):
    dtype = np.dtype([('lat',np.float64),('lon',np.float64),('alt',np.float32),('r',np.float32),('time',np.int32),('hs',np.float32),
                    ('vs',np.float32),('plat',np.float64),('plon',np.float64),('ph',np.float32),('pa',np.float32),('flags',np.uint32),
                    ('photo',np.uint8),('psc',np.uint8),('pda',np.float32),('pp',np.float32),('pr',np.float32),('typ',np.uint8)])


    with open(file_name, "rb") as bin_file:
        num_data = np.fromfile(bin_file, dtype)
    
    list_num_data = num_data.tolist()
    return list_num_data

def parse_mavlink_log_bin_file(file_name):
    points_full = []
    points = []
    mlog = DFReader.DFReader_binary(file_name)
    mlog.rewind()
    while True:
        m = mlog.recv_match(type=param_types_parse_for_mavlink)
        if m is None:
            break
        m_dict = m.to_dict()
        points_full.append([m_dict['Lat'], m_dict['Lng']])
    for i in range(0, len(points_full), int(len(points_full)/count_parsing_log_file)):
        points.append(points_full[i])
    return points

def parse_mavlink_mission_waypoint(file_):
    points = []
    if not isinstance(file_,str):
        text = file_.read().decode()
        data = text.split('\r\n')
        for text_point in data:
            split_point = text_point.split('\t')
            if len(split_point) == 12:
                if not int(float(split_point[9]))==0 and not int(float(split_point[9]))==0:
                    int_part = list(map(int, split_point[:4]))
                    float_part = list(map(float, split_point[4:]))
                    points.append(int_part + float_part)
    return points

def parse_yd_mission_bytes_array(bytes_array):
    pattern = "<2d2fI2f2d2fI2B3fB"
    count_point = (len(bytes_array)/mission_byte_count)
    points = []
    if count_point.is_integer():
        for i in range(int(count_point)):
            point = unpack(pattern, bytes_array[i*mission_byte_count:(i+1)*mission_byte_count])
            points.append(point)
    else:
        raise Exception("File have invalid data")

    return points

def parse_yd_log_bin_file(file_name):
    # pattern = "<BL{0}f12f{1}h3B5fB25f2d19f5B2df2d5f2d3fL3fh35BH".format(adc_sensors, motors_num+18)

    # with open(file_name, "rb") as bin_file:
    #     points_bin = []
    #     points = []
    #     while True:
    #         litera = bin_file.read(3)
    #         if litera == b'':
    #             break
    #         points_bin.append(bin_file.read(1533))

    #     point_count = len(points_bin)
    #     step = int(point_count/50)
        
    #     for index in range(0, point_count, step) :
    #         point = unpack(pattern, points_bin[index][0:573])
    #         lat_lon_gps = point[104:106]
    #         if (lat_lon_gps[0]==0.0 and lat_lon_gps[1]==0.0):
    #             continue
    #         else:
    #             points.append(lat_lon_gps)

    pattern = "<2d".format(adc_sensors, motors_num+18)

    seek_step = 1520
    seek_offset = 340
    pack_size = 16
    point_count = count_parsing_log_file
    point_step = int((os.stat(file_name).st_size/(seek_step+pack_size))/point_count)
    points = []


    with open(file_name, "rb") as bin_file:
        bin_file.seek(seek_offset)
        while True:
            data = bin_file.read(16)
            if data == b'':
                break
            else:
                point = unpack(pattern, data)
                if point[0]!=0 and point[1]!=0:
                    points.append(point)
                bin_file.seek(seek_step*point_step + pack_size*(point_step-1),1)
    return points
    