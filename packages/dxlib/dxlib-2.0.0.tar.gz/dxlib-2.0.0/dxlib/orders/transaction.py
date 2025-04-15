from uuid import UUID


class Transaction:
    def __init__(self, seller: UUID | str, buyer: UUID | str, price, quantity):
        self.seller = seller
        self.buyer = buyer
        self.price = price
        self.quantity = quantity
