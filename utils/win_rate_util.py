import pandas as pd

def get_floor_win_rates(floor):
	df = pd.read_csv('data/win_rates.csv')
	return df[['char_name',f'win_rate_{floor}']].sort_values(by=[f'win_rate_{floor}'])