from os import environ
import click
import tweepy

from twitter_spaces_tracker import app
from twitter_spaces_tracker.models import Account, Space, db


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Account=Account, Space=Space)


@app.cli.command()
@click.option("--drop", is_flag=True, help="Create after drop.")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")


@app.cli.command()
def update():

    spaces = Space.query.all()

    api_key = environ.get('TST_API_KEY')
    api_key_secret = environ.get('TST_API_KEY_SECRET')
    access_token = environ.get('TST_ACCESS_TOKEN')
    access_token_secret = environ.get('TST_ACCESS_TOKEN_SECRET')
    bearer_token = environ.get('TST_BEARER_TOKEN')

    if not api_key or not api_key_secret or not access_token or not access_token_secret or not bearer_token:
        click.echo("Missing configuration. Please set up the .env")
        import sys
        sys.exit(0)

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Setup up twitter v2
    client = tweepy.Client(bearer_token=bearer_token)

    accounts = Account.query.all()
    for account in accounts:

        raws = set()
        tweets = api.user_timeline(screen_name=account.username, count=200)

        # filter by spaces using the url
        for tweet in tweets:
            urls = tweet.entities["urls"]
            if urls:
                expanded_url = urls[0]["expanded_url"]
                if expanded_url.startswith("https://twitter.com/i/spaces/"):
                    raws.add(expanded_url)

        # enrich space data
        for raw in raws:
            space = client.get_space(
                raw.split("/")[-1],  # space_id extracted from the url
                space_fields=["title", "participant_count", "started_at", "ended_at", "scheduled_start"],
            )

            # TODO:
            # if state == ended, data is static, if not, update it.


            # add if it does not exist already
            if raw not in [s.url for s in spaces]:
                s = Space(
                    account=account,
                    title=space.data.title,
                    started_at=space.data.started_at,
                    ended_at=space.data.ended_at,
                    scheduled_at=space.data.scheduled_start,
                    participant_count=space.data.participant_count,
                    state=space.data.state,
                    url=raw,
                )
                db.session.add(s)
                click.echo(raw + " added")
            else:
                click.echo(raw + " already exists")

    db.session.commit()
