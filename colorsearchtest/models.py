from colorsearchtest.database import (
    Column,
    db,
    Model,
    SurrogatePK,
)


class Color(SurrogatePK, Model):
    """An RGB color value."""

    __tablename__ = 'color'

    rgb_r = Column(db.Integer(), default=0)
    rgb_g = Column(db.Integer(), default=0)
    rgb_b = Column(db.Integer(), default=0)
    lab_l = Column(db.Float(), default=0.0)
    lab_a = Column(db.Float(), default=0.0)
    lab_b = Column(db.Float(), default=0.0)

    @property
    def hex(self):
        return '#{:02X}{:02X}{:02X}'.format(self.rgb_r, self.rgb_g, self.rgb_b)

    def __repr__(self):
        return self.hex
