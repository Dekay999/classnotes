from scipy import ndimage
from keras.preprocessing import image
import random
import cairocffi as cairo
import editdistance
import keras.callbacks
import numpy as np
import unicodedata
import random, string
#all_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
all_chars = u'abcdefghijklmnopqrstuvwxyz '
all_chars_idx = range(len(all_chars))
absolute_max_string_len = 10

def randomstring():
    rlen = random.choice(range(3,absolute_max_string_len))
    ridx = [random.choice(all_chars_idx) for i in range(rlen)]
    rchars = [all_chars[i] for i in ridx]
    str = "".join(rchars)
    return ridx, str

def get_minibatch(w,h,batch_size=1):
    res = {}
    source_str = []
    the_labels = np.ones((batch_size,absolute_max_string_len))
    the_input = np.zeros((batch_size,w,h,1))
    label_length = np.zeros((batch_size,1))
    input_length = np.zeros((batch_size,1))
    for i in range(batch_size):
    	(idxs,str) = randomstring()
        #print str
    	tmp = paint_text(str,w,h,rotate=True,ud=True,multi_fonts=True)
    	the_input[i, :] = tmp.reshape((w,h,1))
        label_length[i, 0] = len(str)
        input_length[i, 0] = 30.
        for j in range(len(idxs)): the_labels[i, j] = idxs[j]
        source_str.append(str)

    res['the_input'] = the_input
    res['the_labels'] = the_labels
    res['source_str'] = source_str
    res['label_length'] = label_length
    res['input_length'] = input_length
    return (res,)



# this creates larger "blotches" of noise which look
# more realistic than just adding gaussian noise
# assumes greyscale with pixels ranging from 0 to 1

def speckle(img):
    severity = np.random.uniform(0, 0.6)
    blur = ndimage.gaussian_filter(np.random.randn(*img.shape) * severity, 1)
    img_speck = (img + blur)
    img_speck[img_speck > 1] = 1
    img_speck[img_speck <= 0] = 0
    return img_speck


# Redundant instance of paint_text only kept for generation of empty
# samples within the module.

def paint_text(text, w, h, rotate=False, ud=False, multi_fonts=False):
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
    with cairo.Context(surface) as context:
        context.set_source_rgb(1, 1, 1)  # White
        context.paint()
        # this font list works in CentOS 7
        if multi_fonts:
            fonts = ['Century Schoolbook', 'Courier', 'STIX', 'URW Chancery L', 'FreeMono']
            context.select_font_face(np.random.choice(fonts), cairo.FONT_SLANT_NORMAL,
                                     np.random.choice([cairo.FONT_WEIGHT_BOLD, cairo.FONT_WEIGHT_NORMAL]))
        else:
            context.select_font_face('Courier', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        context.set_font_size(20)
        box = context.text_extents(text)
        border_w_h = (4, 4)
        if box[2] > (w - 2 * border_w_h[1]) or box[3] > (h - 2 * border_w_h[0]):
            raise IOError('Could not fit string into image. Max char count is too large for given image width.')

        # teach the RNN translational invariance by
        # fitting text box randomly on canvas, with some room to rotate
        max_shift_x = w - box[2] - border_w_h[0]
        max_shift_y = h - box[3] - border_w_h[1]
        top_left_x = np.random.randint(0, int(max_shift_x))
        if ud:
            top_left_y = np.random.randint(0, int(max_shift_y))
        else:
            top_left_y = h // 2
        context.move_to(top_left_x - int(box[0]), top_left_y - int(box[1]))
        context.set_source_rgb(0, 0, 0)
        context.show_text(text)

    buf = surface.get_data()
    a = np.frombuffer(buf, np.uint8)
    a.shape = (h, w, 4)
    a = a[:, :, 0]  # grab single channel
    a = a.astype(np.float32) / 255
    a = np.expand_dims(a, 0)
    if rotate:
        a = image.random_rotation(a, 3 * (w - top_left_x) / w + 1)
    a = speckle(a)
    return a


