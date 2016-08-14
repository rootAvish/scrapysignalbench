from scrapy.signals import Signal

from scrapysignalbench.utils import run_benchmark


class sender:
    pass


test_signal = Signal()

def callback(**kwargs):
    pass

test_signal.connect(callback)

def benchmark():
    test_signal.send_robust(sender=sender)

run_benchmark(
    benchmark,
    trials = 100,
    meta = {
        'description': 'A raw apples to apples, signal only comparison'
    }
)
