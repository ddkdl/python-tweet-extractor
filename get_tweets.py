import csv, codecs, got, os, sys, time
from datetime import datetime, timedelta, date

# funtion for generating a date range list given a year
def getDateInterval(year):
	start = date(int(year), 1, 1).strftime('%Y-%m-%d')
	end = date(int(year), 12, 31).strftime('%Y-%m-%d')

	return (start, end)


def main(argv):
	if len(argv) == 0 or len(argv) > 3:
		print('Incorrect Syntax')
		return

	if len(argv) == 1 and argv[0] == '-h':
		print('get_tweets [query string] [query state] [query year]')
		return

	search_query = argv[0]
	search_location = argv[1]
	search_year = argv[2]

	# defining the paths to location and output files
	location_file_path = 'coordinates/'+search_location+'.csv'

	output_file_path = search_query.title()+'_'+search_year+'_'+search_location+'.csv'

	# opening the files
	geo_locations = open(location_file_path, 'r')
	output_file = codecs.open(output_file_path, 'a', 'utf-8')

	# creating a parser for the csv file
	reader = csv.DictReader(geo_locations)

	# if the output file is empty
	if os.stat(output_file_path).st_size == 0:
		# write the header
		output_file.write('id\tUsername\tText\tDate\tRetweets\tFavorites\tMentions\tHashtags\tGeo\tPermalink\n')

	dates = getDateInterval(search_year)
	start_date = dates[0]
	end_date = dates[1]

	print(start_date,end_date)
	try:
		print('Searching...\n')
		for row in reader:
			tweetCriteria = got.manager.TweetCriteria().setQuerySearch(search_query).setSince(start_date).setUntil(end_date).setNear(row['Latitude']+','+row['Longitude']).setWithin(row['Radius(in miles)']+'mi')
			tweets = got.manager.TweetManager.getTweets(tweetCriteria)

			if (len(tweets) != 0):
				for t in tweets:
					output_file.write(('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n')%(t.id, t.username, t.text,t.date.strftime("%Y-%m-%d"), t.retweets, t.favorites, t.mentions, t.hashtags, t.geo, t.permalink))
				print ('%d tweets written to file...' % len(tweets))
				output_file.flush()
			else:
				print ('No tweets found...')
			# sleep for 5 seconds
			time.sleep(5)

	except Exception, message:
		print message

	finally:
		geo_locations.close()
		output_file.close()

if __name__ == '__main__':
	main(sys.argv[1:])
