import numpy as np
from PIL import Image

RGB_TO_XYZ = np.array([[0.412453, 0.357580, 0.180423],
                       [0.212671, 0.715160, 0.072169],
                       [0.019334, 0.119193, 0.950227]])

XYZ_TO_RGB = np.array([[3.240481, -1.537151, -0.498536],
                       [-0.969256, 1.875990, 0.0415560],
                       [0.055647, -0.204041, 1.057311]])

BRADFORD = np.array([[0.8951, 0.2664, -0.1614],
                     [-0.7502, 1.7135, 0.0367],
                     [0.0389, -0.0685, 1.0296]])


def srgb_to_linear(srgb):
    # 'sRGB' in [0.0, 1.0]
    ln_rgb = srgb.copy()
    mask = ln_rgb > 0.04045
    ln_rgb[mask] = np.power((ln_rgb[mask] + 0.055) / 1.055, 2.4)
    ln_rgb[~mask] /= 12.92
    return ln_rgb

def linear_to_srgb(linear):
    # 'linear RGB' in [0.0, 1.0]
    srgb = linear.copy()
    mask = srgb > 0.0031308
    srgb[mask] = 1.055 * np.power(srgb[mask], 1 / 2.4) - 0.055
    srgb[~mask] *= 12.92
    return np.clip(srgb, 0.0, 1.0)

def get_gray_world_illuminant(img):
    # image in sRGB with range [0.0, 1.0]
    # convert sRGB to linear RGB
    ln_img = srgb_to_linear(img)
    # mean of each channel
    avg_ch = ln_img.mean(axis=(0, 1))
    # convert back RGB mean values to sRGB
    return linear_to_srgb(avg_ch)


def srgb_to_xyz(srgb):
    # convert 'sRGB' to 'linear RGB'
    rgb = srgb_to_linear(srgb)
    # convert 'linear RGB' to 'XYZ'
    return rgb @ RGB_TO_XYZ.T

def xyz_to_srgb(xyz):
    # convert 'XYZ' to 'linear RGB'
    rgb = xyz @ XYZ_TO_RGB.T
    # convert back 'linear RGB' to 'sRGB'
    return linear_to_srgb(rgb)

def normalize_xyz(xyz):
    # normalize xyz with 'y' so that 'y' represents luminance
    return xyz / xyz[1]

def xyz_to_lms(xyz):
    return xyz @ BRADFORD.T

def get_gain(lms_src, lms_dst):
    return lms_dst / lms_src

def transform_lms(gain):
    return np.linalg.inv(BRADFORD) @ np.diag(gain) @ BRADFORD

def chromatic_adaptation_image(src_white_point, dst_white_point, src_img):
    # convert white point in 'sRGB' to 'XYZ'
    # and normalize 'XYZ' that 'Y' as luminance
    xyz_src = srgb_to_xyz(src_white_point)
    n_xyz_src = normalize_xyz(xyz_src)
    xyz_dst = srgb_to_xyz(dst_white_point)
    n_xyz_dst = normalize_xyz(xyz_dst)

    # convert 'XYZ' to 'LMS'
    lms_src = xyz_to_lms(n_xyz_src)
    lms_dst = xyz_to_lms(n_xyz_dst)
    # LMS gain by scaling destination with source LMS
    gain = get_gain(lms_src, lms_dst)

    # multiply CAT matrix with LMS gain factors
    ca_transform = transform_lms(gain)

    # convert 'sRGB' source image to 'XYZ'
    src_img_xyz = srgb_to_xyz(src_img)

    # apply CAT transform to image
    transformed_xyz = src_img_xyz @ ca_transform.T

    # convert back 'XYZ' to 'sRGB' image
    transformed_img = xyz_to_srgb(transformed_xyz)

    return transformed_img


if __name__ == '__main__':
    # read image which generally in sRGB format, and scale image in range [0.0, 1.0]
    img = np.array(Image.open('../Textures/batman.png'))[:, :, :3] / 255.0
    illuminant = get_gray_world_illuminant(img)

    # source illuminant white point obtained from previous step
    src_white_point = illuminant
    # destination illuminant white point scale to 1.0
    dst_white_point = np.ones(3)

    ca_img = chromatic_adaptation_image(src_white_point, dst_white_point, img)
    # reverse channel order from RGB to BGR, and rescale to 255
    ca_img = (ca_img * 255).astype(np.uint8)

    dst_image = Image.fromarray(ca_img)
    dst_image.save("../Textures/batman_ca.png")