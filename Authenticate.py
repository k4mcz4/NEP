import urllib
import requests
import hashlib
import os

class Authenticate(object):

    def __init__(self, method):
        self.redirect_uri = "https://login.eveonline.com/v2/oauth/authorize/"
        self.client_id = "3992818" #Unknown due to lack of access
        self.scope = "esi.wallet_example" #Scope should be passed from front end
        self.state = hashlib.sha256(os.urandom(1024)).hexdigest()
        
    def get_state(self):
        return self.state
        
    def get_uri(self):
        return f"{self.redirect_uri}?client_id={self.client_id}&scope={self.scope}&state={self.state}"

    def authenticate_redirect():
        return "http://www.google.com"