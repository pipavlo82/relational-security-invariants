"""Trusted application wiring. Data cannot select imports or executable code."""
from adapters.messaging import model as messaging
from adapters.generic import model as generic
from profiles.synthetic import make_profile, PROFILE_ID
from runner.adapter_registry import Adapter, AdapterRegistry
from runner.expectation_registry import ExpectationRegistry

DEFAULT_PROFILE = PROFILE_ID


def registries(root):
    profiles = ExpectationRegistry([make_profile(root)])
    # Wrappers intentionally read module functions at execution time so existing
    # adapter fault-injection tests and source mutants exercise the native code.
    adapters = AdapterRegistry([
        Adapter("messaging", (PROFILE_ID,), lambda request: messaging.run(request)),
        Adapter("generic", (PROFILE_ID,), lambda request: generic.run(request)),
    ])
    return profiles, adapters
