from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)

@app.route("/")
def index():
    jobs = Job.query.all()
    return render_template("index.html", jobs=jobs)

@app.route("/add", methods=["POST"])
def add():
    job = Job(
        company=request.form["company"],
        role=request.form["role"],
        status=request.form["status"]
    )
    db.session.add(job)
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
