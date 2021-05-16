import opentracing

from flask import g, request
from .ext import TRACE_ID, COMPONENT, HTTP_METHOD, HTTP_URL, SPAN_KIND, SPAN_KIND_RPC_SERVER, REQUEST_ID, \
    HTTP_STATUS_CODE, ERROR, SPAN_KIND_RPC_CLIENT


def format_hex_trace_id(trace_id: int):
    return '{:x}'.format(trace_id)


def before_request_trace(tracer):
    """
    before

    eg:
        @app.before_request
        def befor():
            before_request_trace(tracer)
    :param tracer:
    :return:
    """
    operation_name = request.endpoint
    # print(operation_name, request.headers)
    headers = {}

    for k, v in request.headers:
        headers[k.lower()] = v

    try:
        # 判断是否有父节点，创建
        span_ctx = tracer.extract(opentracing.Format.HTTP_HEADERS, headers)
        print(span_ctx)
        scope = tracer.start_active_span(operation_name, child_of=span_ctx)
    except (opentracing.InvalidCarrierException,
            opentracing.SpanContextCorruptedException):
        # 创建
        scope = tracer.start_active_span(operation_name)

    span = scope.span
    span.set_tag(COMPONENT, 'Flask')
    span.set_tag(TRACE_ID, format_hex_trace_id(span.trace_id))
    span.set_tag(HTTP_METHOD, request.method)
    span.set_tag(HTTP_URL, request.base_url)
    span.set_tag(SPAN_KIND, SPAN_KIND_RPC_SERVER)

    request_id = headers.get(REQUEST_ID)
    if request_id:
        span.set_tag(REQUEST_ID, request_id)

    g.scope = scope
    return scope


def after_request_trace(response=None, error=None):
    """
    eg:
        @app.after_request
        def end_trace(response):
            after_request_trace(response)
            return response
        @app.teardown_request
        def end_trace_with_error(error):
            if error is not None:
                after_request_trace(error=error)
    or:
        class APIBaseView(MethodView):
            def dispatch_request(self, *args, **kwargs):
                before_request_trace(tracer)
                try:
                    response = super(APIBaseView, self).dispatch_request(*args, **kwargs)
                except Exception as e:
                    after_request_trace(error=e)
                    raise e
                else:
                    after_request_trace(response)
                    return response
    """
    scope = getattr(g, 'scope', None)
    if not scope:
        return

    if response is not None:
        scope.span.set_tag(HTTP_STATUS_CODE, response.status_code)
    if error is not None:
        scope.span.set_tag(ERROR, True)
        scope.span.log_kv({
            'event': ERROR,
            'error.kind': type(error),
            'error.object': error,
            'error.stack': error.__traceback__,
            'request.headers': request.headers,
            'request.args': request.args,
            'request.data': request.data
        })

    scope.close()


def trace(tracer):
    """
    Function decorator that traces functions
    NOTE: Must be placed after the @app.route decorator
    eg:
        @app.route('/log')
        @trace(tracer) # Indicate that /log endpoint should be traced
        def log():
            pass
    """

    def decorator(view_func):
        def wrapper(*args, **kwargs):
            before_request_trace(tracer)
            try:
                response = view_func(*args, **kwargs)
            except Exception as e:
                after_request_trace(error=e)
                raise e
            else:
                after_request_trace(response)

            return response

        wrapper.__name__ = view_func.__name__
        return wrapper

    return decorator


def inject(tracer):
    span = tracer.active_span
    headers = {}
    tracer.inject(span, opentracing.Format.HTTP_HEADERS, headers)
    return headers
