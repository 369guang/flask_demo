import logging
import time
from functools import wraps
from flask import Blueprint
import requests
from flask import current_app, request
from flasks.extensions import db, tracer
from flasks.model.todo import Todo
from flasks.trace import inject

bp = Blueprint("blog", __name__)


#
# def cost_count(func):
#     @wraps(func)
#     def wraper(*args, **kwargs):
#         start = time.time()
#         t = func(*args, **kwargs)
#         # print(request.__dict__)
#         print("请求路径：", request.url)
#         print("请求类型：", request.method)
#         if request.method == "GET":
#             print("GET请求值", request.args)
#         else:
#             print(f"{request.method}请求值", request.form, request.json)
#         current_app.logger.info("%s tooks time: %f", func.__name__, time.time() - start)
#         # print(time.time() - start)
#         return t
#
#     return wraper


@bp.route("/")
# @tracing.trace()
def index():
    # data = Todo.query.all()
    # print(data)
    tracer_test("http://localhost:5000/index2")
    tracer_test("http://localhost:5000/index3")
    return "hello world"


@bp.route("/index2")
# @tracing.trace()
def index2():
    return "hello world2"


@bp.route("/index3")
# @tracing.trace()
def index3():
    return "hello world3"


def tracer_test(url):
    headers = inject(tracer)
    start_time = time.time()  # 记录程序开始运行时间

    requests.get(url, params={}, headers=headers)

    end_time = time.time()  # 记录程序结束运行时间
    print('Took %f second' % (end_time - start_time))


@bp.route("/add")
# @cost_count
def add():
    session = db.session
    print(session)
    try:
        obj1 = Todo(title='hello')
        obj2 = Todo(title='hello')
        obj3 = Todo(title='hello')
        obj4 = Todo(id=1, title='hello')
        session.add_all([obj1, obj2, obj3, obj4])
        session.commit()
    except Exception as ex:
        print("error", ex)
        session.rollback()

    data = Todo.query.all()
    print(data)
    return "hadd"


@bp.route("/update", methods=["POST"])
# @cost_count
def update():
    # data = Todo.query.all()
    # print(data)
    return "update"
