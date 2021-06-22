import praw
from datetime import date, timedelta
import random
import decimal
import time
import os

reddit = praw.Reddit(client_id = os.getenv('client_id'),
                    client_secret = os.getenv('client_secret'),
                    username = os.getenv('username'),
                    password = os.getenv('password'),
                    user_agent = os.getenv('user_agent'))

subreddit = reddit.subreddit('all+popular')

keyphrase = 'u/repostsleuthbot'

def message():
    dt = str(date.today() - timedelta(2))
    randnum = str("{:,}".format(random.randrange(100000000, 500000000)))
    randnum2 = str("{:,}".format(random.randrange(100000000, 500000000)))
    randtime = str(decimal.Decimal(random.randrange(1000000))/100000) + 's'
    randpercent = str(random.randrange(90, 99))
    randpercent2 = str(random.randrange(10, 99))

    return 'Looks like a repost. I\'ve seen this image 1 time.\n\nFirst seen [Here](https://www.youtube.com/watch?v=dQw4w9WgXcQ) on ' + dt + ' ' + randpercent + '.' + randpercent2 + '%' + ' match.\n\n**Searched Images**: ' + randnum + ' | **Indexed Posts**: ' + randnum2 + ' | **Search Time**: ' + randtime + '\n\n*Feedback? Hate? Visit [r/repostsleuthbot](https://www.youtube.com/watch?v=6n3pFFPSlW4) - I\'m not perfect, but you can help. Report [ [False Positive](https://www.youtube.com/watch?v=d1YBv2mWll0) ]*'


if not os.path.isfile('replied_users.txt'):
    replied_users = []
else:
    with open('replied_users.txt', 'r') as f:
        replied_users = f.read()
        replied_users = replied_users.split('\n')
        replied_users = list(filter(None, replied_users))

for comment in subreddit.stream.comments():
    if comment.body == keyphrase and len(comment.replies) == 0 and comment.author.name not in replied_users:
        try:      
            comment.reply(message())
            replied_users.append(comment.author.name)
            with open('replied_users.txt', 'w') as f:
                f.write(comment.author.name + '\n')
            print('replied to', comment.author.name, 'in r/', comment.subreddit)
        except:
            print('couldn\'t reply in r/', str(comment.subreddit))
            time.sleep(600)