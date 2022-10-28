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


@app.route("/sign_up")
def check_sign_up():
    entities.get_repo()

    if "current_user" not in session:
        return render_template("sign_up.html")
    else:
        return render_template("profile.html")


@app.route("/sign_up", methods=['POST'])
def sign_up():
    entities.get_repo()

    if "current_user" in session:
        return render_template("profile.html")

    try:
        repository = entities.get_repo()
        session['current_user'] = repository.create_user(request.form.get('username'), request.form.get('email'), request.form.get('password'))
        return redirect(url_for('profile'))
    except Exception as e:
        return render_template("sign_up.html", exeption=True, exep=str(e))
    # POST: request.form.get('<key name>') #### GET: request.args.get('<key name>') #


@app.route("/log_in")
def check_log_in(where="profile.html"):
    entities.get_repo()
    if "current_user" in session:
        return render_template(where)
    return render_template("log_in.html")


@app.route("/log_in", methods=['POST'])
def log_in():
    entities.get_repo()
    if "current_user" in session:
        return render_template("profile.html")

    try:
        repository = entities.get_repo()
        session["current_user"] = repository.log_in(request.form.get('email'), request.form.get('password'))
        return render_template("profile.html")
    except Exception as e:
        return render_template("log_in.html", exeption=True, exep=str(e))


@app.route("/log_out")
def log_out():
    if "current_user" not in session:
        return render_template("log_in.html")

    try:
        session.pop("current_user")
    except Exception:
        pass
    return render_template("index.html")


@app.route("/create_category")
def check_create_category():
    if "current_user" in session:
        return render_template("create_category.html")
    return render_template("log_in.html")


@app.route("/create_category", methods=['POST'])
def create_category():
    if "current_user" not in session:
        return render_template("log_in.html")

    try:
        repository = entities.get_repo()
        category_id = repository.create_category(session["current_user"], request.form.get('title'), request.form.get('description'))
        return redirect(url_for('category', category_id=category_id))
    except Exception as e:
        return render_template("create_category.html", exeption=True, exep=str(e))


@app.route("/category")
def category():
    return "dfgj"