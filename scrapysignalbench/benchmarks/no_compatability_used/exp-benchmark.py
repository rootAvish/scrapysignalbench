from scrapysignalbench.utils import run_benchmark
from scrapy.signalmanager import SignalManager
from scrapy.signals import Signal


def callback(**kwargs):
	pass

test_signal = Signal()
signals = SignalManager()

signals.connect(callback, test_signal)

def benchmark():
	signals.send_catch_log(test_signal)

run_benchmark(
	benchmark,
	trials = 100,
	meta = {
		'description': 'A benchmark to compare routing using signal manager in the new and the old scrapy API'
	}
)
