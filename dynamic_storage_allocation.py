def first_fit(blocks, processes):
    remaining = blocks[:]
    allocation = [-1] * len(processes)

    for i, p in enumerate(processes):
        for j in range(len(remaining)):
            if remaining[j] >= p:
                allocation[i] = j
                remaining[j] -= p
                break

    return allocation, remaining


def best_fit(blocks, processes):
    remaining = blocks[:]
    allocation = [-1] * len(processes)

    for i, p in enumerate(processes):
        best_index = -1
        best_size = float("inf")

        for j in range(len(remaining)):
            if remaining[j] >= p and remaining[j] < best_size:
                best_size = remaining[j]
                best_index = j

        if best_index != -1:
            allocation[i] = best_index
            remaining[best_index] -= p

    return allocation, remaining


def worst_fit(blocks, processes):
    remaining = blocks[:]
    allocation = [-1] * len(processes)

    for i, p in enumerate(processes):
        worst_index = -1
        worst_size = -1

        for j in range(len(remaining)):
            if remaining[j] >= p and remaining[j] > worst_size:
                worst_size = remaining[j]
                worst_index = j

        if worst_index != -1:
            allocation[i] = worst_index
            remaining[worst_index] -= p

    return allocation, remaining


def print_results(strategy_name, blocks, processes, allocation, remaining):
    print(f"\n{strategy_name}:")
    print("-" * 60)
    print(f"{'Process':<10}{'Size':<10}{'Block Allocated':<18}{'Leftover in Block'}")
    print("-" * 60)

    total_fragmentation = 0

    for i, p in enumerate(processes):
        if allocation[i] != -1:
            block_no = allocation[i] + 1
            leftover = remaining[allocation[i]]
            print(f"{i + 1:<10}{p:<10}{block_no:<18}{leftover}")
        else:
            print(f"{i + 1:<10}{p:<10}{'Not Allocated':<18}{'-'}")

    print("-" * 60)
    print("Remaining memory in all blocks:")
    for i, r in enumerate(remaining):
        print(f"Block {i + 1}: {r}")

    total_fragmentation = sum(remaining)
    print(f"\nInternal Fragmentation ({strategy_name}): {total_fragmentation}")


def main():
    n_blocks = int(input("Enter number of memory blocks: "))
    blocks = list(map(int, input("Enter block sizes: ").split()))

    if len(blocks) != n_blocks:
        print("Error: Number of block sizes does not match the number of memory blocks.")
        return

    n_processes = int(input("Enter number of processes: "))
    processes = list(map(int, input("Enter process sizes: ").split()))

    if len(processes) != n_processes:
        print("Error: Number of process sizes does not match the number of processes.")
        return

    ff_allocation, ff_remaining = first_fit(blocks, processes)
    bf_allocation, bf_remaining = best_fit(blocks, processes)
    wf_allocation, wf_remaining = worst_fit(blocks, processes)

    print_results("First Fit", blocks, processes, ff_allocation, ff_remaining)
    print_results("Best Fit", blocks, processes, bf_allocation, bf_remaining)
    print_results("Worst Fit", blocks, processes, wf_allocation, wf_remaining)


if __name__ == "__main__":
    main()