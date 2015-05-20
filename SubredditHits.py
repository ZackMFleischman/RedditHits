#!/usr/bin/python
import praw
from operator import attrgetter
import datetime

def getHits(r, subreddit_name, score_threshold=100):
    html = "<h3>/r/" + subreddit_name + " hits of the day. (Greater than "+str(score_threshold)+" karma)</h3><ol>"
    subreddit = r.get_subreddit(subreddit_name)
    numHits = 1
    hitSubs = []
    todaysDate = datetime.date.today()
    for sub in subreddit.get_hot(limit=300):
        if (sub.score > score_threshold and todaysDate == datetime.date.fromtimestamp(sub.created_utc)):
            hitSubs.append(sub)

    hitSubs = sorted(hitSubs, key=attrgetter('score'), reverse=True)
    for sub in hitSubs:
        html += "<li><b>[" + str(sub.score) + "] </b> | <a href=\"" + sub.short_link + "\">[Comments]</a> | <a href=\"" + sub.url + "\">" + sub.title + "</a></li>\n"
    html +="</ol><br>"
    if len(hitSubs) == 0:
        return ""
    return html
