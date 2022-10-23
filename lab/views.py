from lab import app, entities
from flask import render_template, session, request, redirect, url_for


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/profile")
def profile():
    entities.get_repo()
    if "current_user" not in session:
        return render_template("log_in.html")
    return render_template("profile.html")


@app.route("/signUp", methods=['GET'])
def check_sign_up():
    if "current_user" not in session:
        return render_template("sign_up.html")
    else:
        return render_template("profile.html")


@app.route("/signUp", methods=['POST'])
def sign_up():
    if "current_user" in session:
        return render_template("profile.html")

    try:
        repository = entities.get_repo()
        session['current_user'] = repository.create_user(request.form.get('username'), request.form.get('email'), request.form.get('password'))
        return redirect(url_for('profile'))
    except Exception as e:
        return render_template("sign_up.html", exeption=True, exep=str(e))
    # POST: request.form.get('<key name>') #### GET: request.args.get('<key name>') #


@app.route("/logIn")
def check_log_in():
    if "current_user" in session:
        return render_template("profile.html")
    return render_template("log_in.html")


@app.route("/logIn", methods=['POST'])
def log_in():
    if "current_user" in session:
        return render_template("profile.html")

    try:
        repository = entities.get_repo()
        session['current_user'] = repository.log_in_by_email(request.form.get('email'), request.form.get('password'))
        return render_template("profile.html")
    except Exception as e:
        return render_template("log_in.html", exeption=True, exep=str(e))


@app.route("/logOut")
def log_out():
    try:
        session.pop("current_user")
    except Exception:
        pass
    return render_template("index.html")

