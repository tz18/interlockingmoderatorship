import praw
import csv

r = praw.Reddit(user_agent = 'joke-away scrapin subscriber numbers like deimorz said to')
csvfile = open("C:\Users\Theseus\Documents\moderatorproject\subscribers.csv", 'wb')
writer = csv.writer(csvfile, dialect='excel')

content = r.get_content('http://www.reddit.com/subreddits', limit=None)
for subreddit in content:
	writer.writerow(["/r/"+subreddit.display_name,subreddit.subscribers])
	print "/r/"+subreddit.display_name," ",subreddit.subscribers

