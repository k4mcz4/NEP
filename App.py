import os
import time
import hashlib
import uuid

from datetime import datetime
from datetime import timedelta

from flask import Flask
from flask import render_template
from flask import redirect
from flask import session
from flask import url_for
from flask import request

from flask_login import LoginManager
from flask_login import current_user
from flask_login import UserMixin
from flask_login import login_user

from AuthConfig import *

from esipy import EsiApp
from esipy import EsiClient
from esipy import EsiSecurity
from esipy.exceptions import APIException

from flask_sqlalchemy import SQLAlchemy

# -----------------------------------------------------------------------
# Flask setup
# -----------------------------------------------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "database/sqlite-latest.sqlite")

app = Flask(__name__)
app.secret_key = b'\xdf\x95D\xe7{\x0b\xe1:&\x94G9\xd1\x1f\x94\xed'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=7)

# -----------------------------------------------------------------------
# Flask login manager setup
# -----------------------------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# -----------------------------------------------------------------------
# DB setup
# -----------------------------------------------------------------------
db = SQLAlchemy(app)

# -----------------------------------------------------------------------
# EsiPy setup
# -----------------------------------------------------------------------
esiApp = EsiApp().get_latest_swagger

security = EsiSecurity(
    redirect_uri=REDIRECT_URI,
    client_id=CLIENT_ID,
    secret_key=SECRET,
    headers={'User-Agent': 'Application for tracking Fuel Production'}
)

client = EsiClient(
    retry_requests=True,
    headers={'User-Agent': 'Application for tracking Fuel Production'},
    security=security
)


# -----------------------------------------------------------------------
# Flask Login requirements
# -----------------------------------------------------------------------
@login_manager.user_loader
def load_user(session_id):
    """ Required user loader for Flask-Login """
    user_session = UserSession.query.get(session_id)
    if user_session.verify_login():
        return user_session
    else:
        return None


# -----------------------------------------------------------------------
# DB Models
# -----------------------------------------------------------------------
class UserSession(db.Model, UserMixin):
    __tablename__ = 'UserSession'
    id = db.Column("id", db.String(200), primary_key=True)
    unique_character_id = db.Column("uniqueCharacterID", db.Integer)
    token_id = db.Column("tokenID", db.Integer)
    ip_address = db.Column("ipAddress", db.String(50))

    def get_sso_data(self):
        """ Little "helper" function to get formated data for esipy security
        """
        token = Token.query.filter_by(id=self.token_id).first()

        return {
            'access_token': token.access_token,
            'refresh_token': token.refresh_token,
            'expires_in': (
                    token.expires_at - datetime.utcnow()
            ).total_seconds()
        }

    def update_token(self, token_response):
        """ helper function to update token data from SSO response """
        token = Token.query.get(token_id=self.token_id)
        token.access_token = token_response['access_token']
        token.expires_at = datetime.fromtimestamp(
            time.time() + token_response['expires_in'],
        )
        if 'refresh_token' in token_response:
            token.refresh_token = token_response['refresh_token']

        db.session.merge(token)
        db.session.commit()

    def get_character_id(self):
        character_id = Character.query.filter_by(id=self.unique_character_id).first()
        return character_id.character_id

    def verify_login(self):
        character = Character.query.get(self.unique_character_id)
        return character.is_corporation_authorized()

    def get_corporation_id(self):
        character = Character.query.get(self.unique_character_id)
        return character.corporation_id

    def get_moon_extractions(self):
        op = esiApp.op['get_corporation_corporation_id_mining_extractions'](corporation_id=self.get_corporation_id())
        extractions = client.request(op)

        return extractions


class Character(db.Model, UserMixin):
    __tablename__ = 'Characters'
    id = db.Column("uniqueCharacterID", db.Integer, primary_key=True)
    character_id = db.Column("characterID", db.BigInteger)
    character_name = db.Column("characterName", db.String(50))
    corporation_id = db.Column("corporationID", db.Integer)
    e_tag = db.Column("eTag", db.String(300))

    def is_corporation_authorized(self):
        corporation_id = AccessList.query.filter_by(corporation_id=self.corporation_id).first()

        if corporation_id is None:
            return False
        else:
            return True

    def is_corporation_in_database(self):
        corp_id = Corporation.query.get(self.corporation_id)
        if corp_id is not None:
            False
        else:
            True


class Token(UserMixin, db.Model):
    __tablename__ = 'Tokens'
    id = db.Column("id", db.Integer, primary_key=True)
    access_token = db.Column("accessToken", db.String(4000))
    expires_at = db.Column("expiresAt", db.DateTime)
    token_type = db.Column("tokenType", db.String(30))
    refresh_token = db.Column("refreshToken", db.String(200))


class Corporation(UserMixin, db.Model):
    __tablename__ = 'Corporations'
    id = db.Column("corporationID", db.BigInteger, primary_key=True)
    corporation_name = db.Column("corporationName", db.String(100))

    # alliance_id = db.Column("allianceID", db.BigInteger)


class AccessList(UserMixin, db.Model):
    __tablename__ = 'AccessList'
    id = db.Column("id", db.Integer, primary_key=True)
    corporation_id = db.Column("corporationID", db.BigInteger, nullable=False)


# -----------------------------------------------------------------------
# Login/Authentication routes
# -----------------------------------------------------------------------
@app.route("/auth")
def auth():
    token = hashlib.sha256(os.urandom(1024)).hexdigest()
    session["token"] = token

    session.permanent = True

    return redirect(security.get_auth_uri(state=token, scopes=SCOPE_LIST))


@app.route("/auth/code")
def auth_code():
    code = request.args.get('code')
    token = request.args.get('state')

    if session["token"] == token:

        session["token"] = uuid.uuid4()

        try:
            auth_response = security.auth(code=code)
            esi_token = Token(
                access_token=auth_response['access_token'],
                expires_at=datetime.fromtimestamp(
                    time.time() + auth_response['expires_in']),
                token_type=auth_response['token_type'],
                refresh_token=auth_response['refresh_token']
            )

            db.session.add(esi_token)
            db.session.commit()

            cdata = security.verify()

            character_id = cdata['sub'].split(':')[2]
            op = esiApp.op['get_characters_character_id'](character_id=character_id)
            character = client.request(op)
            character = character.data
            character_data = Character(
                character_id=character_id,
                character_name=character['name'],
                corporation_id=character['corporation_id']
            )

            db.session.add(character_data)
            db.session.commit()

            if character_data.is_corporation_authorized():
                if character_data.is_corporation_in_database():
                    op = esiApp.op['get_corporations_corporation_id'](corporation_id=character['corporation_id'])
                    corporation = client.request(op)
                    corporation = corporation.data

                    corporation_data = Corporation(
                        id=character['corporation_id'],
                        corporation_name=corporation['name']
                    )

                    db.session.add(corporation_data)
                    db.session.commit()

                user_session = UserSession(
                    id=str(session["token"]),
                    unique_character_id=character_data.id,
                    token_id=esi_token.id,
                    ip_address=""
                )

                db.session.add(user_session)
                db.session.commit()

                login_user(user_session)

            else:
                return "Unauthorized"

        except APIException as e:
            return 'Login EVE Online SSO failed: %s' % e, 403

    return redirect(url_for("index"))


# -----------------------------------------------------------------------
# Main routes
# -----------------------------------------------------------------------
@app.route("/")
def index():
    wallet = None

    if current_user.is_authenticated:
        security.update_token(current_user.get_sso_data())

        character_id = current_user.get_character_id()
        op = esiApp.op['get_characters_character_id_wallet'](character_id=character_id)
        wallet = client.request(op)

        extractions = current_user.get_moon_extractions()
        print(str(extractions.data))

    return render_template("index.html")


@app.route("/assets")
def assets():
    if current_user.is_authenticated:
        security.update_token(current_user.get_sso_data())

        character_id = current_user.get_character_id()
        op = esiApp.op['get_characters_character_id_assets'](character_id=character_id)

        response = client.head(op)

        if response.status == 200:
            number_of_page = response.header['X-Pages'][0]

            if number_of_page > 1:

                operations = []
                for page in range(1, number_of_page + 1):
                    operations.append(
                        esiApp.op['get_characters_character_id_assets'](
                            character_id=character_id,
                            page=page)
                    )

                results = client.multi_request(operations)

                item_list = []

                for resp in results:
                    item_list += resp[1].data

                type_list = [34, 35, 36, 37, 38, 39, 40]

                item_list = [
                    {"type_id": item['type_id'],
                     "quantity": item['quantity']}
                    for item in item_list if item['type_id'] in type_list
                ]

                formated_item_list = []

                for type_id in type_list:
                    qty = 0
                    for item in item_list:

                        if type_id == item['type_id']:
                            qty += item['quantity']

                    formated_item_list += [{"type_id": type_id, "quantity": qty}]

        return render_template("assets.html", items=formated_item_list)


@app.route("/check")
def check():
    check_user_session = UserSession().query.filter_by(session_id='12345').first()
    print(check_user_session)

    return str(check_user_session.token_id)


@app.route("/pop")
def pop():
    if len(session) > 1:
        session.pop('token')

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
