class User():
    def __init__(self, nickname, id):
        self.nickname = nickname
        self.id = id
        self.points = 1
    def add_points(self, points):
        self.points += points