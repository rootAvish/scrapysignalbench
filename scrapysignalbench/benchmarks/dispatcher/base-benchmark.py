from pydispatch import dispatcher

from scrapysignalbench.utils import run_benchmark
from scrapy.utils.signal import send_catch_log


class sender:
    pass


test_signal = object()

def callback(**kwargs):
    pass

dispatcher.connect(callback, test_signal)

def benchmark():
    send_catch_log(test_signal, sender=sender)

run_benchmark(
    benchmark,
    trials = 100,
    meta = {
        'description': 'A raw apples to apples, signal only comparison'
    }
)
