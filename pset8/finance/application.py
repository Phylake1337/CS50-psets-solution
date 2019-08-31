import os
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    symbols = []
    shares = []
    lookupDict = []
    id = session['user_id']
    rows = db.execute("SELECT * FROM history WHERE id=:id", id = id)
    cash = db.execute("SELECT cash FROM users WHERE id=:id", id = id)[0]['cash']
    for row in rows:
        symbols.append(row['symbol'])
        shares.append(row['shares'])

    for symbol in symbols:
        lookupDict.append(lookup(symbol))

    TotStockCash = cash
    for i in range(len(shares)):
        TotStockCash += lookupDict[i]['price'] * shares[i]

    return render_template("index.html", symbols = symbols, shares = shares, lookupDict = lookupDict, l = len(symbols), cash = usd(cash),TotStockCash = usd(TotStockCash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get('symbol')
        shares = request.form.get('shares')

        if lookup(symbol) == None:
            return apology("Symbol isn't valid")

        if not shares:
            return apology("Provide shares number!")

        if int(shares) < 0:
            return apology("Shares must be postive number")

        stocksCost = int(shares) * lookup(symbol)['price']
        cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])[0]['cash']
        symbols = db.execute("SELECT symbol FROM history WHERE id=:id",id=session["user_id"])

        for i in range(len(symbols)):
            symbols[i] = symbols[i]['symbol']

        if cash > stocksCost:
            if symbol not in symbols:
                db.execute("INSERT INTO history (id, symbol, price, shares, time) VALUES (:id, :symbol, :price, :shares, :time)"
                , id = session['user_id'], symbol = symbol, price = lookup(symbol)['price'], shares = shares, time = datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            else:
                ownedShares = db.execute("SELECT shares FROM history WHERE id=:id AND symbol=:symbol", id=session["user_id"], symbol = symbol)[0]['shares']
                db.execute("UPDATE history SET shares=:shares WHERE id=:id AND symbol=:symbol", id=session['user_id'], shares = ownedShares + int(shares), symbol = symbol)

            db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash = cash - stocksCost, id = session['user_id'])
        else:
            return apology("You're poor")

    return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/")

        # Redirect user to home page

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("Enter valid symbol!")
        else:
            return render_template("quoted.html", name = quote["name"], price = usd(quote['price']), symbol = quote['symbol'])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 403)
        if not password:
            return apology("must provide password", 403)
        if not confirmation:
            return apology("must provide password confirmation", 403)

        usernames = []
        for i in range(len(db.execute("SELECT username FROM users"))):
            usernames.append(db.execute("SELECT username FROM users")[i]['username'])
        if username in usernames:
            return apology("Username is already exists", 403)

        if password != confirmation:
            return apology("check password confirmation", 403)

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username = username, password = generate_password_hash(password))

        return redirect("/")




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    symbols = db.execute("SELECT symbol FROM history WHERE id=:id", id = session['user_id'])
    for i in range (len(symbols)):
        symbols[i] = symbols[i]['symbol']
    symbols = list(set(symbols))

    if request.method == "GET":
        return render_template("sell.html", symbols = symbols, l = len(symbols))
    else:
        soldShares = request.form.get("shares")
        symbol = request.form.get("symbol")
        lookupDict = lookup(symbol)
        ownedShares = db.execute("SELECT shares FROM history WHERE id=:id AND symbol=:symbol"
        , id = session['user_id'], symbol = symbol)[0]['shares']
        ownedCash = db.execute("SELECT cash FROM users WHERE id=:id", id = session["user_id"])[0]['cash']
        if not soldShares:
            return apology("Enter the number of shares")
        if int(soldShares) < 0 or int(soldShares) > ownedShares:
            return apology("Enter a proper shares number")
        db.execute("UPDATE history SET shares=:shares WHERE id=:id AND symbol=:symbol"
        , shares = ownedShares-int(soldShares), id = session['user_id'], symbol = symbol)
        db.execute("UPDATE users SET cash=:cash WHERE id=:id"
        , cash = ownedCash + int(soldShares) * lookupDict['price'], id = session['user_id'])
        return redirect("/")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
