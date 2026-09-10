"""Explicit callable registry; no reflection or module loading from data."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Adapter:
    adapter_id: str
    supported_profiles: tuple
    evaluate: object
    version: str = "0"
    contextual: bool = False

    def invoke(self, fixture, context):
        return self.evaluate(fixture, context) if self.contextual else self.evaluate(fixture)

class AdapterRegistry:
    def __init__(self, adapters=()):
        self._adapters = {}
        for adapter in adapters:
            if not isinstance(adapter, Adapter) or type(adapter.adapter_id) is not str or not adapter.adapter_id or not adapter.adapter_id.isascii() or not callable(adapter.evaluate):
                raise ValueError("invalid adapter registration")
            if type(adapter.version) is not str or not adapter.version or type(adapter.supported_profiles) is not tuple or any(type(p) is not str or not p for p in adapter.supported_profiles) or type(adapter.contextual) is not bool:
                raise ValueError("invalid adapter version/capabilities")
            if adapter.adapter_id in self._adapters:
                raise ValueError("duplicate adapter registration")
            self._adapters[adapter.adapter_id] = adapter

    def resolve(self, adapter_id, profile_id):
        adapter = self._adapters.get(adapter_id)
        if adapter is None or profile_id not in adapter.supported_profiles:
            return None
        return adapter

    def identities(self):
        return tuple(sorted(self._adapters))
