# hex-note

## The Present:

Hex Note is a Twitter chat bot that speaks in Hex encoded riddles.
The bot first retrieves OAuth credentials from Twitter, then moves into a couple processing loops which determine what to say.
Using REST calls to the Twitter API, the bot can find trends, users, mentions, and post tweets.

## The Future:

With the way software is heading, I'm going to containerize hex-note to make spinning up deployments a bit easier.
I also plan to expand the bot by adding more 'thoughtful' speech patterns. 

##To Run:
 
Copy configtemplate.cfg and drop it in the same directory has the program.
Rename it **app.cfg** and fill out the values with your relevant information.
The logging level can be set from the command line, use -h for help.
Running Hex Note without the Optimize **(-O)** flag will prevent it from tweeting. Useful for debugging.
Run with: `python -O hexnote.py`
