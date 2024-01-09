from flask import Flask
from secrets import token_hex

from sostituzioni.control.configurazione import configurazione
from sostituzioni.control.cli import database_cli, importer_cli


app = Flask(__name__)

app.static_folder = configurazione.get("flaskstaticdir").path
app.template_folder = configurazione.get("flasktemplatedir").path

app.config["SECRET_KEY"] = token_hex(32)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
# sessiona dura 1 ora, dopodichè bisogna eseguire nuovamente il login
app.config["PERMANENT_SESSION_LIFETIME"] = 60 * 60
# il countdown viene ripristinato ad ogni richiesta
# ! attenzione, non si applica a socketio, soltanto a richieste http
app.config["SESSION_REFRESH_EACH_REQUEST"] = True

app.cli.add_command(database_cli)
app.cli.add_command(importer_cli)
