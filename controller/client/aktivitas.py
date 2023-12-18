from . import *


@app.route('/aktivitas')
def aktivitas():
    aktivitas = db["aktivitas"]
    aktivitas_data = aktivitas.find().sort("createdAt", pymongo.DESCENDING)
    return render_template('view/client/aktivitas.html', aktivitas=aktivitas_data)


@app.route('/aktivitas_detail/<id>')
def aktivitas_detail(id):
    username = ''
    aktivitaskuId = ''
    aktivitas = db["aktivitas"]
    aktivitasku = db["aktivitasku"]
    aktivitas_data = aktivitas.find_one({"_id": ObjectId(id)})
    aktivitasku_data = aktivitasku.find_one(
        {"aktivitasData._id": ObjectId(id)})
    print(aktivitasku_data)
    if aktivitasku_data:
        username = aktivitasku_data['username']
        aktivitaskuId = aktivitasku_data['_id']
    return render_template('view/client/aktivitas-detail.html', aktivitas=aktivitas_data, username=username, id=aktivitaskuId)
