from . import *


@app.route('/donatur')
def donatur():
    donatur = db["donatur"]
    donatur_data = donatur.find().sort("createdAt", pymongo.DESCENDING)
    return render_template('view/client/donatur.html', donatur=donatur_data)


@app.route('/donatur_detail/<id>')
def donatur_detail(id):
    donatur = db["donatur"]
    donatur_data = donatur.find_one({"_id": ObjectId(id)})
    return render_template('view/client/donatur-detail.html', donatur=donatur_data)
