import sqlite3
import os

from datetime import datetime
from datetime import timedelta

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "sqlite-latest.sqlite")
conn = sqlite3.connect(db_path)
cur = conn.cursor()


def save_user_data(session, token_json, character_json):
    new_session = Session

    new_session.session_id = session
    new_session.token_id = insert_token(token_json=token_json)
    new_session.unique_character_id = insert_character(character_json=character_json)

    insert_session()
    pass


def is_session_valid(token):
    session_token = cur.execute("SELECT [sessionID] FROM Sessions WHERE sessionID = ?", token).fetchall()

    if token in session_token:
        return True
    else:
        return False


def insert_session():
    cur.execute("INSERT INTO Sessions VALUES (?,?,?,?,?)", ())
    pass


def get_session():
    pass


def insert_token(token_json):
    token_json["expires_in"] = datetime.now() + timedelta(seconds=token_json["expires_in"])

    last_id = cur.execute("INSERT (accessToken, expiresAt, tokenType, refreshToken) INTO Tokens VALUES (?,?,?,?)", (
        token_json["access_token"], token_json["expires_in"], token_json["token_type"], token_json["refresh_token"])
                          ).lastrowid

    return last_id


def insert_character(character_json):
    last_id = cur.execute(
        "INSERT (characterID, characterName, corporationID, eTag) INTO Characters VALUES (?, ?, ?, ?)",
        ()
    ).lastrowid

    return last_id


def get_token_from_database(session_id):
    pass


def get_characters(self, token):
    pass


def get_assets():
    pass
