
# 🔐 Deepan Flask package for Auth & Contact 

A lightweight and ready-to-use authentication and contact form module for Flask-based web applications — perfect for hackathons and rapid development. This package streamlines your development process by offering reusable logic and UI templates for:

- ✅ Login  
- ✅ Registration  
- ✅ Contact Form
- ✅ Profile Details

---

## 🚀 Features

- Plug-and-play **Flask routes and forms**
- Uses **MongoDB** for data storage
- Passwords securely hashed using `werkzeug.security`
- Stylish, responsive templates using **pure HTML/CSS**
- Supports session management and flash messages

---

## 🧰 Technologies Used

- **Python (Flask)**
- **MongoDB (pymongo)**
- **Werkzeug** for password hashing
- **HTML/CSS** for frontend templates

---

## 📁 Folder Structure

```bash
your_project/
│
├── app.py                 # Main Flask application
├── templates/
│   ├── login.html         # (If using external templates)
│   ├── register.html      
│   └── contact.html       
└── ...
```
---

## How to use my package

### 1. Install Dependencies

```bash
pip install deepan_flask flask pymongo

```
### 2. Create app.py
Import the package:

```bash python
from deepan_flask import (
    login_logic, register_logic, logout_logic, contact_logic,
    login_template, register_template, contact_template, profile_logic
)
from flask import Flask, redirect, url_for
from pymongo import MongoClient

```

### 3. Setup Flask and MongoDB in app.py:

```bash python
app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')

db = client['user_db']
users = db['users']
contacts = db['contacts']
```

### 4. Creating login,register, contact and profile route with new package code:

```bash python
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_template(users, redirect_page='login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_template(users, redirect_page='profile')

@app.route('/contact',methods=['GET', 'POST'])
def contact():
    return contact_template(contacts)

@app.route('/profile')
def profile():
    return profile_logic()

@app.route('/logout')
def logout():
    return logout_logic()

if __name__ == '__main__':
    app.run(debug=True)
```
### 5. Run the app.py file:

```bash python
python app.py
```

## Usage Options:
### You can use this package in two ways:
#### 1. With Templates — Use *_template() functions for ready-to-use UIs.
#### 2. With Logic Only — Use *_logic() functions to integrate with your custom templates.

# Release Cycle
## The latest version is released every weekend with improvements and fixes.

## Happy Coding!
### Crafted with ❤️ by Deepan Balu