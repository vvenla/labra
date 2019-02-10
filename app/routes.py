from flask import render_template, redirect, flash, url_for, jsonify
from app import app
from app.forms import NewMeasurementForm
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        title='Etusivu',
    )


datafile = 'data.json'
json_data=open(datafile).read()
data = json.loads(json_data)
print(data)





@app.route('/all', methods=['GET'])
def all():
    return render_template(
        'all.html',
        title='Kaikki mittaukset',
        measurements=data
    )


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = NewMeasurementForm()
    if form.validate_on_submit():

        data.append({
            'id': 3,
            'name': form.name.data,
            'unit': form.unit.data,
            'result': form.result.data,
            'reference': form.reference.data
            })
        with open('data.json', 'w') as outfile:  
            json.dump(data, outfile)

        flash('Lisätty uusi mittaus: {}'.format(
            form.name.data))
        return redirect(url_for('index'))
    return render_template('new.html', title='Uusi mittaus', form=form)
