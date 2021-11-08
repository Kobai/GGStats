import pandas as pd

def get_floor_match_ups(floor):
	df = pd.read_csv(f'data/match_ups_{floor}.csv')
	return df