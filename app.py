from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Configure MongoDB connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/note_app'
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo.Note_app
notes_collection = db.notes

@app.route('/')
def index():
    notes = notes_collection.find()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    title = request.form.get('title')
    content = request.form.get('content')
    notes_collection.insert_one({'title': title, 'content': content})
    return redirect(url_for('index'))

@app.route('/edit/<note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = notes_collection.find_one({'_id': note_id})
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_content = request.form.get('content')
        notes_collection.update_one({'_id': note_id}, {'$set': {'title': new_title, 'content': new_content}})
        return redirect(url_for('index'))
    return render_template('edit.html', note=note)

@app.route('/delete/<note_id>')
def delete_note(note_id):
    notes_collection.delete_one({'_id': note_id})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
