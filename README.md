# RedditHits
Script to aggregate the daily top scoring posts for certain subreddits.

## Setup
####Credentials
```
cp cred_template.py cred.py
```
Edit `cred.py` and punch in your email address credentials that will be used to send you your message.


####(Optional) Create a new subreddit digest.
```
cp GetHits_Template.py GetHits_[name].py
```
Edit `GetHits_[name]` to include your email address that you want your message sent to and the subreddits you would like to receive the top hits from.


## Run
```
python GetHits_[name].py
```

