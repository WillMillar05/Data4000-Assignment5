# inventory spotcheck using API 

import requests

# compute seed for student 

def compute_seed(student_key: str) -> int:
    return sum(ord(ch) for ch in student_key.strip())

# ask user for a valid interger >= 0

def prompt_on_hand() -> int:
    while True:
        raw = input("On hand: ")
        try:
            value = int(raw)
            if value < 0:
                print("Invalid on hand. Enter an integer greater than or equal to 0.")
                continue
            return value
        except ValueError:
            print("Invalid on hand. Enter a valid integer.")


def threshold_from_seed(seed: int) -> int:
    remainder = seed % 3
    if remainder == 0:
        return 15
    if remainder == 1:
        return 12
    return 9

# weezer(even) or Drake (odd) 
def run_spotcheck(seed: int) -> tuple[str, str, int | None]:
   
    term = "weezer" if seed % 2 == 0 else "drake"
    url = "https://itunes.apple.com/search"
    params = {"limit": 5, "term": term}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return term, "FAILED", None

    try:
        data = response.json()
    except ValueError:
        return term, "INVALID_RESPONSE", None

    if not isinstance(data, dict):
        return term, "INVALID_RESPONSE", None

    results = data.get("results")
    if not isinstance(results, list):
        return term, "INVALID_RESPONSE", None

    song_count = 0
    for item in results:
        if not isinstance(item, dict):
            return term, "INVALID_RESPONSE", None
        if item.get("kind") == "song":
            song_count += 1

    return term, "OK", song_count

# user input SKU # --> When done type "DONE" to break
def main() -> None:
    student_key = input("Student key: ")
    seed = compute_seed(student_key)

    threshold = threshold_from_seed(seed)
    total_skus = 0
    reorder_count = 0

    while True:
        sku = input("SKU: ").strip()

        if sku.upper() == "DONE":
            break

        if sku == "":
            print("Invalid SKU. Please enter a non-blank SKU.")
            continue

        on_hand = prompt_on_hand()
        total_skus += 1

        if on_hand < threshold:
            reorder_count += 1

    term, api_status, song_count = run_spotcheck(seed)

    songs_display = str(song_count) if api_status == "OK" else "N/A"

    print(f"Seed: {seed}")
    print(f"Threshold: {threshold}")
    print(f"SKUs entered: {total_skus}")
    print(f"Reorder flagged: {reorder_count}")
    print(f"Spotcheck term: {term}")
    print(f"Songs returned: {songs_display}")
    print(f"API status: {api_status}")


if __name__ == "__main__":
    main()