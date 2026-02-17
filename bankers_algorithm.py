import sys


def read_ints_from_line(line: str):
    return [int(x) for x in line.strip().split() if x.strip()]


def compute_need(maxm, alloc):
    n = len(maxm)
    m = len(maxm[0])
    need = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            need[i][j] = maxm[i][j] - alloc[i][j]
    return need


def is_leq(vec_a, vec_b):
    return all(a <= b for a, b in zip(vec_a, vec_b))


def add_vec(a, b):
    return [x + y for x, y in zip(a, b)]


def sub_vec(a, b):
    return [x - y for x, y in zip(a, b)]


def safety_check(maxm, alloc, avail):
    n = len(alloc)
    m = len(avail)
    need = compute_need(maxm, alloc)

    work = avail[:]
    finish = [False] * n
    safe_seq = []

    progress = True
    while progress:
        progress = False
        for i in range(n):
            if not finish[i] and is_leq(need[i], work):
                work = add_vec(work, alloc[i])
                finish[i] = True
                safe_seq.append(i)
                progress = True

    if all(finish):
        return True, safe_seq
    return False, []


def validate_matrices(maxm, alloc, avail):
    n = len(alloc)
    if n == 0:
        raise ValueError("No processes provided.")
    m = len(avail)
    if m == 0:
        raise ValueError("No resource types provided.")

    if len(maxm) != n:
        raise ValueError("Max matrix row count must equal number of processes.")
    for i in range(n):
        if len(maxm[i]) != m or len(alloc[i]) != m:
            raise ValueError("All matrix rows must have length = number of resource types.")
        for j in range(m):
            if alloc[i][j] > maxm[i][j]:
                raise ValueError(f"Invalid input: Allocation[{i}][{j}] > Max[{i}][{j}]")
            if maxm[i][j] < 0 or alloc[i][j] < 0:
                raise ValueError("Max/Allocation values must be non-negative.")
    for x in avail:
        if x < 0:
            raise ValueError("Available values must be non-negative.")


def try_grant_request(pid, req, maxm, alloc, avail):
    n = len(alloc)
    if pid < 0 or pid >= n:
        return False, "Invalid process id."

    need = compute_need(maxm, alloc)

    if not is_leq(req, need[pid]):
        return False, "Request denied: request exceeds the process NEED."

    if not is_leq(req, avail):
        return False, "Request denied: not enough AVAILABLE resources."

    # Pretend allocation
    avail2 = sub_vec(avail, req)
    alloc2 = [row[:] for row in alloc]
    alloc2[pid] = add_vec(alloc2[pid], req)

    safe, seq = safety_check(maxm, alloc2, avail2)
    if safe:
        # Commit changes
        for j in range(len(avail)):
            avail[j] = avail2[j]
        for j in range(len(avail)):
            alloc[pid][j] = alloc2[pid][j]
        return True, f"Request granted. System remains SAFE.\nSafe sequence: " + " -> ".join(f"P{i}" for i in seq)

    return False, "Request denied: would make the system UNSAFE."


def prompt_matrix(rows, cols, name):
    print(f"Enter the {name} matrix ({rows} rows, each with {cols} integers):")
    mat = []
    for i in range(rows):
        while True:
            line = input().strip()
            vals = read_ints_from_line(line)
            if len(vals) != cols:
                print(f"  Please enter exactly {cols} integers.")
                continue
            mat.append(vals)
            break
    return mat


def interactive_mode():
    n = int(input("Enter the number of processes: ").strip())
    m = int(input("Enter the number of resource types: ").strip())

    alloc = prompt_matrix(n, m, "Allocation")
    maxm = prompt_matrix(n, m, "Max")

    while True:
        line = input("Enter the Available resources: ").strip()
        avail = read_ints_from_line(line)
        if len(avail) != m:
            print(f"  Please enter exactly {m} integers.")
            continue
        break

    validate_matrices(maxm, alloc, avail)

    safe, seq = safety_check(maxm, alloc, avail)
    if safe:
        print("System is in a SAFE state.")
        print("Safe sequence:", " -> ".join(f"P{i}" for i in seq))
    else:
        print("System is NOT in a safe state.")
        return

    while True:
        ans = input("Do you want to make a resource request? (y/n): ").strip().lower()
        if ans not in ("y", "n"):
            continue
        if ans == "n":
            break

        pid = int(input("Enter process id (e.g., 0 for P0): ").strip())
        while True:
            rline = input(f"Enter resource request for P{pid} ({m} integers): ").strip()
            req = read_ints_from_line(rline)
            if len(req) != m:
                print(f"  Please enter exactly {m} integers.")
                continue
            break

        ok, msg = try_grant_request(pid, req, maxm, alloc, avail)
        print(msg)

    print("Done.")


def parse_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

    first = read_ints_from_line(lines[0])
    if len(first) != 2:
        raise ValueError("First line must be: n m")

    n, m = first
    idx = 1

    alloc = []
    for _ in range(n):
        alloc.append(read_ints_from_line(lines[idx]))
        idx += 1

    maxm = []
    for _ in range(n):
        maxm.append(read_ints_from_line(lines[idx]))
        idx += 1

    avail = read_ints_from_line(lines[idx])

    validate_matrices(maxm, alloc, avail)
    return n, m, maxm, alloc, avail


def main():
    args = sys.argv[1:]

    if not args:
        interactive_mode()
        return

    if "--file" in args:
        fi = args.index("--file")
        if fi + 1 >= len(args):
            print("Missing file path after --file")
            sys.exit(1)
        path = args[fi + 1]
        n, m, maxm, alloc, avail = parse_file(path)

        safe, seq = safety_check(maxm, alloc, avail)
        if safe:
            print("System is in a SAFE state.")
            print("Safe sequence:", " -> ".join(f"P{i}" for i in seq))
        else:
            print("System is NOT in a safe state.")
            sys.exit(0)

        if "--request" in args:
            ri = args.index("--request")
            vals = args[ri + 1 :]
            if len(vals) != (1 + m):
                print(f"Request format: --request <pid> <r1> ... <rm>  (need {1+m} numbers)")
                sys.exit(1)

            pid = int(vals[0])
            req = [int(x) for x in vals[1:]]
            ok, msg = try_grant_request(pid, req, maxm, alloc, avail)
            print(msg)

        return

    print("Usage:")
    print("  python bankers_algorithm.py")
    print("  python bankers_algorithm.py --file input.txt")
    print("  python bankers_algorithm.py --file input.txt --request <pid> <r1> ... <rm>")
    sys.exit(1)


if __name__ == "__main__":
    main()
