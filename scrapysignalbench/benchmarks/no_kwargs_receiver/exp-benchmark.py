from scrapysignalbench.utils import run_benchmark
from scrapy.signals import Signal
from scrapy.signalmanager import SignalManager


test_signal = Signal()

def receiver(arg1, arg2):
	pass

signals = SignalManager()

signals.connect(receiver, test_signal)

def benchmark():
	args = {'arg1': 'test', 'arg2': 'test'}
	signals.send_catch_log(test_signal, **args)

run_benchmark(
	benchmark,
	trials=100,
	meta= {
		'description': """
			This benchmark compares the performance of a receiver that does take
			**kwargs under the old and the new signal API.
		"""
	})
