import PIL
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array
from keras.models import load_model


def upscale_image(model, img):
    ycbcr = img.convert("YCbCr")
    y, cb, cr = ycbcr.split()
    y = img_to_array(y)
    y = y.astype("float32") / 255.0

    input = np.expand_dims(y, axis=0)
    out = model.predict(input)

    out_img_y = out[0]
    out_img_y *= 255.0

    out_img_y = out_img_y.clip(0, 255)
    out_img_y = out_img_y.reshape((np.shape(out_img_y)[0], np.shape(out_img_y)[1]))
    out_img_y = PIL.Image.fromarray(np.uint8(out_img_y), mode="L")
    out_img_cb = cb.resize(out_img_y.size, PIL.Image.BICUBIC)
    out_img_cr = cr.resize(out_img_y.size, PIL.Image.BICUBIC)
    out_img = PIL.Image.merge("YCbCr", (out_img_y, out_img_cb, out_img_cr)).convert(
        "RGB"
    )
    return out_img

def upscale_image_3_channels(model, img):
    y = img_to_array(img)
    y = y.astype("float32") / 255.0

    input = np.expand_dims(y, axis=0)
    out = model.predict(input)

    out_img_y = out[0]
    out_img_y *= 255.0

    out_img_y = out_img_y.clip(0, 255)
    out_img_y = out_img_y.reshape((np.shape(out_img_y)[0], np.shape(out_img_y)[1], 3))
    out_img_y = PIL.Image.fromarray(np.uint8(out_img_y), mode="RGB")
    return out_img_y

UPSCALE_MODEL = load_model('model.h5')
UPSCALE_MODEL_3 = load_model('model_3channels.h5')

if __name__ == '__main__':
    with Image.open("Macaco-self_small.jpg") as im:
        im_new = upscale_image(UPSCALE_MODEL, im)
        im_new.show()
        im_new.save("teste.png")
