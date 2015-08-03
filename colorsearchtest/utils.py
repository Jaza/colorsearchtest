# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)


def calc_fore_color(back_color):
    """
    Calculates white or black foreground color depending on
    specified background color.
    Thanks to:
    http://blog.nitriq.com/BlackVsWhiteText.aspx
    """

    RED_LUMINANCE = 299
    GREEN_LUMINANCE = 587
    BLUE_LUMINANCE = 114

    MAX_LUMINANCE = (RED_LUMINANCE * 255 + GREEN_LUMINANCE * 255 + BLUE_LUMINANCE * 255)
    MID_LUMINANCE = MAX_LUMINANCE / 2

    total_custom_brightness = ((back_color[0] * RED_LUMINANCE) + (back_color[1] * GREEN_LUMINANCE) + (back_color[2] * BLUE_LUMINANCE))

    return (total_custom_brightness <= MID_LUMINANCE) and (255, 255, 255) or (0, 0, 0)
