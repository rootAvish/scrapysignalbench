#!/usr/bin/env python

"""
Originally a part of the `djangobench` project, heavily modified for the
purpose of benchmarking Scrapy's signal performance.
"""
import logging
import os

import subprocess
import argparse
import email
import simplejson
import sys
import perf


DEFAULT_BENCHMARK_DIR = os.path.join(os.path.dirname(__file__), 'benchmarks')


def run_benchmarks(control, experiment, benchmark_dir, benchmarks, trials,
                   record_dir=None, profile_dir=None,
                   continue_on_error=False):
    if benchmarks:
        print("Running benchmarks: %s" % " ".join(benchmarks))
    else:
        print("Running all benchmarks")

    if record_dir:
        record_dir = os.path.abspath(record_dir)
        if not os.path.isdir(record_dir):
            raise ValueError('Recording directory "%s" does not exist' % record_dir)
        print("Recording data to '%s'" % record_dir)
    if profile_dir:
        profile_dir = os.path.abspath(profile_dir)
        if not os.path.isdir(profile_dir):
            raise ValueError('Profile directory "%s" does not exist' % profile_dir)
        print("Recording profile data to '%s'" % profile_dir)

    control_env = {'PYTHONPATH': '%s:%s' % (os.path.abspath(control), benchmark_dir)}
    experiment_env = {'PYTHONPATH': '%s:%s' % (os.path.abspath(experiment), benchmark_dir)}

    for benchmark in discover_benchmarks(benchmark_dir):
        if not benchmarks or benchmark in benchmarks:
            print("Running '%s' benchmark ..." % benchmark)
            try:

                control_data = run_benchmark(benchmark, benchmark_dir, trials,
                                             env=control_env,
                                             prefix='base')

                experiment_data = run_benchmark(benchmark, benchmark_dir, trials,
                                                env=experiment_env,
                                                prefix='exp')
            except SkipBenchmark as reason:
                print("Skipped: %s\n" % reason)
                continue
            except RuntimeError as error:
                if continue_on_error:
                    print("Failed: %s\n" % error)
                    continue
                raise

            options = argparse.Namespace(
                track_memory=False,
                diff_instrumentation=False,
                benchmark_name=benchmark,
                disable_timelines=True,
                control_label='control',
                experiment_label='experiment',
            )
            result = perf.CompareBenchmarkData(control_data, experiment_data, options)
            if record_dir:
                record_benchmark_results(
                    dest=os.path.join(record_dir, '%s.json' % benchmark),
                    name=benchmark,
                    result=result,
                    control=control_label,
                    experiment=experiment_label,
                    control_data=control_data,
                    experiment_data=experiment_data,
                )
            print(format_benchmark_result(result, len(control_data.runtimes)))
            print('')


def discover_benchmarks(benchmark_dir):
    for app in os.listdir(benchmark_dir):
        if os.path.exists(os.path.join(benchmark_dir, app, 'exp-' + 'benchmark.py')) \
        or (os.path.join(benchmark_dir, app, 'base-' + 'benchmark.py')):
            yield app


def print_benchmarks(benchmark_dir):
    for app in discover_benchmarks(benchmark_dir):
        print(app)


class SkipBenchmark(Exception):
    pass


def run_benchmark(benchmark, benchmark_dir, trials, executable='python', env=None, prefix='base'):
    """
    Similar to perf.MeasureGeneric, but modified a bit for our purposes.
    """
    # Remove Pycs, then call the command once to prime the pump and
    # re-generate fresh ones. This makes sure we're measuring as little of
    # Python's startup time as possible.
    remove_pycs()
    command = [os.path.expanduser(executable),
               os.path.join(benchmark_dir, benchmark, prefix + '-benchmark.py')]
    out, _, _ = perf.CallAndCaptureOutput(command + ['-t', '1'], env, track_memory=False, inherit_env=[])
    if out.startswith('SKIP:'):
        raise SkipBenchmark(out.replace('SKIP:', '').strip())

    # Now do the actual mesurements.
    output = perf.CallAndCaptureOutput(command + ['-t', str(trials)], env, track_memory=False, inherit_env=[])
    stdout, stderr, mem_usage = output
    message = email.message_from_string(stdout)
    data_points = [float(line) for line in message.get_payload().splitlines()]
    return perf.RawData(data_points, mem_usage, inst_output=stderr)


def record_benchmark_results(dest, **kwargs):
    kwargs['version'] = __version__
    simplejson.dump(kwargs, open(dest, 'w'), default=json_encode_custom)


def json_encode_custom(obj):
    if isinstance(obj, perf.RawData):
        return obj.runtimes
    if isinstance(obj, perf.BenchmarkResult):
        return {
            'min_base': obj.min_base,
            'min_changed': obj.min_changed,
            'delta_min': obj.delta_min,
            'avg_base': obj.avg_base,
            'avg_changed': obj.avg_changed,
            'delta_avg': obj.delta_avg,
            't_msg': obj.t_msg,
            'std_base': obj.std_base,
            'std_changed': obj.std_changed,
            'delta_std': obj.delta_std,
        }
    if isinstance(obj, perf.SimpleBenchmarkResult):
        return {
            'base_time': obj.base_time,
            'changed_time': obj.changed_time,
            'time_delta': obj.time_delta,
        }
    raise TypeError("%r is not JSON serializable" % obj)


def supports_color():
    return sys.platform != 'win32' and hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


class colorize(object):
    GOOD = INSIGNIFICANT = SIGNIFICANT = BAD = ENDC = ''
    if supports_color():
        GOOD = '\033[92m'
        INSIGNIFICANT = '\033[94m'
        SIGNIFICANT = '\033[93m'
        BAD = '\033[91m'
        ENDC = '\033[0m'

    @classmethod
    def colorize(cls, color, text):
        return "%s%s%s" % (color, text, cls.ENDC)

    @classmethod
    def good(cls, text):
        return cls.colorize(cls.GOOD, text)

    @classmethod
    def significant(cls, text):
        return cls.colorize(cls.SIGNIFICANT, text)

    @classmethod
    def insignificant(cls, text):
        return cls.colorize(cls.INSIGNIFICANT, text)

    @classmethod
    def bad(cls, text):
        return cls.colorize(cls.BAD, text)


def format_benchmark_result(result, num_points):
    if isinstance(result, perf.BenchmarkResult):
        output = ''
        delta_min = result.delta_min
        if 'faster' in delta_min:
            delta_min = colorize.good(delta_min)
        elif 'slower' in result.delta_min:
            delta_min = colorize.bad(delta_min)
        output += "Min: %f -> %f: %s\n" % (result.min_base, result.min_changed, delta_min)

        delta_avg = result.delta_avg
        if 'faster' in delta_avg:
            delta_avg = colorize.good(delta_avg)
        elif 'slower' in delta_avg:
            delta_avg = colorize.bad(delta_avg)
        output += "Avg: %f -> %f: %s\n" % (result.avg_base, result.avg_changed, delta_avg)

        t_msg = result.t_msg
        if 'Not significant' in t_msg:
            t_msg = colorize.insignificant(t_msg)
        elif 'Significant' in result.t_msg:
            t_msg = colorize.significant(t_msg)
        output += t_msg

        delta_std = result.delta_std
        if 'larger' in delta_std:
            delta_std = colorize.bad(delta_std)
        elif 'smaller' in delta_std:
            delta_std = colorize.good(delta_std)
        output += "Stddev: %.5f -> %.5f: %s" %(result.std_base, result.std_changed, delta_std)
        output += " (N = %s)" % num_points
        output += result.get_timeline()
        return output
    else:
        return str(result)


def remove_pycs():
    perf.RemovePycs()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--control',
        metavar='BRANCH',
        help="Scrapy version to use as control, refers to a path."
    )
    parser.add_argument(
        '--experiment',
        metavar='BRANCH',
        help="Scrapy version to use as experiment, refers to a path."
    )
    parser.add_argument(
        '-t', '--trials',
        type=int,
        default=50,
        help='Number of times to run each benchmark.'
    )
    parser.add_argument(
        '-r', '--record',
        default=None,
        metavar='PATH',
        help='Directory to record detailed output as a series of JSON files.',
    )
    parser.add_argument(
        '--benchmark-dir',
        dest='benchmark_dir',
        metavar='PATH',
        default=DEFAULT_BENCHMARK_DIR,
        help='Directory to inspect for benchmarks. Defaults to `benchmarks` '
    )
    parser.add_argument(
        'benchmarks',
        metavar='name',
        default=None,
        help="Benchmarks to be run. Defaults to all.",
        nargs='*'
    )
    parser.add_argument(
        '-p',
        '--profile-dir',
        dest='profile_dir',
        default=None,
        metavar='PATH',
        help='Directory to record profiling statistics for the control and '
             'experimental run of each benchmark'
    )
    parser.add_argument(
        '--continue-on-error',
        dest='continue_on_error',
        action='store_true',
        help='Continue with the remaining benchmarks if any fail',
    )
    parser.add_argument(
        '-l',
        '--list',
        dest='list_benchmarks',
        action='store_true',
        help='List all available benchmarks and exit.',
    )
    parser.add_argument(
        '--log',
        dest='loglevel',
        default='WARNING',
        help='Define log level, set to INFO to show executed commands. Useful '
             'for debugging benchmarks.'
    )
    args = parser.parse_args()

    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)
    logging.basicConfig(level=numeric_level)

    if args.list_benchmarks:
        print_benchmarks(args.benchmark_dir)
    else:
        run_benchmarks(
            control=args.control,
            experiment=args.experiment,
            benchmark_dir=args.benchmark_dir,
            benchmarks=args.benchmarks,
            trials=args.trials,
            record_dir=args.record,
            profile_dir=args.profile_dir,
            continue_on_error=args.continue_on_error
        )

if __name__ == '__main__':
    main()
