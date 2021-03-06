#!/usr/bin/python
import smtplib
import cred
import praw
import unicodedata
from pprint import pprint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from operator import attrgetter
from src.SubredditHits import getHits
import datetime
import sys
import warnings
import cred

warnings.simplefilter("ignore", ResourceWarning)

sys.dont_write_bytecode = True

def getAllHits(subreddits, toAddress):
    address=toAddress

# Create message container - the correct MIME type is multipart/alternative.
    today = datetime.date.today()
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Reddit Hits of the Day - " + str(today)
    msg['From'] = cred.username()
    msg['To'] = address

    html =  """\
    <html>
        <head></head>
        <body>
    """

# -----------
    user_agent = "WoahDude Aggregator 1.0 by /u/WoahDudeFanatic"
    r = praw.Reddit(user_agent=user_agent)
    r.login("WoahDudeFanatic", "funny:ears")

    progress = 1
    for sub in subreddits:
        print ("Getting /r/" + sub + "...(" + str(progress) + "/" + str(len(subreddits))+")")
        html += getHits(r, sub)
        progress += 1


    html += "</ol></body></html>\n"


    print(html)
    try:
        f = open('/Users/zfleischman/repos/RedditHits/digest.html', 'w+')
        f.write(html)
        f.close()
    except:
        print ("Couldn't open digest.html file")

    text = "plain text"
    try:
        #html = unicodedata.normalize('NFKD', html).encode('ascii','ignore')
        html.encode('ascii')
    except:
        pass
# Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

# Send the message via local SMTP server.
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)

    try:
        s.login(cred.username(), cred.password())
        s.sendmail(address, address, msg.as_string())
    finally:
        s.quit()

    print ("Done!")
