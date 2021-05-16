from flask import Flask
import logging
from flask import request
from flasks.trace import tracer
from flasks.trace.handler import after_request_trace, before_request_trace


# from flasks.tracing import tracing, jaeger_tracer


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("hello.cfg")

    from flasks import blog
    app.register_blueprint(blog.bp)

    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)

    @app.before_request
    def start_trace():
        before_request_trace(tracer)

    @app.after_request
    def end_trace(response):
        after_request_trace(response)
        return response

    @app.teardown_request
    def end_trace_with_error(response):
        pass
        # if response is not None:
        #     after_request_trace(error=e)

    @app.errorhandler(Exception)
    def exception_trace(e):
        after_request_trace(error=e)
        raise e

    return app
