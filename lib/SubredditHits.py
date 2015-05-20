#!/usr/bin/python
import praw
from operator import attrgetter
import datetime
import time

def getHits(r, subreddit_name, score_threshold=100):
    subreddit = r.get_subreddit(subreddit_name)
    numHits = 1
    hitSubs = []
    todaysDate = datetime.date.today()
    now = time.time()
    nowDate = datetime.datetime.fromtimestamp(now)
    
    topScore = 0
    

    for sub in subreddit.get_hot(limit=300): 
        if (sub.score > topScore):
            topScore = sub.score
        postedDate = datetime.datetime.fromtimestamp(sub.created_utc)
        delta = nowDate - postedDate
        if (delta.days == 0):
            hitSubs.append(sub)
    score_threshold = int(topScore * 0.1)
    recordedSubs = []
    for dayOldSub in hitSubs:
        if (dayOldSub.score > score_threshold):
            recordedSubs.append(dayOldSub)

    html = "<h3>/r/" + subreddit_name + " hits of the day. (Greater than "+str(score_threshold)+" karma)</h3><ol>"

    recordedSubs = sorted(recordedSubs, key=attrgetter('score'), reverse=True)
    for sub in recordedSubs:
        nsfw = ""
        if (sub.over_18):
            nsfw = "(NSFW)"
        html += "<li><b>[" + str(sub.score) + "] </b>" + nsfw + " <a href=\"" + sub.short_link + "\">[Comments]</a> | <a href=\"" + sub.url + "\">" + sub.title + "</a></li>\n"
    html +="</ol><br>"
    if len(hitSubs) == 0:
        return ""
    return html
