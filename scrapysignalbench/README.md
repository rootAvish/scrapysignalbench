Sample output for all benchmarks:

```bash
Running all benchmarks
Running 'no_kwargs_receiver' benchmark ...
Min: 0.000011 -> 0.000008: 1.3939x faster
Avg: 0.000012 -> 0.000009: 1.3835x faster
Significant (t=7.139338)
Stddev: 0.00000 -> 0.00000: 1.1631x smaller (N = 100)

Running 'connect_no_kwargs' benchmark ...
Min: 0.000004 -> 0.000009: 2.1765x slower
Avg: 0.000005 -> 0.000010: 2.2751x slower
Significant (t=-7.459467)
Stddev: 0.00000 -> 0.00001: 5.5780x larger (N = 100)

Running 'no_compatability_used' benchmark ...
Min: 0.000009 -> 0.000005: 1.8500x faster
Avg: 0.000010 -> 0.000005: 1.9596x faster
Significant (t=12.725295)
Stddev: 0.00000 -> 0.00000: 2.6974x smaller (N = 100)

Running 'dispatcher' benchmark ...
Min: 0.000009 -> 0.000004: 2.3125x faster
Avg: 0.000011 -> 0.000004: 2.5537x faster
Significant (t=3.843047)
Stddev: 0.00002 -> 0.00000: 14.9700x smaller (N = 100)

Running 'connect_accepts_kwargs' benchmark ...
Min: 0.000004 -> 0.000007: 1.8125x slower
Avg: 0.000005 -> 0.000008: 1.7462x slower
Significant (t=-11.774645)
Stddev: 0.00000 -> 0.00000: 1.8540x larger (N = 100)

Running 'proxied_signal' benchmark ...
Min: 0.000009 -> 0.000007: 1.2759x faster
Avg: 0.000010 -> 0.000009: 1.0688x faster
Not significant
Stddev: 0.00000 -> 0.00001: 2.1567x larger (N = 100)
```
