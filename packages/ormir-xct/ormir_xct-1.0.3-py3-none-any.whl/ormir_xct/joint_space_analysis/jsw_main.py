"""
Created by: Michael Kuczynski
Created on: June 9th, 2022

Description: Reimplementation of the IPL JSW Analysis
              as part of the ORMIR 2022 workshop.

Overview of JSW Steps:
  1. Image padding (ignored as not needed in Python)
  2. Dilation
  3. Erosion
  4. Threshold out JS Mask
  5. DT sphere filling
  6. Compute JSW parameters

Usage: python jsw_main.py JOINT_SEG.nii

Inputs:
   1. Joint segmentation image (binary)

Outputs:
  1. Joint Space Mask Image (MHA/NIFTI)
  2. Joint Space Output (text file)
"""

import os
import argparse
import SimpleITK as sitk

from jsw_morphometry import jsw_pad, jsw_dilate, jsw_erode, jsw_parameters


def main(joint_seg_path, output_path):
    filename = os.path.basename(joint_seg_path)
    basename = os.path.splitext(filename)[0]
    img = sitk.ReadImage(joint_seg_path, sitk.sitkUInt8)

    # Pad image
    print("Padding image...")
    pad_image = jsw_pad(img)

    # Dilate image
    print("Dilating image...")
    dilated_image = jsw_dilate(pad_image)
    sitk.WriteImage(
        dilated_image, os.path.join(output_path, str(basename) + "_DILATE.nii")
    )

    # Erode image
    print("Eroding image...")
    eroded_image, js_mask, dilated_js_mask = jsw_erode(dilated_image, pad_image)
    sitk.WriteImage(
        eroded_image, os.path.join(output_path, str(basename) + "_ERODE.nii")
    )
    sitk.WriteImage(js_mask, os.path.join(output_path, str(basename) + "_JS_MASK.nii"))
    sitk.WriteImage(
        dilated_js_mask,
        os.path.join(output_path, str(basename) + "_DILATED_JS_MASK.nii"),
    )

    # Compute JS parameters
    print("Computing thickness...")
    dt_img, jsw_params = jsw_parameters(
        pad_image, dilated_js_mask, basename, output_path, js_mask, 0.0607, True, False
    )

    # Copy the origin and spacing information from the original image so the
    # thickness map and original joint image overlap
    dt_img.SetOrigin(js_mask.GetOrigin())
    dt_img.SetSpacing(js_mask.GetSpacing())
    dt_img.SetDirection(js_mask.GetDirection())

    # Mask the thickness map with the original joint space mask
    dt_img = sitk.Mask(dt_img, js_mask)

    sitk.WriteImage(dt_img, os.path.join(output_path, str(basename) + "_DT.nii"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="jsw_main",
        description="Reimplementation of the IPL joint space width analysis.",
    )
    parser.add_argument("joint_seg", type=str, help="Joint segmentation image")
    args = parser.parse_args()

    joint_seg_path = args.joint_seg

    # Set the output path (same as input image path)
    output_path = os.path.dirname(joint_seg_path)

    main(joint_seg_path, output_path)
