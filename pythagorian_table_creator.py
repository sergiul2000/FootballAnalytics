from pythagorian_data_analyzer import generate_formula_for_all_teams
import pandas as pd

df = generate_formula_for_all_teams('', 20)
df.to_csv('./converted_files/simple_pythagorian.csv')
