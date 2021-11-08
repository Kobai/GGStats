import pandas as pd
import requests
import io
from utils.const import CHARACTER_NAMES, FLOORS


def get_data():
	def get_csv_data(url):
		csv_string = requests.get(url).text
		df = pd.read_csv(io.StringIO(csv_string), index_col=None)
		return df

	commits_req = requests.get('https://api.github.com/gists/3c6a1d310025803d5ccdc2786e60ede8/commits')
	commits = commits_req.json()
	commit_urls = [commit['url'] for commit in commits][:1]
	csv_urls = [requests.get(url).json()['files']['GGST_replays.csv']['raw_url'] for url in commit_urls]
	df = pd.concat([get_csv_data(url) for url in csv_urls])
	df.to_csv('data/matches.csv', index=False)
	return df


def clean_data(df):
	code_to_name = {k:v for k,v in enumerate(CHARACTER_NAMES)}
	char_cols = ['playerACharCode', 'playerBCharCode', 'winnerCharCode', 'loserCharCode']
	char_cols_map = {col:code_to_name for col in char_cols}
	df = df.replace(char_cols_map)
	df = df.rename(columns={'playerACharCode':'playerAChar', 'playerBCharCode':'playerBChar', 'winnerCharCode':'winnerChar', 'loserCharCode':'loserChar'})
	df = df.drop('winner', axis=1)
	return df
	

def build_win_rate_table(df):
	df = clean_data(df)
	def win_rates_by_floor(df,floor):
		floor_win_rate = {}
		floor_win_confidence = {}
		floor_df = df[df['floor']==floor]
		for char in CHARACTER_NAMES:
			char_win = len(floor_df[floor_df['winnerChar'] == char])
			char_loss = len(floor_df[floor_df['loserChar'] == char])
			if char_win+char_loss == 0:
				floor_win_rate[char] = 0
				floor_win_confidence[char] = 0
			else:
				win_rate = char_win/(char_win+char_loss)
				floor_win_rate[char] = win_rate
				floor_win_confidence[char] = 2.58*(win_rate*(1-win_rate) / (char_win+char_loss))**(1/2)
		floor_win_rate = pd.DataFrame.from_dict(floor_win_rate, orient='index', columns=[f'win_rate_{floor}'])
		floor_win_confidence = pd.DataFrame.from_dict(floor_win_confidence, orient='index', columns=[f'win_confidence_{floor}'])
		return pd.concat([floor_win_rate, floor_win_confidence], axis=1)

	all_win_rates = pd.concat([win_rates_by_floor(df,i) for i in FLOORS], axis=1).rename_axis('char_name').reset_index()
	all_win_rates.to_csv('data/win_rates.csv',index=False)


def build_play_rate_table(df):
	df = clean_data(df)
	def play_rates_by_floor(df,floor):
		floor_play_rate = {}
		floor_df = df[df['floor']==floor]
		for char in CHARACTER_NAMES:
			char_played = len(floor_df[floor_df['playerAChar'] == char]) + len(floor_df[floor_df['playerBChar'] == char])
			total_played = 2*len(floor_df)
			if char_played == 0:
				floor_play_rate[char] = 0
			else:
				floor_play_rate[char] = char_played/total_played
		floor_play_rate = pd.DataFrame.from_dict(floor_play_rate, orient='index', columns=[f'play_rate_{floor}'])
		return floor_play_rate

	all_play_rates = pd.concat([play_rates_by_floor(df,i) for i in FLOORS], axis=1).rename_axis('char_name').reset_index()
	all_play_rates.to_csv('data/play_rates.csv',index=False)


def build_match_up_tables(df):
	df = clean_data(df)
	def match_ups_by_floor(df,floor):
		match_up_table = []
		floor_df = df[df['floor']==floor]
		for char1 in CHARACTER_NAMES:
			match_up_row = []
			for char2 in CHARACTER_NAMES:
				char1_wins = len(floor_df[(floor_df['winnerChar']==char1) & (floor_df['loserChar']==char2)])
				char1_losses = len(floor_df[(floor_df['winnerChar']==char2) & (floor_df['loserChar']==char1)])
				if char1_wins+char1_losses == 0:
					match_up_row.append(0)
				else:
					match_up_row.append(char1_wins/(char1_wins+char1_losses))
			match_up_table.append(match_up_row)
		match_up_table = pd.DataFrame(match_up_table, columns=CHARACTER_NAMES, index=CHARACTER_NAMES).rename_axis('char_name').reset_index()
		return match_up_table

	for floor in FLOORS:
		floor_match_ups = match_ups_by_floor(df, floor)
		floor_match_ups.to_csv(f'data/match_ups_{floor}.csv',index=False)


def update_data():
	print('getting data')
	df = get_data()
	print('win rate')
	build_win_rate_table(df)
	print('play rate')
	build_play_rate_table(df)
	print('matchups')
	build_match_up_tables(df)


# df = pd.read_csv('../data/matches.csv')
# print(build_match_up_tables(df))