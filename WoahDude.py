#!/usr/bin/python
import smtplib
import praw
import unicodedata
from pprint import pprint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from operator import attrgetter
import datetime

address="zFleischman@gmail.com"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Woah Dude Hits of the Day"
msg['From'] = address
msg['To'] = address

text = "Woah Dude Hits of the Day:\n"
html =  """\
<html>
    <head></head>
    <body>
    <h3>Woah Dude Hits of the Day</h3><br>
    <ol>
"""

# -----------
user_agent = "WoahDude Aggregator 1.0 by /u/WoahDudeFanatic"
r = praw.Reddit(user_agent=user_agent)

r.login("WoahDudeFanatic", "funny:ears")

subreddit = r.get_subreddit('woahdude')
numHits = 1
hitSubs = []
todaysDate = datetime.date.today()
for sub in subreddit.get_hot(limit=300):
    if (sub.score > 100 and todaysDate == datetime.date.fromtimestamp(sub.created_utc)):
        hitSubs.append(sub)

hitSubs = sorted(hitSubs, key=attrgetter('score'), reverse=True)
for sub in hitSubs:
    text += str(sub.score) + " [ " + sub.short_link + " ]: " + sub.title + "\n"
    html += "<li><b>[" + str(sub.score) + "] </b> | <a href=\"" + sub.short_link + "\">[Comments]</a> | <a href=\"" + sub.url + "\">" + sub.title + "</a> Time Created=" + str(sub.created_utc) +"</li>\n"
    numHits += 1


html += "</ol></body></html>\n"

text = unicodedata.normalize('NFKD', text).encode('ascii','ignore') 
html = unicodedata.normalize('NFKD', html).encode('ascii','ignore')
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
    s.login("zFleischman@gmail.com", "PurpleSheepW4ll")
    s.sendmail(address, address, msg.as_string())
finally:
    s.quit()

print html
print text
