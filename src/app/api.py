import atexit
from flask import Flask, request, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from flask_compress import Compress
from src import config
from src.app.routing.router import Router
from src.app.utils.logging.logger import Logger
from src.app.utils.http import http_methods
from src.app.utils.logo_printer import LogoPrinter
from src.infrastructure.database.db_migrator import DBMigrator

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
compress = Compress(app)

router = Router()


@app.route(F'/{Router.get_base_url()}/<path:path>', methods=http_methods.get_methods_list())
@compress.compressed()
def route(path):
    Logger.info(f'Routing to: {path}')
    return router.route(request, path)


@app.route('/', methods=[http_methods.GET])
@compress.compressed()
def root():
    Logger.info('Index route')
    return send_from_directory(config.CLIENT_APP_FOLDER, 'index.html')


@app.route('/<path:path>', methods=[http_methods.GET])
@compress.compressed()
def static_file(path):
    Logger.info(f'Returning static file: {path}')
    return send_from_directory(config.CLIENT_APP_FOLDER, path)


@app.route('/', defaults={'path': ''}, methods=http_methods.get_methods_list())
@app.route('/<path:path>', methods=http_methods.get_methods_list())
def not_found(path):
    Logger.info("Route not found: %s", path)
    return router.error_response('Not found!', 404)


def on_app_stopped():
    Logger.info("App stopped")


atexit.register(on_app_stopped)


def on_starting(server=None):
    router.print_routemap()
    LogoPrinter.print_logo()
    DBMigrator().run_migrations()
    Logger.info("App started")


def run():
    on_starting()
    app.run(debug=config.APP_RUN_DEBUG_MODE,
            use_reloader=config.APP_USE_RELOADER,
            port=config.APP_PORT,
            host=config.HOST)
