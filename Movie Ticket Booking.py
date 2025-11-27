
"""
Simple Movie Ticket Booking CLI
Save as: movie_booking.py
Run: python movie_booking.py
"""

import json
import os
import uuid
from datetime import datetime

DATA_DIR = "movie_data"
SHOWS_FILE = os.path.join(DATA_DIR, "shows.json")
BOOKINGS_FILE = os.path.join(DATA_DIR, "bookings.json")


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, content):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)


def default_shows():
    
    return [
        {
            "show_id": "S1",
            "title": "The Great Adventure",
            "time": "2025-11-26 18:00",
            "price": 150.0,
            "rows": 5,
            "cols": 8,
            # seats 0 = available, 1 = booked
            "seats": [[0]*8 for _ in range(5)]
        },
        {
            "show_id": "S2",
            "title": "Romance in Python",
            "time": "2025-11-26 20:30",
            "price": 180.0,
            "rows": 6,
            "cols": 7,
            "seats": [[0]*7 for _ in range(6)]
        }
    ]

def init_data():
    ensure_data_dir()
    shows = load_json(SHOWS_FILE, None)
    bookings = load_json(BOOKINGS_FILE, None)
    if shows is None:
        shows = default_shows()
       
        save_json(SHOWS_FILE, shows)
    if bookings is None:
        bookings = []
        save_json(BOOKINGS_FILE, bookings)
    return shows, bookings
    
def find_show(shows, show_id):
    for s in shows:
        if s["show_id"] == show_id:
            return s
    return None

def seat_label(row, col):
    # Row 0 -> A, etc. Columns 0 -> 1
    return f"{chr(ord('A') + row)}{col+1}"

def parse_seat_label(label):
    # Accepts like A1, B3
    label = label.strip().upper()
    if len(label) < 2:
        return None
    row_char = label[0]
    if not ('A' <= row_char <= 'Z'):
        return None
    try:
        col_num = int(label[1:])  # 1-based
    except ValueError:
        return None
    row = ord(row_char) - ord('A')
    col = col_num - 1
    return row, col

def print_seat_map(show):
    rows = show["rows"]
    cols = show["cols"]
    seats = show["seats"]
    
    header = "   " + " ".join(f"{c+1:>2}" for c in range(cols))
    print(header)
    for r in range(rows):
        row_label = chr(ord('A') + r)
        row_seats = []
        for c in range(cols):
            row_seats.append("X " if seats[r][c] == 1 else "O ")
        print(f"{row_label}  " + "".join(row_seats))
    print("O = available, X = booked")

def available_count(show):
    return sum(1 for r in show["seats"] for c in r if c == 0)
    
def book_seats(shows, bookings):
    print("\nAvailable shows:")
    for s in shows:
        print(f"{s['show_id']}: {s['title']} at {s['time']} — ₹{s['price']} — {available_count(s)} seats left")
    show_id = input("Enter show id to book (e.g. S1): ").strip()
    show = find_show(shows, show_id)
    if not show:
        print("Invalid show id.")
        return

    print("\nSeat map:")
    print_seat_map(show)
    print("Enter seats to book separated by commas (e.g. A1,A2).")
    seat_input = input("Seats: ").strip()
    raw = [s.strip() for s in seat_input.split(",") if s.strip()]
    if not raw:
        print("No seats entered.")
        return

    requested = []
    for lab in raw:
        parsed = parse_seat_label(lab)
        if not parsed:
            print(f"Invalid seat label: {lab}. Skipping.")
            continue
        r, c = parsed
        if r < 0 or r >= show["rows"] or c < 0 or c >= show["cols"]:
            print(f"Seat {lab} out of range. Skipping.")
            continue
        if show["seats"][r][c] == 1:
            print(f"Seat {lab} already booked. Skipping.")
            continue
        requested.append((r, c))

    if not requested:
        print("No valid seats to book (all skipped).")
        return

    total_price = len(requested) * show["price"]
    print(f"\nYou are booking {len(requested)} seats for '{show['title']}' at {show['time']}. Total = ₹{total_price}")
    confirm = input("Confirm booking? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Booking cancelled.")
        return

    for r, c in requested:
        show["seats"][r][c] = 1

    booking_id = str(uuid.uuid4())[:8].upper()
    booking = {
        "booking_id": booking_id,
        "show_id": show["show_id"],
        "title": show["title"],
        "time": show["time"],
        "seats": [seat_label(r, c) for r, c in requested],
        "amount": total_price,
        "created_at": datetime.now().isoformat()
    }
    bookings.append(booking)
    
    save_json(SHOWS_FILE, shows)
    save_json(BOOKINGS_FILE, bookings)
    print(f"\nBooking successful! Booking ID: {booking_id}")
    print("Seats:", ", ".join(booking["seats"]))

def cancel_booking(shows, bookings):
    bid = input("Enter booking ID to cancel: ").strip().upper()
    match = None
    for b in bookings:
        if b["booking_id"].upper() == bid:
            match = b
            break
    if not match:
        print("Booking ID not found.")
        return
    print("Booking found:")
    print(f"Show: {match['title']} at {match['time']}")
    print("Seats:", ", ".join(match["seats"]))
    confirm = input("Confirm cancel? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancellation aborted.")
        return

    show = find_show(shows, match["show_id"])
    if show:
        for seat_lab in match["seats"]:
            parsed = parse_seat_label(seat_lab)
            if parsed:
                r, c = parsed
                if 0 <= r < show["rows"] and 0 <= c < show["cols"]:
                    show["seats"][r][c] = 0
   
    bookings.remove(match)
    save_json(SHOWS_FILE, shows)
    save_json(BOOKINGS_FILE, bookings)
    print("Booking cancelled and seats freed.")

def view_bookings(bookings):
    if not bookings:
        print("No bookings found.")
        return
    print("\nCurrent bookings:")
    for b in bookings:
        print(f"- ID: {b['booking_id']}\n  Show: {b['title']} at {b['time']}\n  Seats: {', '.join(b['seats'])}\n  Amount: ₹{b['amount']}\n  Created: {b['created_at']}\n")

def view_show_map(shows):
    show_id = input("Enter show id to view seat map (e.g. S1): ").strip()
    show = find_show(shows, show_id)
    if not show:
        print("Invalid show id.")
        return
    print(f"\nSeat map for {show['title']} — {show['time']}:")
    print_seat_map(show)

def add_demo_show(shows, bookings):
    t = input("Movie title: ").strip()
    time = input("Show time (YYYY-MM-DD HH:MM): ").strip()
    try:
        price = float(input("Ticket price: ").strip())
        rows = int(input("Rows (e.g. 5): ").strip())
        cols = int(input("Cols (e.g. 8): ").strip())
    except Exception as e:
        print("Invalid number entered. Aborting.")
        return
    sid = f"S{len(shows)+1}"
    new = {
        "show_id": sid,
        "title": t,
        "time": time,
        "price": price,
        "rows": rows,
        "cols": cols,
        "seats": [[0]*cols for _ in range(rows)]
    }
    shows.append(new)
    save_json(SHOWS_FILE, shows)
    print(f"Added show {sid}.")

# --- Main loop --------------------------------------------------------------
def main():
    shows, bookings = init_data()

    MENU = """
Movie Ticket Booking
1. List shows
2. View seat map for a show
3. Book seats
4. Cancel booking
5. View my bookings
6. Add a new show (admin/demo)
0. Exit
"""
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "1":
            print("\nShows:")
            for s in shows:
                print(f"{s['show_id']}: {s['title']} at {s['time']} — ₹{s['price']} — {available_count(s)} seats available")
        elif choice == "2":
            view_show_map(shows)
        elif choice == "3":
            book_seats(shows, bookings)
        elif choice == "4":
            cancel_booking(shows, bookings)
        elif choice == "5":
            view_bookings(bookings)
        elif choice == "6":
            add_demo_show(shows, bookings)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
