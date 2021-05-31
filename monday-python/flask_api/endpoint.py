import json, urllib.request
import flask

CONTACTS_DATA = "contacts.json"

app = flask.Flask(__name__)

@app.route("/")
def root():
    return "Hello, world!"

@app.route("/add", methods=["GET", "POST"])
def add():
    name = flask.request.args.get("name", None)
    if name is None:
        return "", 400

    age = flask.request.args.get("age", None)
    if age is None:
        age = ask_age(name)

    gender = flask.request.args.get("gender", None)
    if gender is None:
        gender = ask_gender(name)

    user = {
        "name": name,
        "age": age,
        "gender": gender,
    }
    contacts.append(user)
    save_data()
    return "", 200

@app.route("/all")
def all():
    return flask.jsonify(contacts)

@app.route("/details")
def details():
    name = flask.request.args.get("name", None)
    if name is None:
        return "", 400

    for user in contacts:
        if user["name"] == name:
            return flask.render_template("person.html", **user)
    return "", 400

def save_data():
    with open(CONTACTS_DATA, "w") as f:
        json.dump(contacts, f)

def ask_age(name):
    url = f"https://api.agify.io?name={name}"
    resp = urllib.request.urlopen(url)
    json_data = json.loads(resp.read().decode())
    return json_data["age"]

def ask_gender(name):
    url = f"https://api.genderize.io?name={name}"
    resp = urllib.request.urlopen(url)
    json_data = json.loads(resp.read().decode())
    return json_data["gender"]

@app.route("/developer")
def contacts():
    return "rodrigo@mathspp.com"

@app.route("/inspect")
def inspect():
    json_data = {
        "/": {
            "description": "Root route that says hello, world!",
        },
        "add": {
            "description": "Adds a contact.",
        },
        "all": {
            "description": "List all contacts.",
        },
        "details": {
            "description": "Returns the details of a user.",
        },
        "developer": {
            "description": "Show basic info about the developer.",
        },
        "inspect": {
            "description": "List information about this application.",
        }
    }
    return flask.jsonify(json_data)

with open(CONTACTS_DATA, "r") as f:
    contacts = json.load(f)
app.run(debug=True)
