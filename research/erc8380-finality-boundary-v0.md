# ERC-8380 finality boundary v0

Canonical consumption != irreversible off-chain effect. At-most-once != exactly-once.

Live discussion posts 28/29 identify the reorg boundary. Author posts 31 and 33 (74072 and 74074, September 10) acknowledge it and promise a future Security Considerations addition. At inspected PR head 7068f2a2853504475d966c06c8e04ec6d546dbb8, no Finality and Off-Chain Side Effects section was found. Reference SPEC.md likewise has no such section. Classification: INTENT ONLY / author clarification, not landed normative text or implemented finality policy.

The Guard source writes consumed state and emits NullifierBurned before the target call, reverting the transaction if the call fails. This is an atomic contract-state rule assuming a sound verifier. It does not establish canonical inclusion, finality, exactly-once execution, or irreversible external effects. A capability may never be submitted.

A history where a burn is removed and a new history where it is unconsumed must not automatically become clone evidence. No RSI reorg simulator, consensus assumptions, confirmation count, finality threshold or off-chain action fixture was invented. No first/second spend was executed in this stopped phase; existing upstream tests are classified as tests, not independent RSI results.

The finality wording can be bounded as intended semantics, so its pending status alone is not the proving-lane blocker. The blocker is the mismatch between required tagged Keccak and the placeholder circuit helpers, plus non-interchangeable reference/draft domain tags.
