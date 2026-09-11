/**
 * Check that the sum of reserved and confirmed amounts does not exceed the cap.
 *
 * ERC-8312 (StatefulBound variant): (reserved + confirmed) <= cap.
 *
 * @param reserved - The reserved amount (non-negative integer).
 * @param confirmed - The confirmed amount (non-negative integer).
 * @param cap - The cap (total capacity).
 * @returns true if the sum is within the cap, false otherwise.
 */
export function checkStatefulBound(
  reserved: number,
  confirmed: number,
  cap: number,
): boolean {
  return reserved + confirmed <= cap
}

/**
 * Check that an aggregate cursor value does not exceed the cap.
 *
 * ERC-8312 (Orbmis/headroom variant): aggregate <= cap.
 *
 * @param aggregate - The aggregate cursor value (non-negative integer).
 * @param cap - The cap (total capacity).
 * @returns true if the aggregate is within the cap, false otherwise.
 */
export function checkCursorHeadroom(
  aggregate: number,
  cap: number,
): boolean {
  return aggregate <= cap
}

/**
 * Compute the remaining headroom from cap and cumulative spent.
 *
 * ERC-8312 §IBudgetSubstrate: remaining = cap - spent.
 * Returns 0 if spent exceeds cap (exhausted or inactive envelope).
 *
 * @param cap - The maximum capacity (non-negative integer).
 * @param spent - The cumulative amount consumed (non-negative integer).
 * @returns The remaining headroom (non-negative integer).
 */
export function computeRemainingHeadroom(
  cap: number,
  spent: number,
): number {
  return Math.max(0, cap - spent)
}

/**
 * Verify that reported remaining matches cap - spent.
 *
 * ERC-8312 §IBudgetSubstrate: remaining(id) is recomputed, never trusted.
 *
 * @param cap - The maximum capacity.
 * @param spent - The cumulative amount consumed.
 * @param reportedRemaining - The reported remaining headroom.
 * @returns true if the reported value matches the recomputed headroom.
 */
export function verifyRemaining(
  cap: number,
  spent: number,
  reportedRemaining: number,
): boolean {
  return spent <= cap && computeRemainingHeadroom(cap, spent) === reportedRemaining
}
