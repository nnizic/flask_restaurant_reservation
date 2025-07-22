# 🍽️ Flask + MySQL Sustav za rezervaciju stolova

Jednostavni web sustav za rezervaciju stolova u restoranu, izrađen pomoću **Flaska**, **MySQL-a** i **SQLAlchemy ORM-a**.

---

## ✅ Funkcionalnosti

- Prikaz dostupnih stolova
- Rezervacija stola na određeni datum i vrijeme
- Validacija dvostrukih rezervacija
- Admin sučelje s:
  - pregledom i filtriranjem rezervacija (po statusu i datumu)
  - potvrdom i odbijanjem rezervacija (i preko emaila)
  - statistikama (ukupno, danas, potvrđene, na čekanju, odbijene)
  - upravljanjem stolovima (dodavanje i brisanje)
- Email obavijesti:
  - Admin prima mail s botunima za potvrdu/odbijanje rezervacije
  - Korisnik prima mail s informacijom o statusu rezervacije (potvrđeno/odbijeno)
- Admin autentikacija (login/logout)
- Bootstrap dizajn za sve stranice

---

## 🧱 Struktura projekta

```
restaurant-reservation/
├── app/
│ ├── init.py # Inicijalizacija aplikacije i baze
│ ├── models.py # SQLAlchemy modeli za stolove, rezervacije i admina
│ ├── routes.py # Flask rute (view funkcije)
│ ├── email_utils.py # Slanje emailova adminu i korisnicima
│ └── templates/ # HTML predlošci
│ ├── base.html
│ ├── index.html
│ ├── reserve.html
│ ├── admin.html
│ └── login.html
├── static/ # (opcionalno) CSS/JS datoteke
├── config.py # Konfiguracija aplikacije (baza, ključ itd.)
├── run.py # Pokretanje aplikacije
├── requirements.txt # Python ovisnosti
└── README.md # Dokumentacija projekta
```

---

## ⚙️ Pokretanje

1. Instaliraj ovisnosti:

   ```bash
   pip install -r requirements.txt
   ```

   Konfiguriraj config.py:

```

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:lozinka@localhost/restaurant'
SECRET_KEY = 'tvoj_tajni_kljuc'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'tvoj.email@gmail.com'
MAIL_PASSWORD = 'tvoja_app_lozinka'

```

Kreiraj bazu u MySQL-u:

```
CREATE DATABASE restaurant;

Inicijaliziraj migraciju baze (ako koristiš Flask-Migrate):

flask db init
flask db migrate
flask db upgrade
```

Pokreni aplikaciju:

```
python run.py
```

Otvori u pregledniku:

http://127.0.0.1:5000/

🔐 Admin prijava

Dodaj ručno admin korisnika u bazu (ili kroz skriptu):

```
from app import db
from app.models import AdminUser
admin = AdminUser(username='admin', password_hash=generate_password_hash('lozinka'))
db.session.add(admin)
db.session.commit()
```

📌 Ovisnosti

Flask

Flask-SQLAlchemy

Flask-Migrate

Flask-Mail

Flask-Login

PyMySQL

Bootstrap 5 (CDN)

🧪 Primjedbe

Za slanje emailova s Gmailom koristi se "App Password" ako je uključena 2FA.

Aplikacija trenutno koristi osnovnu zaštitu – za produkciju preporučujemo .env, SSL i CSRF zaštitu.

Razgraničeni pristup korisnika i admina može se dodatno proširiti (npr. korisnički paneli).

📬 Kontakt

Za pitanja, prijedloge ili proširenja slobodno se javi! 🙂

```

```
