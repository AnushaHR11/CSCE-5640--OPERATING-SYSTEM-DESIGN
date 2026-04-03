def translate_address(logical_space_size, page_size, logical_address):
    if page_size <= 0:
        print("Error: Page size must be greater than 0.")
        return

    if logical_space_size <= 0:
        print("Error: Logical address space size must be greater than 0.")
        return

    num_pages = logical_space_size // page_size

    if logical_space_size % page_size != 0:
        num_pages += 1

    if logical_address < 0 or logical_address >= logical_space_size:
        print(f"Invalid logical address: {logical_address}")
        print("Error: Address is outside the logical address space.")
        return

    page_number = logical_address // page_size
    offset = logical_address % page_size

    if page_number >= num_pages:
        print(f"Invalid page reference: Page {page_number} does not exist.")
        return

    frame_number = page_number

    physical_address = frame_number * page_size + offset

    print(f"Logical address {logical_address} maps to page {page_number}, offset {offset}.")
    print(f"Physical address: Frame {frame_number}, offset {offset}.")
    print(f"Physical address value: {physical_address}")


def main():
    logical_space_size = int(input("Enter logical address space size: "))
    page_size = int(input("Enter page size: "))
    logical_address = int(input("Enter logical address: "))

    translate_address(logical_space_size, page_size, logical_address)


if __name__ == "__main__":
    main()