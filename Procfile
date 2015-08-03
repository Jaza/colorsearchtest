web: gunicorn colorsearchtest.app:create_app\(\) -b 0.0.0.0:$PORT -w 3
upgrade: python manage.py db upgrade
createcolors: python manage.py createcolors $CREATECOLORS_MIN_COLORS $CREATECOLORS_MAX_COLORS
createcolorpickerimgsymlink: mkdir -p colorsearchtest/static/img && ln -s "../libs/bootstrap-colorpicker/dist/img/bootstrap-colorpicker" colorsearchtest/static/img/bootstrap-colorpicker
