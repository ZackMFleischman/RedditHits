#!/usr/bin/python
import praw
from operator import attrgetter
import datetime
import time

def getHits(r, subreddit_name, score_threshold=100):
    html = "<h3>/r/" + subreddit_name + " hits of the day. (Greater than "+str(score_threshold)+" karma)</h3><ol>"
    subreddit = r.get_subreddit(subreddit_name)
    numHits = 1
    hitSubs = []
    todaysDate = datetime.date.today()
    now = time.time()
    nowDate = datetime.datetime.fromtimestamp(now)
    for sub in subreddit.get_hot(limit=300):
        postedDate = datetime.datetime.fromtimestamp(sub.created_utc)
        delta = nowDate - postedDate
        if (sub.score > score_threshold and delta.days == 0):
            hitSubs.append(sub)

    hitSubs = sorted(hitSubs, key=attrgetter('score'), reverse=True)
    for sub in hitSubs:
        html += "<li><b>[" + str(sub.score) + "] </b> | <a href=\"" + sub.short_link + "\">[Comments]</a> | <a href=\"" + sub.url + "\">" + sub.title + "</a></li>\n"
    html +="</ol><br>"
    if len(hitSubs) == 0:
        return ""
    return html
