from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, static_url_path='', static_folder='static/',)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hosteldata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class HostelInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    totalhostels = db.Column(db.Integer, nullable=False)
    boyshostels = db.Column(db.Integer, nullable=False)
    girlshostels = db.Column(db.Integer, nullable=False)
    totalstudents = db.Column(db.Integer, nullable=False)
    totalboys = db.Column(db.Integer, nullable=False)
    totalgirls = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'HostelInfo' + str(self.id)


class Hostel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hname = db.Column(db.String(30), nullable=False)
    warden = db.Column(db.String(30), nullable=False)
    nrooms = db.Column(db.Integer, nullable=False)
    nstudents = db.Column(db.Integer, nullable=False)
    fee = db.Column(db.Integer, nullable=False)
    messfee = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'Hostel' + str(self.id)


@app.route('/')
def index():
    hostels = Hostel.query.all()
    return render_template("index.html", hostels=hostels)


@app.route('/admin')
def admin():
    info = HostelInfo.query.get(1)
    return render_template("dashboard.html", info=info)


@app.route('/hostels')
def hostel():
    hostels = Hostel.query.all()
    return render_template('hostels.html', hostels=hostels)


@app.route('/hostel-info/<int:id>',methods=['GET'])
def abc(id):
    info=Hostel.query.get(id)
    return render_template("k.html",info=info)

@app.route('/hostels/delete/<int:id>', methods=['GET', 'POSTS'])
def delete(id):
    hostel = Hostel.query.get_or_404(id)
    info = HostelInfo.query.get(1)
    info.totalhostels = info.totalhostels - 1
    info.boyshostels = info.boyshostels - 1
    info.totalstudents -= int(hostel.nstudents)
    db.session.delete(hostel)
    db.session.commit()
    return redirect('/hostels')


@app.route('/add-hostel', methods=['GET', 'POST'])
def addhostel():
    if request.method == 'POST':
        info = HostelInfo.query.get(1)
        info.totalhostels = info.totalhostels + 1
        info.boyshostels = info.boyshostels + 1
        hname = request.form['hname']
        warden = request.form['warden']
        nrooms = request.form['nrooms']
        nstudents = request.form['nstudents']
        info.totalstudents += int(nstudents)
        fee = request.form['fee']
        messfee = request.form['messfee']
        new_hostel = Hostel(hname=hname, warden=warden, nrooms=nrooms,
                            nstudents=nstudents, fee=fee, messfee=messfee)
        db.session.add(new_hostel)
        db.session.commit()
        return redirect('/admin')
    else:
        return render_template('addhostel.html')


@app.route('/hostels/edit/<int:id>', methods=['GET', 'POST'])
def update(id):
    info = Hostel.query.get_or_404(id)
    if request.method == 'POST':
        info2 = HostelInfo.query.get(1)
        info2.totalstudents -= int(info.nstudents)
        info.hname = request.form['hname']
        info.warden = request.form['warden']
        info.nrooms = request.form['nrooms']
        info.nstudents = request.form['nstudents']
        info.fee = request.form['fee']
        info.messfee = request.form['messfee']
        info2.totalstudents += int(info.nstudents)
        db.session.commit()
        return redirect('/hostels')
    else:
        return render_template('edit-hostel.html', info=info)


@app.route('/edit-info', methods=['GET', 'POST'])
def edit():
    info = HostelInfo.query.get_or_404(1)
    if request.method == 'POST':
        info.totalhostels = request.form['totalhostels']
        info.boyshostels = request.form['boyshostels']
        info.girlshostels = request.form['girlshostels']
        info.totalstudents = request.form['totalstudents']
        info.totalboys = request.form['totalboys']
        info.totalgirls = request.form['totalgirls']
        db.session.commit()
        return redirect('/admin')
    else:
        return render_template('edit.html', info=info)


if __name__ == "__main__":
    app.run(debug=True)
