class User:
    ID = 1
    CATEG_ID = 1
    CATEGORIES = {}

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.id = self.ID
        self.ID += 1

    def createCategory(self, title, description):
        self.CATEGORIES[self.CATEG_ID] = Category(title, description)


class Category:
    def __init__(self, title, description):
        self.title = title
        self.description = description
