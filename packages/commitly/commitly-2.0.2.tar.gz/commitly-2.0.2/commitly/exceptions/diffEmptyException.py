

class DiffEmptyException(Exception):
    def __init__(self,):
        self.message = "aucun changement detecte, aucun message de commit peut etre genere"
        super().__init__(self.message)