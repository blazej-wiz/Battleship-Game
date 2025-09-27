import tkinter as tk
from tkinter import messagebox
from src.game import Game

# === Setup Game Engine ===
fleet_template = [
    ('Carrier', 5), ('Battleship', 4),
    ('Cruiser', 3), ('Submarine', 3), ('Destroyer', 2)
]
game = Game("Player 1", "Player 2", fleet_template[:], fleet_template[:])

# === Tkinter Setup ===
root = tk.Tk()
root.title("Battleship")

buttons_p1 = {}
buttons_p2 = {}

placement_phase = True
placing_player = 1
orientation = "horizontal"

# ---------- Helpers ----------

def current_player_name():
    return game.player1_name if game.current_player == 1 else game.player2_name

def remaining_fleet(player):
    return game.fleet1 if player == 1 else game.fleet2

def next_ship_tuple(player):
    fl = remaining_fleet(player)
    return fl[0] if fl else None

def coord_from_rc(r, c):
    return game.board_p1.columns[c] + game.board_p1.rows[r]

def update_next_ship_label():
    nxt = next_ship_tuple(placing_player)
    if placement_phase:
        if nxt:
            ship_name, length = nxt
            next_ship_lbl.config(
                text=f"{('P1' if placing_player==1 else 'P2')}: Place {ship_name} (len {length})"
            )
        else:
            next_ship_lbl.config(text=f"{('P1' if placing_player==1 else 'P2')}: All ships placed")
    else:
        next_ship_lbl.config(text="Battle phase")

def privacy_screen(message, after_close=None):
    """Modal cover so the other player can't peek."""
    cover = tk.Toplevel(root)
    cover.title("Pass the device")
    cover.attributes("-topmost", True)
    cover.grab_set()

    msg = tk.Label(cover, text=message, font=("Arial", 14), padx=20, pady=20)
    msg.pack()

    def close_and_call():
        cover.destroy()
        if after_close:
            after_close()

    btn = tk.Button(cover, text="Continue", width=18, command=close_and_call)
    btn.pack(pady=10)

    cover.update_idletasks()
    w = cover.winfo_width()
    h = cover.winfo_height()
    sw = cover.winfo_screenwidth()
    sh = cover.winfo_screenheight()
    cover.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    cover.wait_window()

def update_boards():
    for player, buttons in [(1, buttons_p1), (2, buttons_p2)]:
        grid = game.get_board(player)
        for r in range(game.board_p1.size):
            for c in range(game.board_p1.size):
                cell = grid[r][c]
                display_symbol = "."

                if game.phase == "placement":
                    if player == game.current_player:
                        display_symbol = cell
                elif game.phase == "battle":
                    # Battle phase: NO ships are visible, only hits/misses
                    if cell in ["X", "O"]:
                        display_symbol = cell

                buttons[(r, c)]["text"] = display_symbol


def start_battle_phase():
    global placement_phase
    placement_phase = False
    game.phase = "battle"
    game.current_player = 1
    turn_label.config(text=f"{current_player_name()}'s Turn")
    next_ship_lbl.config(text="Battle phase")
    update_boards()
    messagebox.showinfo("Battle Start", f"{game.player1_name} begins!")

def toggle_orientation():
    global orientation
    orientation = "vertical" if orientation == "horizontal" else "horizontal"
    orientation_label.config(text=f"Orientation: {orientation.capitalize()}")

# ---------- Click Handlers ----------

def handle_click_p1(r, c):
    handle_click(r, c, 1)

def handle_click_p2(r, c):
    handle_click(r, c, 2)

def handle_click(r, c, board_num):
    global placing_player

    coord = coord_from_rc(r, c)

    if placement_phase:
        if board_num != placing_player:
            messagebox.showwarning("Not your board", "Click your own board to place ships.")
            return

        nxt = next_ship_tuple(placing_player)
        if not nxt:
            return

        ship_name, length = nxt
        success = game.place_ship(placing_player, ship_name, length, coord, orientation)

        if success:
            update_boards()
            if len(remaining_fleet(placing_player)) == 0:
                if placing_player == 1:
                    placing_player = 2
                    game.current_player = 2
                    update_boards()  # immediately hide P1 ships
                    update_next_ship_label()
                    privacy_screen(
                        f"{game.player2_name}, it's your turn to place.\nClick Continue when ready.",
                        after_close=update_boards
                    )
                    turn_label.config(text=f"{game.player2_name}: Place your fleet")
                else:
                    update_next_ship_label()
                    privacy_screen(
                        "Placement finished.\nClick Continue to start the battle!",
                        after_close=start_battle_phase
                    )
            else:
                update_next_ship_label()
        else:
            messagebox.showwarning("Invalid", "Invalid placement (overlap/out of bounds).")
    else:
        if board_num == game.current_player:
            messagebox.showwarning("Invalid", "You cannot fire at your own board!")
            return

        result = game.fire(game.current_player, coord)
        messagebox.showinfo("Result", f"{current_player_name()} fired at {coord}: {result}")
        update_boards()

        winner = game.is_game_over()
        if winner != 0:
            winner_name = game.player1_name if winner == 1 else game.player2_name
            messagebox.showinfo("Game Over", f"{winner_name} wins!")
            root.quit()
            return

        game.switch_turn()
        update_boards()
        turn_label.config(text=f"{current_player_name()}'s Turn")

# ---------- Layout ----------

turn_label = tk.Label(root, text=f"{game.player1_name}: Place your fleet", font=("Arial", 16))
turn_label.grid(row=0, column=0, columnspan=2, pady=(6, 0))

orientation_btn = tk.Button(root, text="Toggle Orientation (H/V)", command=toggle_orientation)
orientation_btn.grid(row=1, column=0, columnspan=2, pady=4)

orientation_label = tk.Label(root, text=f"Orientation: {orientation.capitalize()}")
orientation_label.grid(row=2, column=0, columnspan=2, pady=(0, 6))

next_ship_lbl = tk.Label(root, text="", font=("Arial", 12))
next_ship_lbl.grid(row=3, column=0, columnspan=2, pady=(0, 6))

frame_p1 = tk.Frame(root, padx=10, pady=10, borderwidth=2, relief="groove")
frame_p1.grid(row=4, column=0, padx=(8, 4), pady=(4, 8), sticky="n")

label_p1 = tk.Label(frame_p1, text="Player 1 Board")
label_p1.grid(row=0, column=0, columnspan=10)

for r in range(10):
    for c in range(10):
        btn = tk.Button(frame_p1, text=".", width=3, height=1, command=lambda r=r, c=c: handle_click_p1(r, c))
        btn.grid(row=r+1, column=c)
        buttons_p1[(r, c)] = btn

frame_p2 = tk.Frame(root, padx=10, pady=10, borderwidth=2, relief="groove")
frame_p2.grid(row=4, column=1, padx=(4, 8), pady=(4, 8), sticky="n")

label_p2 = tk.Label(frame_p2, text="Player 2 Board")
label_p2.grid(row=0, column=0, columnspan=10)

for r in range(10):
    for c in range(10):
        btn = tk.Button(frame_p2, text=".", width=3, height=1, command=lambda r=r, c=c: handle_click_p2(r, c))
        btn.grid(row=r+1, column=c)
        buttons_p2[(r, c)] = btn

# Initialize
game.phase = "placement"
update_boards()
update_next_ship_label()

root.mainloop()
