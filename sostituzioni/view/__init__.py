import logging
import signal

from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

from sostituzioni.model.app import app

logger = logging.getLogger(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

csrf = CSRFProtect(app)
socketio = SocketIO(app, manage_session=False)

from sostituzioni.view.errorhandlers import routes
import sostituzioni.view.legal

logger.debug("Importing blueprints..")
from sostituzioni.view.impostazioni import impostazioni as impostazioni_blueprint
from sostituzioni.view.auth import auth as auth_blueprint
from sostituzioni.view.visualizzazionefisica import (
    fisica as visualizzazionefisica_blueprint,
)
from sostituzioni.view.visualizzazioneonline import (
    online as visualizzazioneonline_blueprint,
)

app.register_blueprint(impostazioni_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(visualizzazionefisica_blueprint)
app.register_blueprint(visualizzazioneonline_blueprint)


def exit_handler(signal, frame):
    logger.info("Shutting down")
    # todo: velocizzare il shutdown di socketio
    # socketio.emit("shutdown") per qualche motivo non funziona, clients non lo ricevono
    exit(0)


signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

logger.debug("All blueprints registered")
logger.info("System ready")
