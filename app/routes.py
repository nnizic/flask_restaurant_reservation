# routes.py

from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask import current_app as app

from . import db
from .models import Reservation, Table


@app.route("/")
def index():
    tables = Table.query.all()
    return render_template("index.html", tables=tables)


@app.route("/reserve/<int:table_id>", methods=["GET", "POST"])
def reserve(table_id):
    table = Table.query.get_or_404(table_id)
    if request.method == "POST":
        name = request.form["name"]
        date = datetime.strptime(request.form["date"], "%Y-%m-%dT%H:%M")
        existing = Reservation.query.filter_by(table_id=table.id, date=date).first()
        if existing:
            flash("Rezervacija već postoji za taj datum i vrijeme.", "danger")
            return redirect(url_for("reserve", table_id=table.id))
        reservation = Reservation(name=name, date=date, table_id=table.id)
        db.session.add(reservation)
        db.session.commit()
        flash("Rezervacija uspješna!", "success")
        return redirect(url_for("index"))
    return render_template("reserve.html", table=table)


@app.route("/admin")
def admin():
    reservations = Reservation.query.order_by(Reservation.date.desc()).all()
    tables = Table.query.order_by(Table.number).all()
    return render_template("admin.html", reservations=reservations, tables=tables)


@app.route("/admin/confirm/<int:reservation_id>", methods=["POST"])
def confirm_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    reservation.status = "confirmed"
    db.session.commit()
    flash("Rezervacija potvrđena.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/delete/<int:reservation_id>", methods=["POST"])
def delete_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    flash("Rezervacija obrisana.", "danger")
    return redirect(url_for("admin"))


@app.route("/admin/add_table", methods=["POST"])
def add_table():
    number = request.form.get("number")
    capacity = request.form.get("capacity")

    if not number or not capacity:
        flash("Broj i kapacitet su obavezni.", "danger")
        return redirect(url_for("admin"))

    if Table.query.filter_by(number=number).first():
        flash("Stol s tim brojem već postoji", "danger")
        return redirect(url_for("admin"))

    new_table = Table(number=number, capacity=capacity)
    db.session.add(new_table)
    db.session.commit()
    flash("Stol dodan.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/delete_-table/<int:table_id>", methods=["POST"])
def delete_table(table_id):
    table = Table.query.get_or_404(table_id)
    if table.reservations:
        flash("Stol ne može biti obrisan jer ima rezervacije.", "danger")
        return redirect(url_for("admin"))

    db.session.delete(table)
    db.session.commit()
    flash("Stol obrisan.", "success")
    return redirect(url_for("admin"))
