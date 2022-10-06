# Interview Test for KNOREX

I made use of `feedparser` to parse the rss data.
Then, I iterated through the html files and got the text using `beautifulsoup`.

All these data is pushed to a MongoDB instance.
After that, I used the built-in `mongoexport` to export the databse data into JSON data.
