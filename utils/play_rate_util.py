import pandas as pd

def get_floor_play_rates(floor):
	df = pd.read_csv('data/play_rates.csv')
	return df[['char_name',f'play_rate_{floor}']].sort_values(by=[f'play_rate_{floor}'])