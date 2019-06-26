import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET KEY') or 'you-will-never-guess'
    MONGODB_SETTINGS={
    'db': 'ChatDb',
    'host': 'mongodb+srv://admin:admin123@cluster0-yytvz.mongodb.net/ChatDb?retryWrites=true&w=majority',
    }
    MAIL_SERVER=os.environ.get('MAIL_SERVER')
    MAIL_PORT=int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    ADMINS=['susantest38@gmail.com']
    