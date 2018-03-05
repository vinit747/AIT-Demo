import os

from flask import Flask,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy

proj_dir = os.path.dirname(os.path.abspath(__file__))

database_file = "sqlite:///{}".format(os.path.join(proj_dir, "persondatabase.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


class person(db.Model):
    name = db.Column(db.String(80),unique=True, nullable=False,primary_key=True)
    # id = db.Column(db.int(10),primary_key=True)



    def __repr__(self):
        return "<HI> ".format(self.name)

@app.route('/')
def index():
    return "Method is : "+str(request.method)
    # return "Hello World"
#default GET method


@app.route("/preq",methods = ["GET","POST"])
def preq():
    if request.method == "POST":
        return "Using the post Request"
    else:
        return "Using GET request"


@app.route("/tuna")
def tuna():
    return "<h1>Tuna is awesome </h1>"

@app.route("/profile/<username>")
def profile(username):
    # return "User Name : "+username
    return render_template("prof.html",name=username)

@app.route("/dash/<int:rno>")
def dash(rno):
    return "Roll Number : "+str(rno)



@app.route('/perso',methods=["GET","POST"])
def perso():
    if request.form:
        Person = person(name=request.form.get('name'))
        db.session.add(Person)
        db.session.commit()
    people = person.query.all()
    return render_template("pers.html",ppl = people)


@app.route("/update",methods=["POST"])
def update():
    newname = request.form.get("newname")
    oldname = request.form.get("oldname")
    Person = person.query.filter_by(name=oldname).first()
    Person.name = newname
    db.session.commit()
    return redirect("/perso")

@app.route("/delete",methods=["POST"])
def delete():
    name = request.form.get("name")
    Person = person.query.filter_by(name=name).first()
    db.session.delete(Person)
    db.session.commit()
    return redirect("/perso")


@app.route("/map/")
@app.route("/map/<user>")
def map(user = None):
    return render_template("prof1.html",name=user)
    

@app.route("/shop")
def shop():
    items = ["Mango","Guava","Raspberries"]
    return render_template("shopping.html",list=items)





if __name__ =="__main__":
    app.run(debug=True)