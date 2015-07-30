# -*- coding: utf-8 -*-
from flask_wtf import Form
import wtforms
import wtforms.validators


class ColorSearchForm(Form):
    color = wtforms.TextField(validators=[wtforms.validators.Required()])
