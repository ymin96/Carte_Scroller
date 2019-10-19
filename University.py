class University:
    def __init__(self, title):
        self.title = title
        self.cartes = []

    def addCarte(self, carte):
        self.cartes.append(carte)