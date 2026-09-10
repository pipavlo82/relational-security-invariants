from eth_utils import keccak, to_bytes, to_hex


def compute_verdict_hash(job_id: str, result_text: str) -> str:
    """
    Compute the verdictHash for an ERC-8203 SettlementProofRef.

    ERC-8203 (ConsultEscrow release commitment):
        verdictHash = keccak256(abi.encode(
            bytes32 jobId,
            keccak256(utf8(resultText))
        ))

    This is the commitment ConsultEscrow.release() recomputes on-chain before
    checking the attestor signature. The result is fully re-derivable from
    public data — both jobId and resultText are emitted in the Released event.

    Since both jobId and resultHash are 32-byte values, abi.encode(bytes32, bytes32)
    is equivalent to simple byte concatenation.

    Args:
        job_id: The 32-byte job identifier (0x-prefixed hex string).
        result_text: The delivered result text (UTF-8).

    Returns:
        The 32-byte verdict/commitment hash as a 0x-prefixed hex string.
    """
    result_bytes = result_text.encode("utf-8")
    result_hash = keccak(result_bytes)
    job_bytes = to_bytes(hexstr=job_id)
    combined = job_bytes + result_hash
    return to_hex(keccak(combined))
