import atexit
from flask import Flask, request, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from flask_compress import Compress
from src import config
from src.routing.router import Router
from src.utils.logger import Logger
from src.utils.http import http_methods
from src.database.db_migrator import DBMigrator
from src.utils.logo_printer import LogoPrinter

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
compress = Compress(app)

router = Router()


@app.route(F'/{Router.get_base_url()}/<path:path>', methods=http_methods.get_methods_list())
@compress.compressed()
def route(path):
    Logger.get_logger(__file__).debug("router route: %s", path)
    return router.route(request, path)


@app.route('/', methods=[http_methods.GET])
@compress.compressed()
def root():
    Logger.get_logger(__file__).debug("index route")
    return send_from_directory(config.CLIENT_APP_FOLDER, 'index.html')


@app.route('/<path:path>', methods=[http_methods.GET])
@compress.compressed()
def static_file(path):
    Logger.get_logger(__file__).debug("static file: %s", path)
    return send_from_directory(config.CLIENT_APP_FOLDER, path)


@app.route('/', defaults={'path': ''}, methods=http_methods.get_methods_list())
@app.route('/<path:path>', methods=http_methods.get_methods_list())
def not_found(path):
    print(F"{path} not found")
    Logger.get_logger(__file__).info("Not found route: %s", path)
    return router.error_response('Not found!', 404)


def on_app_stopped():
    Logger.get_logger(__file__).info("App stopped")


atexit.register(on_app_stopped)


def on_starting(server):
    router.print_routemaps()
    LogoPrinter.print_logo()
    DBMigrator().run_migrations()
    Logger.get_logger(__file__).info("App started")


def run():
    on_starting(None)
    app.run(debug=config.APP_RUN_DEBUG_MODE,
            use_reloader=config.APP_USE_RELOADER,
            port=config.APP_PORT)
