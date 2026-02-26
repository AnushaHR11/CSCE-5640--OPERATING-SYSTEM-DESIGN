from collections import deque
import argparse


def format_frames(frame):
    return "[" + ", ".join(str(x) if x is not None else "-" for x in frame) + "]"


def print_steps(steps, algo_name):
    print(f"\n=== {algo_name} ===")
    print("Step  Page  Fault  Frames")
    for i, (page, fault, frame) in enumerate(steps, start=1):
        print(f"{i:>4}  {str(page):>4}  {'Y' if fault else 'N':>5}  {format_frames(frame)}")


def simulate_fifo(ref, frames):
    frame = [None] * frames
    queue = deque()  # stores frame indexes in FIFO order
    faults = 0
    steps = []

    for page in ref:
        hit = page in frame
        if not hit:
            faults += 1
            if None in frame:
                idx = frame.index(None)
                frame[idx] = page
                queue.append(idx)
            else:
                idx = queue.popleft()
                frame[idx] = page
                queue.append(idx)

        steps.append((page, not hit, frame.copy()))

    return faults, steps


def simulate_lru(ref, frames):
    frame = [None] * frames
    last_used = {}  # page -> time index
    faults = 0
    steps = []

    for t, page in enumerate(ref):
        hit = page in frame
        if hit:
            last_used[page] = t
        else:
            faults += 1
            if None in frame:
                idx = frame.index(None)
                frame[idx] = page
                last_used[page] = t
            else:
                # victim = least recently used among pages currently in frames
                victim = min(frame, key=lambda pg: last_used.get(pg, -1))
                idx = frame.index(victim)
                del last_used[victim]
                frame[idx] = page
                last_used[page] = t

        steps.append((page, not hit, frame.copy()))

    return faults, steps


def simulate_optimal(ref, frames):
    frame = [None] * frames
    faults = 0
    steps = []

    for i, page in enumerate(ref):
        hit = page in frame
        if not hit:
            faults += 1
            if None in frame:
                idx = frame.index(None)
                frame[idx] = page
            else:
                # victim = page whose next use is farthest in the future (or never used again)
                future_next_use = {}
                for pg in frame:
                    try:
                        nxt = ref.index(pg, i + 1)
                    except ValueError:
                        nxt = float("inf")
                    future_next_use[pg] = nxt

                victim = max(frame, key=lambda pg: future_next_use[pg])
                idx = frame.index(victim)
                frame[idx] = page

        steps.append((page, not hit, frame.copy()))

    return faults, steps


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames", type=int, required=True, help="Number of frames (>=1)")
    parser.add_argument("--ref", type=str, required=True, help='Reference string, e.g. "7 0 1 2 0 3"')
    args = parser.parse_args()

    if args.frames < 1:
        raise SystemExit("Error: --frames must be >= 1")

    ref = args.ref.split()

    fifo_faults, fifo_steps = simulate_fifo(ref, args.frames)
    lru_faults, lru_steps = simulate_lru(ref, args.frames)
    opt_faults, opt_steps = simulate_optimal(ref, args.frames)

    print(f"Reference string: {ref}")
    print(f"Frames: {args.frames}")

    print_steps(fifo_steps, "FIFO")
    print(f"FIFO Page Faults: {fifo_faults}")

    print_steps(lru_steps, "LRU")
    print(f"LRU Page Faults: {lru_faults}")

    print_steps(opt_steps, "Optimal")
    print(f"Optimal Page Faults: {opt_faults}")

    print("\nSummary (faults):")
    print(f"  FIFO   : {fifo_faults}")
    print(f"  LRU    : {lru_faults}")
    print(f"  Optimal: {opt_faults}")


if __name__ == "__main__":
    main()