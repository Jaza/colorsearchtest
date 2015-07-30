def createcolors(min_colors, max_colors):
    """Creates some random colors and saves them to the DB."""

    from colorsearchtest.database import db
    from colorsearchtest.models import Color

    from colormath.color_conversions import convert_color
    from colormath.color_objects import sRGBColor, LabColor

    # Based on:
    # https://github.com/kevinwuhoo/randomcolor-py/blob/master/test_randomcolor.py

    import randomcolor
    import random

    rand_color = randomcolor.RandomColor()

    rand = random.Random()
    rand_int = lambda: rand.randint(min_colors, max_colors)

    i = rand_int()
    colors = rand_color.generate(count=i, format_='rgbArray')

    for x in colors:
        c_rgb = sRGBColor(rgb_r=x[0], rgb_g=x[1], rgb_b=x[2],
                          is_upscaled=True)
        c_lab = convert_color(c_rgb, LabColor)

        c = Color(rgb_r=x[0], rgb_g=x[1], rgb_b=x[2],
                  lab_l=c_lab.lab_l, lab_a=c_lab.lab_a, lab_b=c_lab.lab_b)
        db.session.add(c)

    db.session.commit()

    return i
