Sample output for all benchmarks:

```bash
Running all benchmarks
Running 'no_kwargs_receiver' benchmark ...
Min: 0.000011 -> 0.000007: 1.5862x faster
Avg: 0.000012 -> 0.000009: 1.4045x faster
Significant (t=7.277109)
Stddev: 0.00000 -> 0.00000: 1.0950x smaller (N = 100)

Running 'connect_no_kwargs' benchmark ...
Min: 0.000007 -> 0.000013: 1.8621x slower
Avg: 0.000009 -> 0.000014: 1.6524x slower
Significant (t=-8.083380)
Stddev: 0.00000 -> 0.00001: 2.6941x larger (N = 100)

Running 'no_compatability_used' benchmark ...
Min: 0.000009 -> 0.000004: 2.1765x faster
Avg: 0.000011 -> 0.000005: 2.0548x faster
Significant (t=12.793539)
Stddev: 0.00000 -> 0.00000: 2.5308x smaller (N = 100)

Running 'dispatcher' benchmark ...
Min: 0.000009 -> 0.000004: 2.3125x faster
Avg: 0.000010 -> 0.000005: 2.1571x faster
Significant (t=15.301444)
Stddev: 0.00000 -> 0.00000: 2.6563x smaller (N = 100)

Running 'connect_accepts_kwargs' benchmark ...
Min: 0.000007 -> 0.000019: 2.7241x slower
Avg: 0.000009 -> 0.000022: 2.4746x slower
Significant (t=-7.760665)
Stddev: 0.00000 -> 0.00002: 4.3374x larger (N = 100)

Running 'proxied_signal' benchmark ...
Min: 0.000010 -> 0.000008: 1.2424x faster
Avg: 0.000011 -> 0.000009: 1.2551x faster
Significant (t=2.739335)
Stddev: 0.00001 -> 0.00001: 1.1157x smaller (N = 100)
```
