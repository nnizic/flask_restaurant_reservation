# routes.py

from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask import current_app as app
from flask_mail import Message

from . import db
from . import mail
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
        email = request.form["email"]
        date = datetime.strptime(request.form["date"], "%Y-%m-%dT%H:%M")
        existing = Reservation.query.filter_by(table_id=table.id, date=date).first()
        if existing:
            flash("Rezervacija već postoji za taj datum i vrijeme.", "danger")
            return redirect(url_for("reserve", table_id=table.id))
        reservation = Reservation(name=name, email=email, date=date, table_id=table.id)
        db.session.add(reservation)
        db.session.commit()

        # pošalji adminu mail
        msg = Message(f"Nova rezervacija: {name}", recipients=["project.virtualis@gmail.com"])
        msg.body = f"""Nova rezervacija:
        Ime: {name}
        Stol: #{table.number}
        Datum: {date.strftime('%d.%m.%Y %H:%M')}

        Potvrdi ili odbij:
        http://localhost:5000/admin/confirm_email/{reservation.id}
        http://localhost:5000/admin/reject_email/{reservation.id}
        """
        mail.send(msg)

        flash("Rezervacija zatražena Čekajte potvrdu.!", "success")
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


# rute za potvrdu i odbijanje rezervacije putem mail-as
@app.route("/admin/confirm_email/<int:reservation_id>")
def confirm_email(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    if reservation.status != "pending":
        return "Rezervacija je već obrađena!"

    reservation.status = "confirmed"
    db.session.commit()

    send_user_notification(reservation, accepted=True)
    return "Rezervacije potvrđena. Korisnik obaviješten."


@app.route("/admin/reject_email/<int:reservation_id>")
def reject_email(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    if reservation.status != "rejected":
        return "Rezervacija je već obrađena."

    reservation.status = "rejected"
    db.session.commit()

    send_user_notification(reservation, accepted=False)
    return "Rezervacija je odbijena. Korisnik je obaviješten."


def send_user_notification(reservation, accepted=True):
    """funkcija za slanje maila korisniku"""
    msg = Message("Status vaše rezervacije", recipients=[f"{reservation.email}"])
    status = "potvrđena" if accepted else "odbijena"
    msg.body = f"""
    Poštovani {reservation.name},

    Vaša rezervacija je {status}.


    Detalji:
    Stol: #{reservation.table.number}
    Datum: {reservation.date.strftime('%d.%m.%Y %H:%M')}

    Hvala što koristite naš sustav.
    """

    mail.send(msg)
