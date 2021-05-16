from flask import Flask
import logging
from flask import request
# from flasks.trace import tracer
# from flasks.trace.handler import after_request_trace, before_request_trace
from flasks.extensions import db, tracer
from flasks.trace import Tracing


# import sqlalchemy_opentracing

# from flasks.tracing import tracing, jaeger_tracer


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("hello.cfg")

    from flasks import blog
    app.register_blueprint(blog.bp)

    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)

    config = {
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'local_agent': {
            'reporting_host': '10.10.253.8',
        },
        'logging': True,
    }
    db.init_app(app)
    Tracing(app, tracer)
    return app
