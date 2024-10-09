from pymongo import MongoClient
from bd import *

# Clase Pokemon
class Pokemon:
    def __init__(self, name):
        self.name = name.lower()
        self.data = self.obtener_stats()

    def obtener_stats(self):
        pokemon = pokemon_collection.find_one({"Name": self.name})  # Buscar por nombre
        if pokemon:
            return {
                'Name': pokemon['Name'],
                'Type': pokemon['Type'],
                'HP': pokemon['HP'],
                'ATK': pokemon['ATK'],
                'DEF': pokemon['DEF'],
                'SPA': pokemon['SPA'],
                'SPD': pokemon['SPD'],
                'SPE': pokemon['SPE'],
                'MOVES': pokemon['MOVES'].split(";")  # Dividir los movimientos por ';'
            }
        return None

    def stats(self):
        return self.data