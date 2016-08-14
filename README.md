## Benchmarks to compare scrapy's old and new signal API

The bootstrapping tools have been taken from the [djangobench](https://github.com/django/djangobench) but modified heavily for our
purposes. The benchmark reporting is however keeps mostly the same format. It does not support vcs branches however, you need two separate source trees(control and experimental).

Usage:

`scrapysignalbench --control control-dir --experiment experiment-dir`
