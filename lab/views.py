import json
from lab import app, entities
from flask import render_template, session, request, redirect, url_for
from flask_smorest import abort


# @app.route("/")
# def main():
#     return render_template("index.html")
#
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return redirect(url_for('main'))


# @app.route("/profile")
# def profile():
#     repository = entities.get_repo()
#     user = repository.USERS[session['current_user']]
#     return render_template("profile.html", data=json.dumps(user.get_all_categories()))


# @app.route("/sign_up")
# def check_sign_up():
#     entities.get_repo()
#
#     if "current_user" not in session:
#         return render_template("sign_up.html")
#     else:
#         return redirect(url_for('profile'))
#
#
@app.post('/create_user')  # {"username": "<>", "email": "<>", "password": "<>"}
def create_user(json_request):
    repo = entities.get_repo()
    request = json.loads(json_request)
    try:
        username = request['username']
        email = request['email']
        password = request['password']
    except KeyError:
        abort(400, message='user data is not found. must be specified "username", "email" and "password".')
    result = repo.create_user(username, email, password)
    return json.dumps(result)


    # if "current_user" in session:
    #     return redirect(url_for('profile'))
    #
    # try:
    #     repository = entities.get_repo()
    #     session['current_user'] = repository.create_user(request.form.get('username'), request.form.get('email'),
    #                       request.form.get('password'))
    #     return redirect(url_for('profile'))
    # except Exception as e:
    #     return render_template("sign_up.html", data=json.dumps({"exeption": True, "exep": str(e)}))
    # POST: request.form.get('<key name>') #### GET: request.args.get('<key name>') #
#
#
# @app.route("/log_in")
# def check_log_in():
#     entities.get_repo()
#     if "current_user" in session:
#         return redirect(url_for('profile'))
#     return render_template("log_in.html")
#
#
# @app.route("/log_in", methods=['POST'])
# def log_in():
#     entities.get_repo()
#     if "current_user" in session:
#         return redirect(url_for('profile'))
#
#     try:
#         repository = entities.get_repo()
#         session["current_user"] = repository.log_in(request.form.get('email'), request.form.get('password'))
#         return redirect(url_for('profile'))
#     except Exception as e:
#         return render_template("log_in.html", data=json.dumps({"exeption": True, "exep": str(e)}))
#
#
# @app.route("/log_out")
# def log_out():
#     try:
#         session.pop("current_user")
#     except Exception:
#         pass
#     return redirect(url_for('main'))


# @app.route("/create_category")
# def check_create_category(json_request):
#
#     return render_template("create_category.html")


@app.route("/create_category", methods=['POST'])  # {"user_id": "<>", "title": "<>", "description": "<>"}
def create_category(json_request):
    repo = entities.get_repo()
    request = json.loads(json_request)
    try:
        user_id = request['user_id']
        title = request['title']
        description = request['description']
    except KeyError:
        abort(400, message='user data is not found. must be specified "user_id", "title" and "description".')
    result = repo.create_category(user_id, title, description)
    return json.dumps(result)


@app.route("/get_category", methods=['POST'])  # {"user_id": "<>", "category_id": "<>"} !!!!!CHANGE
def category(json_request):
    repo = entities.get_repo()
    request = json.loads(json_request)
    try:
        user_id = request['user_id']
        category_id = request['category_id']
    except KeyError:
        abort(400, message='must be specified "user_id" and "category_id".')

    try:
        user = repo.USERS[user_id]
    except KeyError:
        abort(400, message='no user with such id.')

    data = user.get_category_by_id(category_id)
    return json.dumps(data)


@app.route("/update_category", methods=['POST'])  # {"user_id": "<>", "category_id": "<>", "title"/"description"}
def update_category(json_request):
    repository = entities.get_repo()
    request = json.loads(json_request)
    try:
        user_id = request['user_id']
        category_id = request['category_id']
    except KeyError:
        abort(400, message='must be specified "user_id" and "category_id".')
    title = request.get('title')
    description = request.get('description')
    # if request.form.get('from_category_page'):
    #     return render_template("update_category.html", data=json.dumps({"category_id": category_id,
    #                                                                     "title": title,
    #                                                                     "description": description}))
    result = repository.update_category(user_id, category_id, title, description)
    return json.dumps(result)
    # except Exception as e:
    #     return render_template("update_category.html", data=json.dumps({"category_id": category_id,
    #                                                                     "title": title,
    #                                                                     "description": description,
    #                                                                     "exeption": True,
    #                                                                     "exep": str(e)}))


@app.route("/delete_category", methods=['DELETE'])  # {"user_id": "<>", "category_id": "<>"}
def delete_category(json_request):
    repo = entities.get_repo()
    request = json.loads(json_request)
    try:
        user_id = request['user_id']
        category_id = request['category_id']
    except KeyError:
        abort(400, message='must be specified "user_id" and "category_id".')
    result = repo.delete_category(user_id, category_id)
    return json.dumps(result)


@app.route("/get_cost", methods=['POST'])  # {"user_id": "<>", "category_id": "<>", "cost_id": "<>"}
def cost(json_request):
    repo = entities.get_repo()
    request = json.loads(json_request)
    try:
        user_id = request['user_id']
        category_id = request['category_id']
        cost_id = request['cost_id']
    except KeyError:
        abort(400, message='must be specified "user_id", "category_id" and "cost_id".')

    result = repo.get_cost(user_id, category_id, cost_id)
    return json.dumps(result)


@app.route("/get_all_costs")  # {"user_id": "<>"}
def get_all_costs(json_request):
    repo = entities.get_repo()
    request = json.loads(json_request)
    try:
        user_id = request['user_id']
    except KeyError:
        abort(400, message='must be specified "user_id".')

    all_costs = repo.get_all_costs(user_id)
    return json.dumps(all_costs)


@app.route("/delete_cost", methods=['DELETE'])  # {"user_id": "<>", "category_id": "<>", "cost_id": "<>"}
def delete_cost(json_request):
    repo = entities.get_repo()
    request = json.loads(json_request)
    try:
        user_id = request['user_id']
        category_id = request['category_id']
        cost_id = request['cost_id']
    except KeyError:
        abort(400, message='must be specified "user_id", "category_id" and "cost_id".')

    result = repo.delete_cost(user_id, category_id, cost_id)
    return json.dumps(result)


@app.route("/update_cost", methods=['POST'])  # {"user_id": "<>", "category_id": "<>", "cost_id": "<>",
# "money"/"description"}
def update_cost():
    money = request.form.get('money')
    description = request.form.get('description')
    try:
        user_id = request['user_id']
        category_id = request['category_id']
        cost_id = request['cost_id']
    except KeyError:
        abort(400, message='must be specified "user_id", "category_id" and "cost_id".')

    # if request.form.get('from_cost_page'):
    #     return render_template("update_cost.html", data=json.dumps({"cost_id": cost_id,
    #                                                                 "money": money,
    #                                                                 "description": description}))
    repository = entities.get_repo()
    result = repository.update_cost(session["current_user"], cost_id, money, description)
    print("cost_id " + cost_id)
    print("money " + money)
    print("description " + description)
    return json.dumps(result)


@app.route("/create_cost", methods=['POST'])  # {"user_id": "<>", "category_id": "<>", "description": "<>", "money":
# "<>"}
def create_cost():
    # if request.form.get('from_category_page'):
    #     return render_template("create_cost.html", data=json.dumps({'category_id': request.form.get('category_id')}))
    try:
        user_id = request['user_id']
        category_id = request['category_id']
        description = request['description']
        money = request['money']
    except KeyError:
        abort(400, message='must be specified "user_id", "category_id", "description" and "money".')

    repository = entities.get_repo()
    result = repository.create_cost(user_id, category_id, description, money)
    return json.dumps(result)
