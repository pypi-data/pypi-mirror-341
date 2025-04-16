from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

def login_logic(users,redirect_page='',render_page=''):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for(redirect_page))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template(render_page)

def login_template(users,redirect_page=''):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for(redirect_page))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return '''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
    <style>
        /* Basic reset */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #74ebd5, #acb6e5);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .form-container {
            background-color: white;
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
            text-align: center;
        }

        h2 {
            margin-bottom: 1.5rem;
            color: #333;
        }

        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 0.8rem 1rem;
            margin: 0.5rem 0 1rem 0;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }

        input:focus {
            border-color: #fda085;
            outline: none;
        }

        button {
            width: 100%;
            padding: 0.8rem;
            background-color: blue;
            border: none;
            border-radius: 8px;
            color: white;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #skytblue;
        }

        p {
            margin-top: 1rem;
            font-size: 0.95rem;
        }

        a {
            color: blue;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h2>Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required/>
            <input type="password" name="password" placeholder="Password" required/>
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <a href="/register">Register</a></p>
    </div>
</body>
</html>

'''


def register_logic(users, redirect_page='', render_page=''):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if users.find_one({'username': username}):
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if users.find_one({'email': email}):
            flash('Username already exists')
            return redirect(url_for('register'))

        users.insert_one({'username': username,'email':email, 'password': password})
        flash('Registration successful. Please log in.')
        return redirect(url_for(redirect_page))

    return render_template(render_page)

def register_template(users, redirect_page=''):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if users.find_one({'username': username}):
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if users.find_one({'email': email}):
            flash('Username already exists')
            return redirect(url_for('register'))

        users.insert_one({'username': username,'email':email, 'password': password})
        flash('Registration successful. Please log in.')
        return redirect(url_for(redirect_page))

    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Register</title>
    <style>
        /* Reset some basic styles */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #74ebd5, #acb6e5);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .form-container {
            background-color: white;
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
            text-align: center;
        }

        h2 {
            margin-bottom: 1.5rem;
            color: #333;
        }

        input[type="text"],
        input[type="password"],
         input[type="email"] {
            width: 100%;
            padding: 0.8rem 1rem;
            margin: 0.5rem 0 1rem 0;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }

        input:focus {
            border-color: #74ebd5;
            outline: none;
        }

        button {
            width: 100%;
            padding: 0.8rem;
            background-color: blue;
            border: none;
            border-radius: 8px;
            color: white;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: blue;
        }

        p {
            margin-top: 1rem;
            font-size: 0.95rem;
        }

        a {
            color: blue;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h2>Register</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required/>
            <input type="email" name="email" placeholder="Email" required/>
            <input type="password" name="password" placeholder="Password" required/>
            <button type="submit">Register</button>
        </form>
        <p>Already have an account? <a href="/login">Login</a></p>
    </div>
</body>
</html>


'''


def contact_logic(collection, render_page=''):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        message = request.form['message']
        
        collection.insert_one({
            'username': username,
            'email': email,
            'message': message
        })
        flash('Message sent successfully!')
        
    return render_template(render_page)

def contact_template(collection):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        message = request.form['message']
        
        collection.insert_one({
            'username': username,
            'email': email,
            'message': message
        })
        flash('Message sent successfully!')
        
    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Contact</title>
    <style>
        /* Reset styles */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #cfd9df, #e2ebf0);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .form-container {
            background-color: white;
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 500px;
            text-align: center;
        }

        h2 {
            margin-bottom: 1.5rem;
            color: #333;
        }

        input[type="text"],
        input[type="email"],
        textarea {
            width: 100%;
            padding: 0.8rem 1rem;
            margin: 0.5rem 0 1rem 0;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
            resize: vertical;
        }

        input:focus,
        textarea:focus {
            border-color: #a0bacc;
            outline: none;
        }

        textarea {
            min-height: 120px;
        }

        button {
            width: 100%;
            padding: 0.8rem;
            background-color: blue;
            border: none;
            border-radius: 8px;
            color: white;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: blue;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h2>Contact Form</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required/>
            <input type="email" name="email" placeholder="Email" required/>
            <textarea name="message" placeholder="Enter your message here..." required></textarea>
            <button type="submit">Submit</button>
        </form>
    </div>
</body>
</html>

'''


def profile_logic():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', username=session['username'])

def logout_logic():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))