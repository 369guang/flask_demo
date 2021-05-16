from jaeger_client import Config


def init_tracer(service_name: str, config: dict):
    """
    初始化全局tracer
    :param service_name:
    :param config:
    :return:
    """
    assert isinstance(config, dict)
    config['trace_id_header'] = config.get('trace_id_header', 'trace_id')

    configs = Config(config=config, service_name=service_name, validate=True)

    return configs.initialize_tracer()


trace_config = {
    'sampler': {
        'type': 'const',
        'param': 1,
    },
    'local_agent': {
        'reporting_host': '10.10.253.8',
    },
    'logging': True,
}

tracer = init_tracer('flasks', trace_config)
