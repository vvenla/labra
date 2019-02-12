from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class MeasurementForm(FlaskForm):
    name = StringField('Nimi', validators=[DataRequired()])
    unit = StringField('Yksikkö', validators=[DataRequired()])
    result = StringField('Mittaustulos', validators=[DataRequired()])
    reference = StringField('Viitearvo')
    submit = SubmitField('Tallenna mittaus')