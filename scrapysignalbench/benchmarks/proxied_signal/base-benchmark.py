from scrapysignalbench.utils import run_benchmark

from scrapy.signalmanager import SignalManager


test_signal = object()

signals = SignalManager()

def receiver(**kwargs):
	pass

signals.connect(receiver, test_signal)

def benchmark():
	signals.send_catch_log(test_signal)


run_benchmark(
		benchmark,
		trials=100,
		meta = {
			'description': """
				This test compares the performance when signals need to be
				proxied.
				"""
		}
	)
