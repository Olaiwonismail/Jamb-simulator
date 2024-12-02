
import os
class Config:
    # SQLALCHEMY_DATABASE_URI  = 'sqlite:///sqlite.db'
    SQLALCHEMY_DATABASE_URI =os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY=os.environ.get('secret_key')
    # MAIL_SERVER='smtp.gmail.com'
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    # SQLALCHEMY_DATABASE_URI =  os.getenv('SQLALCHEMY_DATABASE_URI')
