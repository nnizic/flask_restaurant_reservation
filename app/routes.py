# routes.py

from datetime import date, datetime

from flask import flash, redirect, render_template, request, url_for
from flask import current_app as app
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from sqlalchemy import and_, func

from . import db
from . import mail
from .models import Admin, Reservation, Table


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

        # HTML verzija s botunima
        msg.html = f"""
        <p><strong>Nova rezervacija</strong></p>
        <ul>
          <li>Ime: {name}</li>
          <li>Stol: #{table.number}</li>
          <li>Datum: {date.strftime('%d.%m.%Y %H:%M')}</li>
        </ul>
        
        <p>Odaberi što želiš napraviti:</p>
        
        <a href="http://localhost:5000/admin/confirm_email/{reservation.id}"
           style="display:inline-block; padding:10px 20px; background-color:#28a745; color:white; text-decoration:none; border-radius:5px;">
           ✅ Potvrdi
        </a>
        
        <a href="http://localhost:5000/admin/reject_email/{reservation.id}"
           style="display:inline-block; padding:10px 20px; background-color:#dc3545; color:white; text-decoration:none; border-radius:5px; margin-left:10px;">
           ❌ Odbij
        </a>
        """

        mail.send(msg)

        flash("Rezervacija zatražena Čekajte potvrdu.!", "success")
        return redirect(url_for("index"))
    return render_template("reserve.html", table=table)


@app.route("/admin")
@login_required
def admin():
    status_filter = request.args.get("status")
    date_filter = request.args.get("date")

    query = Reservation.query

    if status_filter:
        query = query.filter_by(status=status_filter)

    if date_filter:
        try:
            parsed_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
            query = query.filter(func.date(Reservation.date) == parsed_date)
            print("Filter po datumu:", parsed_date)
        except ValueError:
            flash("Neispravan format datuma", "danger")

    reservations = query.order_by(Reservation.date.desc()).all()
    tables = Table.query.order_by(Table.number).all()

    # Statistika
    total = Reservation.query.count()
    confirmed = Reservation.query.filter_by(status="confirmed").count()
    pending = Reservation.query.filter_by(status="pending").count()
    rejected = Reservation.query.filter_by(status="rejected").count()
    today = Reservation.query.filter(func.date(Reservation.date) == date.today()).count()

    stats = {"total": total, "confirmed": confirmed, "pending": pending, "rejected": rejected, "today": today}

    return render_template("admin.html", reservations=reservations, tables=tables, stats=stats)


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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            flash("Uspješna prijava!", "success")
            return redirect(url_for("admin"))
        else:
            flash("Neispravno korisničko ime ili lozinka", "danger")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Odjavljen si", "info")
    return redirect(url_for("login"))
