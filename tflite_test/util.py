# -*- encoding: utf-8 -*-
'''
@File    :   util.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/4/27 13:50   LiuDongxing      1.0         None
'''

import cv2
import numpy as np
# import lib

def get_yuv_crop(frame_shape, crop):
    # crop should be (x1,y1,x2,y2)
    frame_height = frame_shape[0] // 3 * 2
    frame_width = frame_shape[1]

    # compute the width/height of the uv channels
    uv_width = frame_width // 2  # width of the uv channels
    uv_height = frame_height // 4  # height of the uv channels

    # compute the offset for upper left corner of the uv channels
    uv_x_offset = crop[0] // 2  # x offset of the uv channels
    uv_y_offset = crop[1] // 4  # y offset of the uv channels

    # compute the width/height of the uv crops
    uv_crop_width = (crop[2] - crop[0]) // 2  # width of the cropped uv channels
    uv_crop_height = (crop[3] - crop[1]) // 4  # height of the cropped uv channels

    # ensure crop dimensions are multiples of 2 and 4
    y = (crop[0], crop[1], crop[0] + uv_crop_width * 2, crop[1] + uv_crop_height * 4)

    u1 = (
        0 + uv_x_offset,
        frame_height + uv_y_offset,
        0 + uv_x_offset + uv_crop_width,
        frame_height + uv_y_offset + uv_crop_height,
    )

    u2 = (
        uv_width + uv_x_offset,
        frame_height + uv_y_offset,
        uv_width + uv_x_offset + uv_crop_width,
        frame_height + uv_y_offset + uv_crop_height,
    )

    v1 = (
        0 + uv_x_offset,
        frame_height + uv_height + uv_y_offset,
        0 + uv_x_offset + uv_crop_width,
        frame_height + uv_height + uv_y_offset + uv_crop_height,
    )

    v2 = (
        uv_width + uv_x_offset,
        frame_height + uv_height + uv_y_offset,
        uv_width + uv_x_offset + uv_crop_width,
        frame_height + uv_height + uv_y_offset + uv_crop_height,
    )

    return y, u1, u2, v1, v2

def yuv_crop_and_resize(frame, region, height=None):
    # Crops and resizes a YUV frame while maintaining aspect ratio
    # https://stackoverflow.com/a/57022634
    height = frame.shape[0] // 3 * 2
    width = frame.shape[1]

    # get the crop box if the region extends beyond the frame
    crop_x1 = max(0, region[0])
    crop_y1 = max(0, region[1])
    # ensure these are a multiple of 4
    crop_x2 = min(width, region[2])
    crop_y2 = min(height, region[3])
    crop_box = (crop_x1, crop_y1, crop_x2, crop_y2)

    y, u1, u2, v1, v2 = get_yuv_crop(frame.shape, crop_box)

    # if the region starts outside the frame, indent the start point in the cropped frame
    y_channel_x_offset = abs(min(0, region[0]))
    y_channel_y_offset = abs(min(0, region[1]))

    uv_channel_x_offset = y_channel_x_offset // 2
    uv_channel_y_offset = y_channel_y_offset // 4

    # create the yuv region frame
    # make sure the size is a multiple of 4
    # TODO: this should be based on the size after resize now
    size = (region[3] - region[1]) // 4 * 4
    yuv_cropped_frame = np.zeros((size + size // 2, size), np.uint8)
    # fill in black
    yuv_cropped_frame[:] = 128
    yuv_cropped_frame[0:size, 0:size] = 16

    # copy the y channel
    yuv_cropped_frame[
        y_channel_y_offset : y_channel_y_offset + y[3] - y[1],
        y_channel_x_offset : y_channel_x_offset + y[2] - y[0],
    ] = frame[y[1] : y[3], y[0] : y[2]]

    uv_crop_width = u1[2] - u1[0]
    uv_crop_height = u1[3] - u1[1]

    # copy u1
    yuv_cropped_frame[
        size + uv_channel_y_offset : size + uv_channel_y_offset + uv_crop_height,
        0 + uv_channel_x_offset : 0 + uv_channel_x_offset + uv_crop_width,
    ] = frame[u1[1] : u1[3], u1[0] : u1[2]]

    # copy u2
    yuv_cropped_frame[
        size + uv_channel_y_offset : size + uv_channel_y_offset + uv_crop_height,
        size // 2
        + uv_channel_x_offset : size // 2
        + uv_channel_x_offset
        + uv_crop_width,
    ] = frame[u2[1] : u2[3], u2[0] : u2[2]]

    # copy v1
    yuv_cropped_frame[
        size
        + size // 4
        + uv_channel_y_offset : size
        + size // 4
        + uv_channel_y_offset
        + uv_crop_height,
        0 + uv_channel_x_offset : 0 + uv_channel_x_offset + uv_crop_width,
    ] = frame[v1[1] : v1[3], v1[0] : v1[2]]

    # copy v2
    yuv_cropped_frame[
        size
        + size // 4
        + uv_channel_y_offset : size
        + size // 4
        + uv_channel_y_offset
        + uv_crop_height,
        size // 2
        + uv_channel_x_offset : size // 2
        + uv_channel_x_offset
        + uv_crop_width,
    ] = frame[v2[1] : v2[3], v2[0] : v2[2]]

    return yuv_cropped_frame

def yuv_region_2_rgb(frame, region):
    try:
        # TODO: does this copy the numpy array?
        yuv_cropped_frame = yuv_crop_and_resize(frame, region)
        return cv2.cvtColor(yuv_cropped_frame, cv2.COLOR_YUV2RGB_I420)
    except:
        print(f"frame.shape: {frame.shape}")
        print(f"region: {region}")
        raise