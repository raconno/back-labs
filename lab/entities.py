from datetime import datetime
from lab import exceptions


class Repository:
    USERS = []

    def create_user(self, username, email, password):
        for user in self.USERS:
            if user.username == username:
                raise Exception("Please choose another username")
            if user.email == email:
                raise exceptions.ExistingEmail()

        new_user = User(username, email, password)
        self.USERS.append(new_user)
        return new_user

    def log_in_by_email(self, email, password):
        for user in self.USERS:
            if user.email == email or user.password == password:
                return user
        raise Exception

    def log_in_by_username(self, username, password):
        for user in self.USERS:
            if user.username == username or user.password == password:
                return user
        raise Exception


class User:
    ID = 1
    CATEGORY_ID = 1
    COST_ID = 1

    CATEGORIES = {}
    COSTS = {}

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.id = self.ID
        self.ID += 1

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
