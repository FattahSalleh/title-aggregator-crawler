import os
import datetime
from flask import Flask, render_template
import json
import pytz 

app = Flask(__name__)


@app.route("/")
def index():
    articles = []
    # Define the start date (1st of January 2022) in UTC timezone
    utc = pytz.UTC
    start_date = datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=utc)

    with open("wired_articles.json") as f:
        data = json.load(f)
        for article in data:
            # Convert the article's publication date to a datetime object
            publication_date = datetime.datetime.strptime(
                article["publication_date"], "%Y-%m-%dT%H:%M:%S%z"
            )
            # Check if the article was published on or after the start date
            if publication_date >= start_date:
                articles.append(
                    {
                        "title": article["title"],
                        "url": article["url"],
                        "publication_date": publication_date,
                    }
                )

    # Sort the articles in anti-chronological order (latest article first)
    articles.sort(key=lambda x: x["publication_date"], reverse=True)

    return render_template("index.html", articles=articles)


if __name__ == "__main__":
    # Get the port number from the PORT environment variable provided by Heroku
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
