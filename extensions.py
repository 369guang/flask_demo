from flask_sqlalchemy import SQLAlchemy
from flasks.trace import init_tracer

db = SQLAlchemy()
tracer = init_tracer('flasks', {
    'sampler': {
        'type': 'const',
        'param': 1,
    },
    'local_agent': {
        'reporting_host': '10.10.253.8',
    },
    'logging': True,
})
