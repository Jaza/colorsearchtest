# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)

from sqlalchemy import func

from colorsearchtest.utils import flash_errors, calc_fore_color
from colorsearchtest.public.forms import ColorSearchForm

from colorsearchtest.models import Color

blueprint = Blueprint('public', __name__, static_folder="../static")


MAX_COLORS = 100


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form =ColorSearchForm(request.form)

    # Handle search
    if request.method == 'POST':
        if form.validate_on_submit():
            return redirect(url_for("public.home") + '?color={0}'.format(form.color.data.replace('#', '')))
        else:
            flash_errors(form)

    color_results = Color.query

    color = None
    colors = None

    colors_cie2000 = None
    colors_cie1976 = None
    colors_cie1994 = None
    colors_cmc = None

    colors_cie1976_db = None
    colors_cie2000_db = None

    if request.args.get('color', None):
        color = '#{0}'.format(request.args.get('color'))

        from operator import itemgetter
        from colormath.color_conversions import convert_color
        from colormath.color_objects import sRGBColor, LabColor
        from colormath.color_diff import (delta_e_cie2000,
                                          delta_e_cie1976,
                                          delta_e_cie1994,
                                          delta_e_cmc)

        from colorsearchtest.utils import (delta_e_cie1976_query,
                                           delta_e_cie2000_query)

        c_rgb = sRGBColor.new_from_rgb_hex(color)
        c_lab = convert_color(c_rgb, LabColor)

        colors = []

        if 0:
            for c in color_results.all():
                c2_lab = LabColor(lab_l=c.lab_l,
                                  lab_a=c.lab_a,
                                  lab_b=c.lab_b,
                                  illuminant='d65')

                colors.append({
                    'hex': str(c),
                    'fore_color': ('#{:02X}{:02X}{:02X}'.format(*calc_fore_color((c.rgb_r, c.rgb_g, c.rgb_b)))),
                    'delta_e_cie2000': delta_e_cie2000(c_lab,
                                                       c2_lab),
                    'delta_e_cie1976': delta_e_cie1976(c_lab,
                                                       c2_lab),
                    'delta_e_cie1994': delta_e_cie1994(c_lab,
                                                       c2_lab),
                    'delta_e_cmc': delta_e_cmc(c_lab,
                                               c2_lab)})

        #colors_cie2000 = sorted(colors, key=itemgetter('delta_e_cie2000'))[:MAX_COLORS]
        #colors_cie1976 = sorted(colors, key=itemgetter('delta_e_cie1976'))[:MAX_COLORS]
        #colors_cie1994 = sorted(colors, key=itemgetter('delta_e_cie1994'))[:MAX_COLORS]
        #colors_cmc = sorted(colors, key=itemgetter('delta_e_cmc'))[:MAX_COLORS]
        colors = None

        if 0:
            color_results = delta_e_cie1976_query(
                lab_l=c_lab.lab_l,
                lab_a=c_lab.lab_a,
                lab_b=c_lab.lab_b,
                limit=MAX_COLORS)

            colors_cie1976_db = []
            for c in color_results:
                colors_cie1976_db.append({
                    'hex': '#{:02X}{:02X}{:02X}'.format(c[0], c[1], c[2]),
                    'fore_color': ('#{:02X}{:02X}{:02X}'.format(*calc_fore_color((c[0], c[1], c[2])))),
                    'delta_e_cie1976_db': c[3]})

        if 1:
            color_results = delta_e_cie2000_query(
                lab_l=c_lab.lab_l,
                lab_a=c_lab.lab_a,
                lab_b=c_lab.lab_b,
                limit=MAX_COLORS)

            colors_cie2000_db = []
            for c in color_results:
                colors_cie2000_db.append({
                    'hex': '#{:02X}{:02X}{:02X}'.format(c[0], c[1], c[2]),
                    'fore_color': ('#{:02X}{:02X}{:02X}'.format(*calc_fore_color((c[0], c[1], c[2])))),
                    'delta_e_cie2000_db': c[3]})
    else:
        colors = [{
                'hex': str(c),
                'fore_color': ('#{:02X}{:02X}{:02X}'.format(*calc_fore_color((c.rgb_r, c.rgb_g, c.rgb_b)))),
                'delta_e_cie2000': None}
            for c in color_results
                .order_by(func.random())
                .limit(MAX_COLORS)
                .all()]

    return render_template("public/home.html",
                           form=form,
                           colors=colors,
                           colors_cie2000=colors_cie2000,
                           colors_cie1976=colors_cie1976,
                           colors_cie1994=colors_cie1994,
                           colors_cmc=colors_cmc,
                           colors_cie1976_db=colors_cie1976_db,
                           colors_cie2000_db=colors_cie2000_db,
                           color=color)
