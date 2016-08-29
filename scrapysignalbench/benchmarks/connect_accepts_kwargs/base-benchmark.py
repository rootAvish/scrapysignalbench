from scrapysignalbench.utils import run_benchmark
from scrapy.signalmanager import SignalManager


test_signal = object()

signals = SignalManager()


def callback(arg1, arg2, **kwargs):
	pass


def benchmark():
	signals.connect(callback, test_signal)


run_benchmark(
	benchmark,
	trials=100,
	meta = {
		'description': """A benchmark to test signal connection time with
			a receiver that accepts **kwargs.
			"""
	})
