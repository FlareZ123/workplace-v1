"""Bounded same-job late-cohort xoshiro128** source holdout (no K04 target read).

Based on the .NET Random.Xoshiro128StarStarImpl transition; this is an
unproven producer hypothesis. Use only the two unselected requested attempts.
See Agent36 memory, 21 Oct 2026, for frozen assumptions and nearest prior art.
"""
from pathlib import Path
import hashlib

MOD = (1 << 32) - 1
SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def rotl(x, k):
    return ((x << k) | (x >> (32 - k))) & MOD


def rotr(x, k):
    return ((x >> k) | (x << (32 - k))) & MOD


def step(state):
    a, b, c, d = state
    t = (b << 9) & MOD
    c ^= a
    d ^= b
    b ^= c
    a ^= d
    c ^= t
    d = rotl(d, 11)
    return a, b, c, d


def output(state):
    return rotl((state[1] * 5) & MOD, 7) * 9 & MOD


def invert_output(value):
    return rotr(value * pow(9, -1, 1 << 32) & MOD, 7) * pow(5, -1, 1 << 32) & MOD


def generate(state, n):
    values = []
    for _ in range(n):
        values.append(output(state))
        state = step(state)
    return values


def recover(outputs):
    columns = []
    for bit in range(128):
        state = tuple(1 << (bit % 32) if i == bit // 32 else 0 for i in range(4))
        trajectory = []
        for _ in range(4):
            trajectory.append(state[1])
            state = step(state)
        columns.append(trajectory)
    pivots = {}
    for i, y in enumerate(outputs):
        state_word = invert_output(y)
        for bit in range(32):
            coeff = sum(((columns[j][i] >> bit) & 1) << j for j in range(128))
            rhs = (state_word >> bit) & 1
            while coeff:
                lead = coeff.bit_length() - 1
                if lead not in pivots:
                    pivots[lead] = (coeff, rhs)
                    break
                old_coeff, old_rhs = pivots[lead]
                coeff ^= old_coeff
                rhs ^= old_rhs
            else:
                if rhs:
                    return None, len(pivots)
    answer = 0
    for lead in sorted(pivots):
        coeff, rhs = pivots[lead]
        if rhs ^ ((coeff & answer).bit_count() & 1):
            answer |= 1 << lead
    return tuple((answer >> (32 * i)) & MOD for i in range(4)), len(pivots)


def unpack(data, endian, reverse):
    values = [int.from_bytes(data[i:i + 4], endian) for i in range(0, 16, 4)]
    return values[::-1] if reverse else values


def run():
    seed = (0x12345678, 0x9ABCDEF0, 0x23456789, 0xABCDEF01)
    recovered, rank = recover(generate(seed, 4))
    assert rank == 128 and recovered == seed
    assert generate(recovered, 12)[8:12] == generate(seed, 12)[8:12]
    print("SYNTHETIC PASS exact 128-bit state and skipped-attempt prediction")

    source = Path(__file__).resolve().parents[2] / "resources/evidence/print/spool-reconstruction.log"
    data = source.read_bytes()
    assert hashlib.sha256(data).hexdigest() == SHA
    lines = data.decode("ascii").splitlines()
    def payload(attempt, state):
        matches = [line for line in lines if
                   "JOB=PS-261003-0417 " in line and
                   f"ATTEMPT={attempt} STATE={state} CLASS=RECOVER " in line]
        assert len(matches) == 1
        return bytes.fromhex(matches[0].split("PAYLOAD=")[1].split()[0])

    # Intentionally do not parse, read or hash the disputed attempt 2 ACK.
    first = payload(1, "REQUESTED")
    third = payload(3, "REQUESTED")
    for endian in ("little", "big"):
        for reverse in (False, True):
            state, rank = recover(unpack(first, endian, reverse))
            assert state is not None and rank == 128
            predicted = generate(state, 12)[8:12]
            observed = unpack(third, endian, reverse)
            bit_distance = sum((a ^ b).bit_count() for a, b in zip(predicted, observed))
            print(f"ORIGINAL endian={endian} reverse={reverse} rank={rank} "
                  f"predicted_third_match={predicted == observed} "
                  f"bit_distance={bit_distance}")
            assert bit_distance != 0
    print("STOP: zero full 128-bit heldout hits across four fixed encodings.")
    print("Target coupon not inspected; no accepted K04 bytes or K08 words recovered.")


if __name__ == "__main__":
    run()
