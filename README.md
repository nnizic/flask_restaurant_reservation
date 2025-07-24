# 🍽️ Flask + MySQL Sustav za rezervaciju stolova

Jednostavni web sustav za rezervaciju stolova u restoranu, izrađen pomoću **Flaska**, **MySQL-a** i **SQLAlchemy ORM-a**.

---

## ✅ Funkcionalnosti

- Prikaz dostupnih stolova i rezervacija po datumu
- Rezervacija stola na određeni datum i vrijeme
- Validacija dvostrukih rezervacija
- Potvrda i odbijanje rezervacija od strane admina:
  - putem admin panela ili
  - direktno iz e-mail poruke
- Slanje email potvrda korisniku (potvrda / odbijanje)
- Admin dashboard s:
  - pregledom i filtriranjem rezervacija po datumu i statusu
  - osnovnim statistikama (danas, potvrđeno, na čekanju itd.)
  - dodavanjem i brisanjem stolova (nije moguće brisanje stola s rezervacijom)
- Admin login sustav (autentifikacija)
- Flash poruke s automatskim nestajanjem
- Bootstrap dizajn + spinner pri slanju rezervacije
- .env konfiguracija za sigurnost osjetljivih podataka

---

## 🧱 Struktura projekta

```
restaurant-reservation/
├── app/
│ ├── init.py # Inicijalizacija aplikacije, baza, mail, login
│ ├── models.py # SQLAlchemy modeli (Admin, Table, Reservation)
│ ├── routes.py # Flask rute (korisnik i admin)
│ └── templates/ # HTML predlošci
│ ├── base.html # Layout s Bootstrapom i flash porukama
│ ├── index.html # Početna stranica - stolovi
│ ├── reserve.html # Forma za rezervaciju
│ ├── admin.html # Admin panel s filtrima i statistikama
│ └── email/ # HTML poruke za admina i korisnika
│ ├── notify_admin.html
│ ├── user_confirmed.html
│ └── user_rejected.html
├── static/ # (opcionalno) CSS/JS datoteke
├── config.py # Konfiguracija aplikacije (.env podrška)
├── run.py # Pokretanje aplikacije
├── requirements.txt # Python ovisnosti
├── .env # Tajne varijable (lokalno)
├── .gitignore # Ignorirane datoteke
└── README.md # Dokumentacija projekta
```

---

## ⚙️ Pokretanje

1. Instaliraj ovisnosti:

   ```bash
   pip install -r requirements.txt

   ```

   Konfiguriraj .env datoteku:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@localhost/restaurant
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=admin@example.com
```

Kreiraj bazu u MySQL-u:

```
CREATE DATABASE restaurant;

```

Inicijaliziraj bazu i migracije:

```
flask db init
flask db migrate -m "init"
flask db upgrade

```

Pokreni aplikaciju:

```
flask run

```

Otvori u pregledniku:

    http://127.0.0.1:5000/

🔐 Admin login

Prvi admin unosi se direktno iz baze. Primjer SQL unosa:

```
INSERT INTO admin (username, password_hash) VALUES (
'admin',
'<hash lozinke>'
);

```

Hash možeš generirati u Python konzoli:

```
from werkzeug.security import generate_password_hash
generate_password_hash("tvoja_lozinka")

```

🧪 Napomena

    Flash poruke se automatski gase nakon 5 sekundi.

    Spinner se prikazuje tijekom slanja rezervacije.

    Admin dobiva poruku mailom sa "Potvrdi" i "Odbij" gumbima.

    Korisnik dobiva potvrdu mailom nakon adminove akcije.

    Deployment moguć na server s WSGI podrškom (Passenger, Apache, Nginx+Gunicorn, itd.)

📌 Ovisnosti

    Flask

    Flask-SQLAlchemy

    Flask-Migrate

    Flask-Mail

    Flask-Login

    python-dotenv

    PyMySQL

    Bootstrap (via CDN)

📬 Kontakt

Za komentare, ideje i proširenja slobodno se javi! 🙂
