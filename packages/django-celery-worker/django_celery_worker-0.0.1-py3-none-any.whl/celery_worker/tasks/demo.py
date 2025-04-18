# -*- coding: utf-8 -*-

from celery_worker.app import app


@app.task
def add(n, m):
    try:
        print(f'{n} + {m}的结果：{n + m}')
    except Exception as e:
        print(e.args)

    return n + m
