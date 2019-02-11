from flask import render_template, redirect, flash, url_for, jsonify
from app import app
from app.forms import NewMeasurementForm, EditForm
import json


datafile = 'data.json'
json_data=open(datafile).read()
data = json.loads(json_data)
print(data)


## Dummy method for choosing the index for new measurement
def new_id():
    list = [i['id'] for i in data]
    print(list)
    print(max(list))
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
        measurements=data
    )


## Adding new measurement
@app.route('/new', methods=['GET', 'POST'])
def new():
    global current_id
    form = NewMeasurementForm()
    if form.validate_on_submit():

        data.append({
            'id': new_id(),
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


## Deleting a measurement by id
@app.route('/delete/<int:id>', methods=['DELETE', 'POST'])
def delete(id):
    for i in range(len(data)):
        if data[i]['id'] == id:
            data.pop(i)
            break

    with open('data.json', 'w') as outfile:  
            json.dump(data, outfile)

    flash('Mittaus poistettu'.format())

    return render_template(
        'all.html',
        title='Kaikki mittaukset',
        measurements=data
    )


## Editing a measurement by id
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    for i in range(len(data)):
        if data[i]['id'] == id:
            edit_data = data[i]

    form = EditForm()

    if form.validate_on_submit():
        form.name.data = edit_data.name
        form.unit.data = edit_data.name
        print(edit_data)
        print(edit_data.name)
        



        with open('data.json', 'w') as outfile:  
            json.dump(data, outfile)

        flash('Mittaus muokattu: {}'.format(
            form.name.data))
        return render_template(
            'all.html',
            title='Kaikki mittaukset',
            measurements=data
        )
    return render_template('edit.html', title='Muokkaa', form=form, data=edit_data)



