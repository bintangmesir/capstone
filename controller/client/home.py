from . import *


@app.route('/')
def home():
    artikel = db["artikel"]
    aktivitas = db["aktivitas"]
    artikel_data = artikel.find().sort("createdAt", pymongo.DESCENDING)
    aktivitas_data = aktivitas.find().sort("createdAt", pymongo.DESCENDING)
    return render_template('view/index.html', artikel=artikel_data, aktivitas=aktivitas_data)
