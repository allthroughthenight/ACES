# -*- coding: utf-8 -*-
# try something like
# def index(): return dict(message="hello from test.py")
def inlet_process():
    return {'a':10, 'b':'hello world'}

def inlet_process2():
    c = 1
    d = 2
    # new = {'a':10, 'b':'hello world'}
    # new2 = dict()
    # new2 = locals()
    return locals()
