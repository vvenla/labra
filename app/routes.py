from flask import render_template, redirect, flash, url_for, request
from app import app
from app.forms import MeasurementForm
import json


datafile = 'data.json'
json_data=open(datafile).read()
measurements = json.loads(json_data)
print(measurements)


## Dummy method for choosing the index for new measurement
def new_id():
    list = [i['id'] for i in measurements]
    return max(list) + 1


## Front page
@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        title='Etusivu',
    )


## Showing list of all measurements
@app.route('/all', methods=['GET'])
def all():
    return render_template(
        'all.html',
        title='Kaikki mittaukset',
        measurements=measurements
    )


## Adding new measurement
@app.route('/new', methods=['GET', 'POST'])
def new():
    form = MeasurementForm()
    if form.validate_on_submit():
        measurements.append({
            'id': new_id(),
            'name': form.name.data,
            'unit': form.unit.data,
            'result': form.result.data,
            'reference': form.reference.data
            })

        with open('data.json', 'w') as outfile:  
            json.dump(measurements, outfile)

        flash('Lisätty uusi mittaus: {}'.format(
            form.name.data))
        return redirect(url_for('index'))
    return render_template('new.html', title='Uusi mittaus', form=form)


## Deleting a measurement by id
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    for i in range(len(measurements)):
        if measurements[i]['id'] == id:
            measurements.pop(i)
            break

    with open('data.json', 'w') as outfile:  
            json.dump(measurements, outfile)

    flash('Mittaus poistettu'.format())

    return render_template(
        'all.html',
        title='Kaikki mittaukset',
        measurements=measurements
    )


## Editing a measurement by id (TODO: Prefilled form)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    for i in range(len(measurements)):
        if measurements[i]['id'] == id:
            edit_data = measurements[i]
    form = MeasurementForm()

    if form.validate_on_submit():
        edit_data['name'] = form.name.data
        edit_data['unit'] = form.unit.data
        edit_data['result'] = form.result.data
        edit_data['reference'] = form.reference.data

        with open('data.json', 'w') as outfile:  
            json.dump(measurements, outfile)

        flash('Mittaus muokattu: {}'.format(
            form.name.data))
        return redirect(url_for('index'))
    return render_template('edit.html', title='Muokkaa', form=form, id=id)



