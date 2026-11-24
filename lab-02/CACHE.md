# Cache

## Cache configuration

Used `actions/setup-python` with `cache: pip`

The cache key depends on:

- `lab-02/requirements.txt`
- `lab-02/requirements-dev.txt`

### Cold run

- Commit: `51b38d3`
- Cache status: `pip cache is not found`
- Dependency installation duration: 4 s

### Warm run

- Commit: `29023e3`
- Cache status:`Cache restored successfully`
- Dependency installation duration: 3 s
- Restored cache size: ~7 MB 

## Observation

The first workflow run did not find an existing pip cache, so it downloaded the required dependencies and created the cache. The second run successfully restored the cache using the same dependency configuration, installation time decreased, demonstrating that the pip cache was reused successfully.