# hex-note
The Present:
Hex Note is a Twitter chat bot that speaks Hex.
The bot first retrieves OAuth credentials from Twitter, then moves into a couple processing loops which determine what to say.
Using REST calls to the Twitter API, the bot can find trends, users, mentions, and post tweets.

The Future:
Now that I have a better threading structing in place, I'd like to revisit running Hex Note as a Service.
I also plan to expand the bot by adding more 'thoughtful' speech patterns. 

To Run:
Copy configtemplate.cfg and drop it in the same directory has the program.
Rename it 'app.cfg' and fill out the values with your relevant information.
The logging level can be set from the command line, use -h for help.
Running Hex Note without the Optimize (-O) flag will prevent it from tweeting. Useful for debugging.
Run with: python -O hexnote.py
