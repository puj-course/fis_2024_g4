import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

# Agregar la ruta de la carpeta 'main' al sys.path para poder importar el archivo
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'main'))

from calculadora import *
from moves import get_move
import random
from math import sqrt
from pokemon import Pokemon
from bd import *

class TestPokemonBattle(unittest.TestCase):
    
    def test_pokemon_stats(self):
        # Verifica que las estadísticas del Pokémon sean correctas
        pokemon_y = Pokemon("bulbasaur")
        stats = pokemon_y.stats()
        
        self.assertEqual(stats["HP"], 45)
        self.assertEqual(stats["ATK"], 49)
        self.assertEqual(stats["DEF"], 49)
        self.assertEqual(stats["SPA"], 65)
        self.assertEqual(stats["SPD"], 65)
        self.assertEqual(stats["SPE"], 45)
    
    def test_mostrar_movimientos(self):
        # Verifica que los movimientos sean correctamente mostrados
        pokemon_y = Pokemon("bulbasaur")
        moves = pokemon_y.stats()["MOVES"]
        
        self.assertIn("bodyslam", moves)
        self.assertIn("amnesia", moves)
        self.assertIn("attract", moves)
    
    @patch("random.randint", return_value=100)
    @patch("builtins.input", side_effect=["bulbasaur", 6, "bodyslam", "charmander"])
    def test_stab_bonus(self, mock_input, mock_randint):
        pokemon_y = Pokemon("bulbasaur")  
        move = 6
        pokemon_z = Pokemon("meowth")
        
        modifier_value = modifier(move, pokemon_y, pokemon_z)
        self.assertEqual(modifier_value, 1.2)  
    
    @patch("random.randint", return_value=100)
    @patch("builtins.input", side_effect=["bulbasaur", 5, "bodyslam", "meowth"])
    def test_no_stab_bonus(self, mock_input, mock_randint):
        pokemon_y = Pokemon("bulbasaur") 
        move = 5
        pokemon_z = Pokemon("meowth")
        
        modifier_value = modifier(move, pokemon_y, pokemon_z)
        self.assertEqual(modifier_value, 1) 

    @patch("random.randint", return_value=100)
    @patch("builtins.input", side_effect=["bulbasaur", 6, "bulletseed", "squirtle"])
    def test_super_efective_bonus_and_stab(self, mock_input, mock_randint):
        pokemon_y = Pokemon("bulbasaur")  
        move = 6
        pokemon_z = Pokemon("squirtle")
        
        modifier_value = modifier(move, pokemon_y, pokemon_z)
        self.assertEqual(modifier_value, 2.4)
        
    @patch("random.randint", return_value=100)
    @patch("builtins.input", side_effect=["bulbasaur", 6, "bulletseed", "charmander"])
    def test_not_very_efective_and_stab(self, mock_input, mock_randint):
        pokemon_y = Pokemon("bulbasaur")  
        move = 6
        pokemon_z = Pokemon("charmander")
        
        modifier_value = modifier(move, pokemon_y, pokemon_z)
        self.assertEqual(modifier_value, 0.6)
        
    @patch("random.randint", return_value=100)
    @patch("builtins.input", side_effect=["charmander", 0, "acrobatics", "bulbasaur"])
    def test_super_efective(self, mock_input, mock_randint):
        pokemon_y = Pokemon("charmander")  
        move = 0
        pokemon_z = Pokemon("bulbasaur")
        
        modifier_value = modifier(move, pokemon_y, pokemon_z)
        self.assertEqual(modifier_value, 2.0)

    @patch("random.randint", return_value=100)
    @patch("builtins.input", side_effect=["charmander", 0, "acrobatics", "geodude"])
    def test_bot_very_efective(self, mock_input, mock_randint):
        pokemon_y = Pokemon("charmander")  
        move = 0
        pokemon_z = Pokemon("geodude")
        
        modifier_value = modifier(move, pokemon_y, pokemon_z)
        self.assertEqual(modifier_value, 0.5)
        
    @patch('random.randint', return_value=95)
    def test_dano_special_attack(self, mock_randint):
        y = Pokemon('charmander')
        z = Pokemon('charmander')
        move = 2 #aircutter
        result = dano(move, y, z)
        expected_damage = int(((((((2 * lvl) / 5) + 2) * get_move(mostrar_movimientos(y)[move])[1] * (stat(y)[1] / stat(z)[4])) / 50) + 2) * modifier(move, y, z))
        self.assertEqual(result, expected_damage)

    @patch('random.randint', return_value=95)
    def test_dano_physical_attack(self, mock_randint):
        y = Pokemon('bulbasaur')
        z = Pokemon('charmander')
        move = 5 #bodyslam
        result = dano(move, y, z)
        expected_damage = int(((((((2 * lvl) / 5) + 2) * get_move(mostrar_movimientos(y)[move])[1] * (stat(y)[1] / stat(z)[2])) / 50) + 2) * modifier(move, y, z))
        self.assertEqual(result, expected_damage)

    @patch('random.randint', return_value=95)
    def test_vida_restanter(self, mock_randint):
        y = Pokemon('bulbasaur')
        z = Pokemon('charmander')
        move = 5 #bodyslam
        roll = dano(move, y, z)
        result=vida(roll,z)
        self.assertEqual(result, 131-40)

    

if __name__ == "__main__":
    unittest.main()
