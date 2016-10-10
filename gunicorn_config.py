import multiprocessing
import os

bind = "0.0.0.0:{}".format(os.environ['PORT'])
workers = multiprocessing.cpu_count() * 2 + 1
