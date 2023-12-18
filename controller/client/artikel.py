from . import *


@app.route('/artikel')
def artikel():
    artikel = db["artikel"]
    artikel_data = artikel.find().sort("createdAt", pymongo.DESCENDING)
    return render_template('view/client/artikel.html', artikel=artikel_data)


@app.route('/artikel_detail/<id>')
def artikel_detail(id):
    artikel = db["artikel"]
    artikel_data = artikel.find_one({"_id": ObjectId(id)})
    return render_template('view/client/artikel-detail.html', artikel=artikel_data)
