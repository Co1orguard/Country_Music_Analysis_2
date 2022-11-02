from flask_wtf import FlaskForm
from typing import List, Tuple
from wtforms import SubmitField, SelectMultipleField, BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from applayer.artistlist import ArtistList


class ArtistForm(FlaskForm):
    # The next four lines are the extension point for adding data to the pick list
    choices: List[Tuple[int, str]]
    ids = [938895, 2634203, 1141486, 908705, 2411933, 2304638, 3895080, 1448909, 1448911, 1141474, 2916175, 353265, 1141476, 938862, 1141491, 1141484, 1141487, 307357, 1141480, 516930, 1001138, 1141475, 269365, 1141488, 1141483, 1141489, 2867358, 2867360, 2189637, 908699, 1420640, 2867359, 1826135]
    artists = ArtistList(ids)
    choices = artists.artists

    # Create the two fields for the form
    omit = BooleanField(label="Omit Writers")
    depth = IntegerField(label="Depth", default=3, validators=[NumberRange(min=1, max=8)])
    select = SelectMultipleField('Select one or more artists', choices=choices, coerce=int, validators=[DataRequired()])
    submit = SubmitField('Generate')
