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


class Category:
    def __init__(self, title, description):
        self.title = title
        self.description = description


class Cost:
    def __init__(self, category_id, money):
        self.category_id = category_id
        self.creation_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.money = money
