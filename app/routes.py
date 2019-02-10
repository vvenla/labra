from flask import render_template, redirect, flash, url_for
from app import app
from app.forms import NewMeasurementForm

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        title='Etusivu',
    )

measurements = [
    {
        "id": 1,
        "name": "Hemoglobiini",
        "unit": "g/l",
        "result": "132.2",
        "reference": "167"
    },
    {
        "id": 2,
        "name": "LDL-kolesteroli",
        "unit": "mmol/l",
        "result": "0",
        "reference": "3"
    }
]



@app.route('/all', methods=['GET'])
def all():
    return render_template(
        'all.html',
        title='Kaikki mittaukset',
        measurements=measurements
    )


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = NewMeasurementForm()
    if form.validate_on_submit():
        flash('Lisätty uusi mittaus: {}'.format(
            form.name.data))
        return redirect(url_for('index'))
    return render_template('new.html', title='Uusi mittaus', form=form)
