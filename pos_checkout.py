# checkout system for campus retail score 


def compute_seed(student_key: str) -> int:
   
    return sum(ord(ch) for ch in student_key.strip())

# ask for unit price > 0 --> if <=0 or not a number, ask again

def prompt_unit_price() -> float:
    while True:
        raw = input("Unit price: ")
        try:
            price = float(raw)
            if price <= 0:
                print("Invalid unit price. Enter a number greater than 0.")
                continue
            return price
        except ValueError:
            print("Invalid unit price. Enter a valid number.")

# ask for quantity >1 --> if <1 or not an integer, ask again

def prompt_quantity() -> int:
    while True:
        raw = input("Quantity: ")
        try:
            qty = int(raw)
            if qty < 1:
                print("Invalid quantity. Enter an integer greater than or equal to 1.")
                continue
            return qty
        except ValueError:
            print("Invalid quantity. Enter a valid integer.")

# When "DONE" enetered, loop breaks and calculates totals a quantity 
# Item can only be letters, not numeric 

def main() -> None:
    student_key = input("Student key: ")
    seed = compute_seed(student_key)

    subtotal = 0.0
    total_units = 0

    while True:
        item_name = input("Item name: ").strip()

        if item_name.upper() == "DONE":
            break

        if item_name == "":
            print("Item name cannot be empty.")
            continue

        if item_name.isdigit():
            print("Invalid item name. Use letters, not only numbers.")
            continue

        price = prompt_unit_price()
        quantity = prompt_quantity()

        subtotal += price * quantity
        total_units += quantity
# discounts 
    discount_percent = 10 if (total_units >= 10 or subtotal >= 100) else 0
    discount_amount = subtotal * (discount_percent / 100)
    total_after_discount = subtotal - discount_amount

    perk_applied = (seed % 2 == 1)
    if perk_applied:
        total_after_discount -= 3.00

    final_total = max(0.0, total_after_discount)

    print(f"Seed: {seed}")
    print(f"Units: {total_units}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Discount: {discount_percent}%")
    print(f"Perk applied: {'YES' if perk_applied else 'NO'}")
    print(f"Total: ${final_total:.2f}")


if __name__ == "__main__":
    main()