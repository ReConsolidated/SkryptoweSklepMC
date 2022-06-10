from abc import abstractmethod, ABC


class ShopItem(ABC):
    @abstractmethod
    def get_price_key(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

