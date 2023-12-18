from . import *

target = os.path.join(
    APP_ROOT, app.config['IMG_ARTIKEL'])
artikel = db["artikel"]


@app.route('/data_artikel', methods=["GET"])
@login_required
@roles_required('admin')
def data_artikel():
    artikel_data = artikel.find().sort("createdAt", pymongo.DESCENDING)
    return render_template('view/server/data-artikel/index.html', artikel=artikel_data)


@app.route('/data_artikel/create', methods=["GET"])
@login_required
@roles_required('admin')
def data_artikel_create():
    return render_template('view/server/data-artikel/create.html')


@app.route('/data_artikel/<id>/edit', methods=["GET"])
@login_required
@roles_required('admin')
def data_artikel_edit(id):
    artikel_data = artikel.find_one({"_id": ObjectId(id)})
    return render_template('view/server/data-artikel/edit.html', artikel=artikel_data)


@app.route('/data_artikel', methods=["POST"])
@login_required
@roles_required('admin')
def data_artikel_store():
    if not os.path.isdir(target):
        os.mkdir(target)
    judul = request.form['judul']
    deskripsi = request.form['deskripsi']
    image = request.files["image"]

    required_fields = ['judul', 'deskripsi', 'image']
    error_messages = {
        'judul': 'Data judul tidak boleh kosong',
        'deskripsi': 'Data deskripsi tidak boleh kosong',
        'image': 'Data image tidak boleh kosong',
    }

    for field in required_fields:
        if not locals()[field]:
            flash(error_messages[field], 'error')
            return redirect(url_for('data_artikel_create'))

    filename = secure_filename(image.filename)
    unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{filename}"
    destination = os.path.join(target, unique_filename)
    image.save(destination)
    artikel.insert_one({'judul': judul,
                        'deskripsi': deskripsi,
                        "image": unique_filename,
                        "createdAt": current_time,
                        "updateAt": current_time})
    flash('Data artikel berhasil di tambah!', 'success')
    return redirect(url_for('data_artikel'))


@app.route('/data_artikel/<id>', methods=["POST"])
@login_required
@roles_required('admin')
def data_artikel_update(id):
    judul = request.form['judul']
    deskripsi = request.form['deskripsi']
    new_image = request.files["image"]

    required_fields = ['judul', 'deskripsi', 'new_image']
    error_messages = {
        'judul': 'Data judul tidak boleh kosong',
        'deskripsi': 'Data deskripsi tidak boleh kosong',
        'new_image': 'Data image tidak boleh kosong',
    }

    for field in required_fields:
        if not locals()[field]:
            flash(error_messages[field], 'error')
            return redirect(url_for('data_artikel_edit', id=id))

    if not os.path.isdir(target):
        os.mkdir(target)

    existing_data = artikel.find_one({"_id": ObjectId(id)})
    existing_image = existing_data.get("image")

    if existing_image:
        existing_image_path = os.path.join(target, existing_image)
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)

    filename = secure_filename(new_image.filename)
    unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{filename}"
    destination = os.path.join(target, unique_filename)
    new_image.save(destination)

    artikel.update_one({"_id": ObjectId(id)},
                       {"$set": {
                           "judul": judul,
                           "deskripsi": deskripsi,
                           "image": unique_filename,
                           "updateAt": current_time}
                        })
    flash('Data artikel berhasil di edit!', 'success')
    return redirect(url_for('data_artikel'))


@app.route('/data_artikel/delete/<id>', methods=["POST"])
@login_required
@roles_required('admin')
def data_artikel_delete(id):
    if not os.path.isdir(target):
        os.mkdir(target)

    existing_data = artikel.find_one({"_id": ObjectId(id)})
    existing_image = existing_data.get("image")

    if existing_image:
        existing_image_path = os.path.join(target, existing_image)
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)
    artikel.delete_one({"_id": ObjectId(id)})
    flash('Data artikel berhasil di hapus!', 'success')
    return redirect(url_for('data_artikel'))
