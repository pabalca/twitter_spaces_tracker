from flask import abort, flash, redirect, render_template, session, url_for, request
from sqlalchemy import or_, and_

from twitter_spaces_tracker import app
from twitter_spaces_tracker.models import Account, Space, db
from twitter_spaces_tracker.forms import SearchForm, AccountForm


@app.route("/", methods=["GET"])
def index():
    spaces = (
        Space.query.order_by(Space.scheduled_at.desc())
        .filter(Space.state != "scheduled")
        .limit(20)
        .all()
    )
    return render_template("spaces.html", spaces=spaces, username=None)


@app.route("/accounts", methods=["GET", "POST"])
def accounts():
    form = AccountForm()
    accounts = Account.query.order_by(Account.created_at.desc())

    if form.validate_on_submit():
        username = form.username.data.lower()
        a = Account(username=username)
        db.session.add(a)
        db.session.commit()
        flash(f"Your account <{username} is saved.")
        return redirect(url_for("index"))
    accounts = accounts.all()

    return render_template("index.html", accounts=accounts, form=form)


@app.route("/spaces/<account_id>", methods=["GET"])
def spaces(account_id):
    account = Account.query.filter_by(id=account_id).first()
    return render_template(
        "spaces.html", spaces=account.spaces, username=account.username
    )

