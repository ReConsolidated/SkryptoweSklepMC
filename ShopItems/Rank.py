from ShopItems.ShopItem import ShopItem


class Rank(ShopItem):

    def __init__(self, name, key):
        self.price_key = key
        self.name = name

    def get_name(self):
        return self.name

    def get_price_key(self):
        return self.price_key
