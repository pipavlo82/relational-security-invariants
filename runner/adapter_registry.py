"""Explicit callable registry; no reflection or module loading from data."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Adapter:
    adapter_id: str
    supported_profiles: tuple
    evaluate: object

class AdapterRegistry:
    def __init__(self, adapters=()):
        self._adapters = {}
        for adapter in adapters:
            if not isinstance(adapter, Adapter) or not adapter.adapter_id or not callable(adapter.evaluate):
                raise ValueError("invalid adapter registration")
            if adapter.adapter_id in self._adapters:
                raise ValueError("duplicate adapter registration")
            self._adapters[adapter.adapter_id] = adapter

    def resolve(self, adapter_id, profile_id):
        adapter = self._adapters.get(adapter_id)
        if adapter is None or profile_id not in adapter.supported_profiles:
            return None
        return adapter
