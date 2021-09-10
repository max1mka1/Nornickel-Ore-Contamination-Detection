
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def EncodedPixels_string(pixels):
    EncodedPixels_s = ''
    x = 0
    w = 0
    for i in range(len(pixels)):
        if x == 0:
            if pixels[i] == 1:
                x = i
                w += 1
        else:
            if pixels[i] == 1:
                w += 1
            else:
                EncodedPixels_s = EncodedPixels_s + str(x + 1) + ' ' + str(w) + ' '
                x = 0
                w = 0

    return EncodedPixels_s


def EncodedPixels(data, image_name, class_type, image_shape_x=704, image_shape_y=421):
    data_im = data[(data['image_name'] == image_name) & (data['type'] == class_type)]

    if len(data_im) == 0:
        print('Image or type not found')

    image_pixels = np.zeros((image_shape_x, image_shape_y))

    for k in range(len(data_im)):
        xmin = data_im.iloc[k]['xmin']
        xmax = data_im.iloc[k]['xmax'] + 1
        ymin = data_im.iloc[k]['ymin']
        ymax = data_im.iloc[k]['ymax'] + 1
        image_pixels[xmin:xmax, ymin:ymax] = 1

    image_pixels = image_pixels.T.reshape(1, -1)[0]
    EncodedPixels_s = EncodedPixels_string(image_pixels)

    return EncodedPixels_s


def decode_pixels(result):
    # decode pixels
    image_shape_x = 704
    image_shape_y = 421
    result = result.split(' ')
    image_pixels = np.zeros((image_shape_x, image_shape_y))
    for i in range(0, len(result) - 1, 2):
        y = int(result[i]) // image_shape_x
        x = int(result[i]) % image_shape_x
        w = int(result[i + 1])
        image_pixels[x:x + w, y] = 1

    plt.imshow(image_pixels.T)
    plt.xlabel('x')
    plt.ylabel('y')


if __name__ == '__main__':
    data = pd.read_csv('data/train.csv', index_col=0)
    data.head()

    result = EncodedPixels(data, '0019Date_01_08_2019.jpg', 'armature')
    print(result)
    decode_pixels(result)
