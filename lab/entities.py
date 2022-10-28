from datetime import datetime
from lab import exceptions
from flask import session


repo = None


def get_repo():
    global repo
    if repo is None:
        session.clear()
        repo = Repository()
        user1 = repo.get_user(repo.create_user("11", "11", "11"))
        user2 = repo.get_user(repo.create_user("22", "22", "22"))
        user3 = repo.get_user(repo.create_user("33", "33", "33"))
        user4 = repo.get_user(repo.create_user("44", "44", "44"))
        user5 = repo.get_user(repo.create_user("55", "55", "55"))

        user1.create_category("category1", "for user 1")
        user1.create_category("category2", "for user 1")
        user1.create_category("category3", "for user 1")

        user2.create_category("category1", "for user 2")
        user2.create_category("category2", "for user 2")
        user2.create_category("category3", "for user 2")

        user3.create_category("category1", "for user 3")
        user3.create_category("category2", "for user 3")
        user3.create_category("category3", "for user 3")

        user4.create_category("category1", "for user 4")
        user4.create_category("category2", "for user 4")
        user4.create_category("category3", "for user 4")

        user5.create_category("category1", "for user 5")
        user5.create_category("category2", "for user 5")
        user5.create_category("category3", "for user 5")
    return repo


class Repository:
    USER_ID = 1
    USERS = {}

    def create_user(self, username, email, password):
        for _, user in self.USERS.items():
            if user.username.title() == username:
                raise Exception("Please choose another username. username:") #+ str(user.username) + "; email:" + str(user.email) + "; password:" + str(user.password)+"; cause of username:"+str(username)+"; email:"+str(email)+"; password: "+str(password))
            if user.email.lower() == email:
                # raise exceptions.ExistingEmail() #offer to restore password
                raise Exception("You already have an account with such email.")

        new_user = User(username.title(), email.lower(), password)
        self.USERS[self.USER_ID] = new_user
        self.USER_ID += 1
        return self.USER_ID - 1

    def log_in(self, nick, password):
        for id, user in self.USERS.items():
            if user.email.lower() == nick or user.username.title() == nick:
                if user.password == password:
                    return id
                else:
                    raise Exception("Wrong password!")
        raise Exception("Wrong email or username.")

    def get_user(self, id):
        return self.USERS[id]


class User:
    CATEGORY_ID = 1
    COST_ID = 1

    CATEGORIES = {}
    COSTS = {}

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def create_category(self, title, description):
        self.CATEGORIES[self.CATEGORY_ID] = Category(title, description)
        self.CATEGORY_ID += 1

    def create_cost(self, category_id, money):
        self.COSTS[self.COST_ID] = Cost(category_id, money)
        self.COST_ID += 1

    def get_costs(self):
        return self.COSTS

    def get_costs_in_category(self, category_id):
        return_costs = []
        for cost in self.COSTS:
            if cost.category_id == category_id:
                return_costs.append(cost)
        return return_costs


class Category:
    def __init__(self, title, description):
        self.title = title
        self.description = description


class Cost:
    def __init__(self, category_id, money):
        self.category_id = category_id
        self.creation_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.money = money
