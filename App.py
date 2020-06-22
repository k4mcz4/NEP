from flask import Flask, render_template, redirect, session, request
import Authenticate as Auth

app = Flask(__name__)
app.secret_key = "cMonshOwm3S0M3LuVV"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/auth/code")
def authCode():
    code = request.args.get('code')
    state = request.args.get('state')

    print(state)

    if(session["state"] == state):
        message = "The code is {}, this part will be used for catching authentication response code".format(code)
    else:
        message = "oops, something went wrong with your state {}".format(state) 

    return message

@app.route("/auth")
def auth():
    authRequest = Auth.Authenticate("GET")
    session["state"] = authRequest.get_state()
    print(session["state"])
    return redirect(authRequest.get_uri())

if __name__ == "__main__":
    app.run(debug = True)