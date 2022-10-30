import json
from lab import app, entities
from flask import render_template, session, request, redirect, url_for


def check_user_not_in_session(func):
    def inner(*args, **kwargs):
        entities.get_repo()
        if "current_user" not in session:
            return redirect(url_for('log_in'))
        return func(*args, **kwargs)
    inner.__name__ = func.__name__  # why?
    return inner


@app.route("/")
def main():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('main'))


@app.route("/profile")
@check_user_not_in_session
def profile():
    repository = entities.get_repo()
    user = repository.get_user(session['current_user'])
    return render_template("profile.html", data=json.dumps(user.get_all_categories()))


@app.route("/sign_up")
def check_sign_up():
    entities.get_repo()

    if "current_user" not in session:
        return render_template("sign_up.html")
    else:
        return redirect(url_for('profile'))


@app.route("/sign_up", methods=['POST'])
def sign_up():
    entities.get_repo()

    if "current_user" in session:
        return redirect(url_for('profile'))

    try:
        repository = entities.get_repo()
        session['current_user'] = repository.create_user(request.form.get('username'), request.form.get('email'), request.form.get('password'))
        return redirect(url_for('profile'))
    except Exception as e:
        return render_template("sign_up.html", data=json.dumps({"exeption": True, "exep": str(e)}))
    # POST: request.form.get('<key name>') #### GET: request.args.get('<key name>') #


@app.route("/log_in")
def check_log_in():
    entities.get_repo()
    if "current_user" in session:
        return redirect(url_for('profile'))
    return render_template("log_in.html")


@app.route("/log_in", methods=['POST'])
def log_in():
    entities.get_repo()
    if "current_user" in session:
        return redirect(url_for('profile'))

    try:
        repository = entities.get_repo()
        session["current_user"] = repository.log_in(request.form.get('email'), request.form.get('password'))
        return redirect(url_for('profile'))
    except Exception as e:
        return render_template("log_in.html", data=json.dumps({"exeption": True, "exep": str(e)}))


@app.route("/log_out")
def log_out():
    try:
        session.pop("current_user")
    except Exception:
        pass
    return redirect(url_for('main'))


@app.route("/create_category")
@check_user_not_in_session
def check_create_category():
    return render_template("create_category.html")


@app.route("/create_category", methods=['POST'])
@check_user_not_in_session
def create_category():
    try:
        repository = entities.get_repo()
        category_id = repository.create_category(session["current_user"], request.form.get('title'), request.form.get('description'))
        return redirect(url_for('profile'))
    except Exception as e:
        return render_template("create_category.html", data=json.dumps({"exeption": True, "exep": str(e)}))


@app.route("/category", methods=['POST'])
@check_user_not_in_session
def category():
    repository = entities.get_repo()
    user = repository.get_user(session['current_user'])
    category_id = request.form.get('id')
    data = user.get_category_by_id(category_id)
    if not data:
        return redirect(url_for('profile'))
    return render_template("category.html", data=json.dumps(data))


@app.route("/delete_category", methods=['POST'])
@check_user_not_in_session
def delete_category():
    repository = entities.get_repo()
    repository.delete_category(session['current_user'], request.form.get('category_id'))
    return redirect(url_for('profile'))


@app.route("/update_category", methods=['POST'])
@check_user_not_in_session
def update_category():
    category_id = request.form.get('category_id')
    title = request.form.get('title')
    description = request.form.get('description')
    if request.form.get('from_category_page'):
        return render_template("update_category.html", data=json.dumps({"category_id": category_id,
                                                                        "title": title,
                                                                        "description": description}))
    try:
        repository = entities.get_repo()
        repository.update_category(session["current_user"], category_id, title, description)
        return redirect(url_for('profile'))
    except Exception as e:
        return render_template("update_category.html", data=json.dumps({"category_id": category_id,
                                                                        "title": title,
                                                                        "description": description,
                                                                        "exeption": True,
                                                                        "exep": str(e)}))


@app.route("/all_costs")
@check_user_not_in_session
def all_costs():
    all = entities.get_repo().get_all_costs(session['current_user'])
    # print(all)
    return render_template("all_costs.html", data=json.dumps(all))


@app.route("/cost", methods=['POST'])
@check_user_not_in_session
def cost():
    repository = entities.get_repo()
    user = repository.get_user(session['current_user'])
    cost_id = request.form.get('cost_id')
    data = user.get_cost_by_id(cost_id)
    if not data:
        return redirect(url_for('profile'))
    return render_template("cost.html", data=json.dumps(data))


@app.route("/delete_cost", methods=['POST'])
@check_user_not_in_session
def delete_cost():
    repository = entities.get_repo()
    if repository.USERS[session['current_user']].delete_cost(request.form.get('cost_id')):
        return redirect(url_for('profile'))
    return redirect(url_for('main'))


@app.route("/update_cost", methods=['POST'])
@check_user_not_in_session
def update_cost():
    cost_id = request.form.get('cost_id')
    money = request.form.get('money')
    description = request.form.get('description')
    if request.form.get('from_cost_page'):
        return render_template("update_cost.html", data=json.dumps({"cost_id": cost_id,
                                                                    "money": money,
                                                                    "description": description}))
    repository = entities.get_repo()
    repository.update_cost(session["current_user"], cost_id, money, description)
    print("cost_id " + cost_id)
    print("money " + money)
    print("description " + description)
    return redirect(url_for('profile'))


@app.route("/create_cost", methods=['POST'])
@check_user_not_in_session
def create_cost():
    if request.form.get('from_category_page'):
        return render_template("create_cost.html", data=json.dumps({'category_id': request.form.get('category_id')}))

    repository = entities.get_repo()
    repository.USERS[session["current_user"]].create_cost(request.form.get('category_id'),
                                                          request.form.get('description'),
                                                          request.form.get('money'))
    return redirect(url_for('profile'))
