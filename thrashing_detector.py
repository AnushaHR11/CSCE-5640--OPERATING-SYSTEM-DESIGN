import argparse
from collections import deque


def parse_int_list(s: str):
    if not s.strip():
        return []
    return [int(x) for x in s.replace(",", " ").split()]


def logical_addresses_to_pages(logical_addrs, page_size, las_size):
    # validate
    for a in logical_addrs:
        if a < 0 or a >= las_size:
            raise ValueError(f"Logical address {a} out of range [0, {las_size-1}]")
    return [a // page_size for a in logical_addrs]


def lru_faults(ref_pages, frames):
    frame = []
    last_used = {}  # page -> last index
    faults = 0
    fault_each_step = []

    for t, p in enumerate(ref_pages):
        if p in frame:
            last_used[p] = t
            fault_each_step.append(0)
            continue

        faults += 1
        fault_each_step.append(1)

        if len(frame) < frames:
            frame.append(p)
            last_used[p] = t
        else:
            victim = min(frame, key=lambda pg: last_used.get(pg, -1))
            frame[frame.index(victim)] = p
            last_used.pop(victim, None)
            last_used[p] = t

    return faults, fault_each_step


def working_set_sizes(ref_pages, window):
    # WS(t,Δ) based on last 'window' references, inclusive
    sizes = []
    for t in range(len(ref_pages)):
        start = max(0, t - window + 1)
        ws = set(ref_pages[start : t + 1])
        sizes.append(len(ws))
    return sizes


def analyze_thrashing(ref_pages, frames, window, thrash_ratio_threshold=0.30):
    """
    thrash event at time t: |WS(t,Δ)| > frames
    Additionally report overall thrash ratio and LRU fault rate.
    """
    ws_sizes = working_set_sizes(ref_pages, window)
    thrash_flags = [1 if ws_sizes[t] > frames else 0 for t in range(len(ref_pages))]
    thrash_count = sum(thrash_flags)
    thrash_ratio = thrash_count / max(1, len(ref_pages))

    faults, fault_each_step = lru_faults(ref_pages, frames)
    fault_rate = faults / max(1, len(ref_pages))

    # "Thrashing occurs" summary decision:
    # We say thrashing occurs if a significant portion of time steps violate WS>frames
    # (default threshold 30%).
    thrashing = thrash_ratio >= thrash_ratio_threshold

    return {
        "frames": frames,
        "window": window,
        "n": len(ref_pages),
        "faults": faults,
        "fault_rate": fault_rate,
        "thrash_steps": thrash_count,
        "thrash_ratio": thrash_ratio,
        "thrashing": thrashing,
        "ws_sizes": ws_sizes,
        "thrash_flags": thrash_flags,
        "fault_each_step": fault_each_step,
    }


def print_step_table(ref_pages, result, show_steps_limit=60):
    n = result["n"]
    frames = result["frames"]
    window = result["window"]

    print(f"\n--- Step Details (frames={frames}, window={window}) ---")
    print("Step  Page  WS_size  WS>F  Fault(LRU)")
    limit = min(n, show_steps_limit)
    for i in range(limit):
        p = ref_pages[i]
        ws = result["ws_sizes"][i]
        tf = "Y" if result["thrash_flags"][i] else "N"
        fl = "Y" if result["fault_each_step"][i] else "N"
        print(f"{i+1:>4}  {p:>4}  {ws:>7}  {tf:>4}  {fl:>9}")
    if n > limit:
        print(f"... ({n-limit} more steps not shown)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, required=True, help="Number of physical frames available")
    ap.add_argument("--window", type=int, required=True, help="Working set window size Δ (in references)")
    ap.add_argument("--ref", type=str, default="", help='Page reference string, e.g. "7 0 1 2 0 3"')

    # Address translation inputs (optional)
    ap.add_argument("--las", type=int, default=0, help="Logical address space size in bytes (optional)")
    ap.add_argument("--page_size", type=int, default=0, help="Page size in bytes (optional)")
    ap.add_argument(
        "--addrs",
        type=str,
        default="",
        help='Logical addresses in bytes, e.g. "0 12 4097 8191" (optional)',
    )

    ap.add_argument("--show_steps", action="store_true", help="Print step-by-step WS/thrashing/fault table")
    args = ap.parse_args()

    if args.frames < 1:
        raise SystemExit("frames must be >= 1")
    if args.window < 1:
        raise SystemExit("window must be >= 1")

    # Build reference pages
    ref_pages = []
    if args.ref.strip():
        ref_pages = parse_int_list(args.ref)
    else:
        # must have las, page_size, addrs
        if args.las <= 0 or args.page_size <= 0 or not args.addrs.strip():
            raise SystemExit("Provide either --ref OR (--las --page_size --addrs).")
        logical_addrs = parse_int_list(args.addrs)
        ref_pages = logical_addresses_to_pages(logical_addrs, args.page_size, args.las)

    result = analyze_thrashing(ref_pages, args.frames, args.window)

    print("\n=== Thrashing Detector Report ===")
    print(f"References (pages): {ref_pages}")
    print(f"Frames: {result['frames']}")
    print(f"Working set window Δ: {result['window']}")
    print(f"Total references: {result['n']}")
    print(f"LRU page faults: {result['faults']} (fault rate = {result['fault_rate']:.3f})")
    print(
        f"WS violations (|WS|>frames): {result['thrash_steps']} "
        f"({result['thrash_ratio']:.3f} of steps)"
    )
    print(f"Thrashing: {'YES' if result['thrashing'] else 'NO'}")

    if args.show_steps:
        print_step_table(ref_pages, result)


if __name__ == "__main__":
    main()