import os

import psycopg2
from psycopg2 import OperationalError

from ShopItems.ShopItem import ShopItem
from passw import get_password


class DatabaseConnector:
    def __init__(self):
        self._conn = None

    def _connect(self):
        self._conn = psycopg2.connect(
            host="grypciocraft.pl",
            database="hibernate_db",
            user="postgres",
            password=get_password())

    @property
    def conn(self):
        if self._conn is not None:
            try:
                self._conn.isolation_level
            except OperationalError:
                self._connect()
            return self._conn
        self._connect()
        return self._conn

    def close(self):
        if self._conn is not None:
            self._conn.close()


def add_item(name, time, email, shop_item):
    dc = DatabaseConnector()

    cur = dc.conn.cursor()
    cur.execute("""
    INSERT INTO itemshop_data (player_name, shop_item_name, timestamp, 
    email, used) VALUES ('%s', '%s', %s, '%s', false);""", (name, shop_item, time, email))
    dc.conn.commit()
    dc.close()
