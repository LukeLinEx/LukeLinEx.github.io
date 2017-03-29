import sys
sys.path.append('/home/llin/coporate_training/universal')
from pymongo import MongoClient

def connect_remote_mongo():
    client = MongoClient('mongodb://heroku_q6lsp17r:695vf0bga9tl0q8tlo5r6lm4f6@216.230.228.86:61178/heroku_q6lsp17r')
    db = client.heroku_q6lsp17r
    remote = db.corporates
    users = db.users
    return remote, users

def connect_local_mongo():
    mm = MongoClient('localhost', 27017)
    mmdb = mm.test
    local = mmdb.server_users
    return local

def connect_accounts_db():
    mm = MongoClient('localhost', 27017)
    mmdb = mm.test
    accounts = mmdb.accounts
    return accounts
