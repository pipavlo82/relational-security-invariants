# Messaging reference adapters

`models.py` models tentative bootstrap processing and atomic position consumption. The auth model performs real AES-GCM authentication but stores its durable state representation in memory.

The concurrency model executes a deterministic stale-read schedule: both workers read first, then attempt consumption in each possible commit order. This exposes a removed compare-and-swap guard. It does not model actual OS threads, storage transactions, process crashes, arbitrary schedules, multi-device ratchets or a complete secure messaging protocol.
