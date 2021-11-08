import requests
import io
import pandas as pd


# commits_req = requests.get('https://api.github.com/gists/3c6a1d310025803d5ccdc2786e60ede8/commits')
# commits = commits_req.json()
# commit_urls = [commit['url'] for commit in commits][:3]

# csv_urls = [requests.get(url).json()['files']['GGST_replays.csv']['raw_url'] for url in commit_urls]

# for i,url in enumerate(csv_urls):
# 	csv_string = requests.get(url).text
# 	df = pd.read_csv(io.StringIO(csv_string), index_col=None)
# 	df.to_csv(f'../test_data/{i}.csv')

# def get_csv_data(url):
# 	csv_string = requests.get(url).text
# 	df = pd.read_csv(io.StringIO(csv_string), index_col=None)
# 	return df
	# df.to_csv(f'../test_data/{i}.csv')

# df = pd.concat([get_csv_data(url) for url in csv_urls])
# df.to_csv('../test_data/raw.csv',index=False)
# df = pd.read_csv(string_to_io(csvs[0]))
# print(df)

# df = pd.concat([pd.read_csv('GGST_replays.csv'), pd.read_csv('GGST_replays.csv')])
# print(df)

# df = pd.read_csv('../data/win_rates.csv')
# print(df[['char_name','win_rate_99']])

df = pd.read_csv('../data/match_ups.csv')
print(df)

