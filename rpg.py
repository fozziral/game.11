import random
import time

# =========================
# DATA PEMAIN
# =========================
player = {
    "name": "",
    "level": 1,
    "hp": 100,
    "max_hp": 100,
    "attack": 15,
    "defense": 5,
    "exp": 0,
    "gold": 50,
    "potion": 3,
    "weapon": "Pedang Kayu"
}

weapons = {
    "Pedang Kayu": {"attack": 0, "price": 0},
    "Pedang Besi": {"attack": 10, "price": 50},
    "Pedang Api": {"attack": 25, "price": 120},
    "katana cahaya": {"attack": 50, "price": 200}     
}

monsters = [
    {"name": "Slime", "hp": 40, "attack": 8, "defense": 2, "exp": 20, "gold": 15},
    {"name": "Goblin", "hp": 60, "attack": 12, "defense": 4, "exp": 30, "gold": 25},
    {"name": "Orc", "hp": 90, "attack": 16, "defense": 7, "exp": 45, "gold": 40},
    {"name": "monster", "hp": 250, "attack": 32, "defense": 7, "exp": 410000, "gold": 100}
]


# =========================
# FUNGSI BANTUAN
# =========================
def slow_print(text):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.01)
    print()


def pause():
    input("\nTekan ENTER untuk melanjutkan...")


def player_attack():
    weapon_bonus = weapons[player["weapon"]]["attack"]
    return player["attack"] + weapon_bonus


def show_status():
    print("\n========== STATUS ==========")
    print(f"Nama     : {player['name']}")
    print(f"Level    : {player['level']}")
    print(f"HP       : {player['hp']}/{player['max_hp']}")
    print(f"Attack   : {player_attack()}")
    print(f"Defense  : {player['defense']}")
    print(f"EXP      : {player['exp']}/{player['level'] * 50}")
    print(f"Gold     : {player['gold']}")
    print(f"Potion   : {player['potion']}")
    print(f"Senjata  : {player['weapon']}")
    print("============================")


# =========================
# LEVEL UP
# =========================
def check_level_up():
    required_exp = player["level"] * 50

    while player["exp"] >= required_exp:
        player["exp"] -= required_exp
        player["level"] += 1

        player["max_hp"] += 20
        player["hp"] = player["max_hp"]
        player["attack"] += 5
        player["defense"] += 2

        slow_print("\n⭐ LEVEL UP!")
        slow_print(f"Kamu sekarang Level {player['level']}!")
        slow_print("+20 Max HP")
        slow_print("+5 Attack")
        slow_print("+2 Defense")

        required_exp = player["level"] * 50


# =========================
# PERTARUNGAN
# =========================
def battle(monster):
    enemy = monster.copy()

    print("\n============================")
    print(f"⚔️  MUSUH: {enemy['name']}")
    print("============================")

    while enemy["hp"] > 0 and player["hp"] > 0:
        print(f"\n❤️ HP Kamu    : {player['hp']}/{player['max_hp']}")
        print(f"👹 HP {enemy['name']}: {enemy['hp']}")

        print("\n1. Serang")
        print("2. Gunakan Potion")
        print("3. Kabur")

        choice = input("\nPilih: ")

        # SERANG
        if choice == "1":
            damage = max(1, player_attack() - enemy["defense"])
            
            # Critical hit
            if random.randint(1, 10) == 10:
                damage *= 2
                slow_print("💥 CRITICAL HIT!")

            enemy["hp"] -= damage
            slow_print(f"⚔️ Kamu memberikan {damage} damage!")

            if enemy["hp"] <= 0:
                slow_print(f"\n🎉 Kamu mengalahkan {enemy['name']}!")
                slow_print(f"⭐ EXP +{enemy['exp']}")
                slow_print(f"💰 Gold +{enemy['gold']}")

                player["exp"] += enemy["exp"]
                player["gold"] += enemy["gold"]

                check_level_up()
                return True

        # POTION
        elif choice == "2":
            if player["potion"] <= 0:
                print("❌ Potion kamu habis!")
                continue

            heal = 30
            old_hp = player["hp"]

            player["hp"] = min(player["max_hp"], player["hp"] + heal)
            player["potion"] -= 1

            slow_print(
                f"🧪 HP pulih {player['hp'] - old_hp}!"
            )

        # KABUR
        elif choice == "3":
            if random.randint(1, 2) == 1:
                slow_print("🏃 Kamu berhasil kabur!")
                return False
            else:
                slow_print("❌ Gagal kabur!")

        else:
            print("❌ Pilihan tidak valid!")
            continue

        # SERANGAN MUSUH
        if enemy["hp"] > 0:
            damage = max(
                1,
                enemy["attack"] - player["defense"] +
                random.randint(-2, 3)
            )

            player["hp"] -= damage

            slow_print(
                f"👹 {enemy['name']} menyerang dan memberikan "
                f"{damage} damage!"
            )

    if player["hp"] <= 0:
        player["hp"] = 0
        slow_print("\n💀 Kamu kalah...")
        return False


# =========================
# TOKO
# =========================
def shop():
    while True:
        print("\n========== TOKO ==========")
        print(f"💰 Gold kamu: {player['gold']}")

        print("\n1. Potion - 20 Gold")
        print("2. Pedang Besi - 50 Gold")
        print("3. Pedang Api - 120 Gold")
        print("4. Keluar")

        choice = input("\nPilih: ")

        if choice == "1":
            if player["gold"] >= 20:
                player["gold"] -= 20
                player["potion"] += 1
                print("🧪 Kamu membeli 1 Potion!")
            else:
                print("❌ Gold tidak cukup!")

        elif choice == "2":
            if player["weapon"] == "Pedang Besi":
                print("Kamu sudah memiliki Pedang Besi.")
            elif player["gold"] >= 50:
                player["gold"] -= 50
                player["weapon"] = "Pedang Besi"
                print("🗡️ Kamu membeli Pedang Besi!")
            else:
                print("❌ Gold tidak cukup!")

        elif choice == "3":
            if player["weapon"] == "Pedang Api":
                print("Kamu sudah memiliki Pedang Api.")
            elif player["gold"] >= 120:
                player["gold"] -= 120
                player["weapon"] = "Pedang Api"
                print("🔥 Kamu membeli Pedang Api!")
            else:
                print("❌ Gold tidak cukup!")

        elif choice == "4":
            break

        else:
            print("❌ Pilihan tidak valid!")


# =========================
# BOSS
# =========================
def boss_battle():
    boss = {
        "name": "🐉 Naga Kegelapan",
        "hp": 200,
        "attack": 25,
        "defense": 10,
        "exp": 150,
        "gold": 200
    }

    slow_print("\n🐉 BOSS MUNCUL!")
    slow_print("Naga Kegelapan menghadang perjalananmu!")

    return battle(boss)


# =========================
# GAME UTAMA
# =========================
def main():
    print("""
====================================
        ⚔️ RPG PETUALANGAN ⚔️
====================================
    """)

    player["name"] = input("Masukkan nama pahlawan: ")

    slow_print(
        f"\nSelamat datang, {player['name']}!"
    )

    slow_print(
        "Kerajaan sedang diserang monster."
    )

    slow_print(
        "Kalahkan monster dan hadapi Naga Kegelapan!"
    )

    while True:
        print("\n========== MENU ==========")
        print("1. Jelajah")
        print("2. Status")
        print("3. Toko")
        print("4. Keluar")

        choice = input("\nPilih: ")

        # JELAJAH
        if choice == "1":
            print("\n🌲 Kamu menjelajahi hutan...")

            event = random.randint(1, 10)

            if event <= 7:
                monster = random.choice(monsters)
                battle(monster)

            elif event == 8:
                gold_found = random.randint(10, 30)
                player["gold"] += gold_found

                slow_print(
                    f"💰 Kamu menemukan {gold_found} Gold!"
                )

            elif event == 9:
                potion_found = 1
                player["potion"] += potion_found

                slow_print("🧪 Kamu menemukan 1 Potion!")

            else:
                print("\n🐉 Kamu menemukan Naga Kegelapan!")

                if player["level"] >= 3:
                    victory = boss_battle()

                    if victory:
                        print("\n" + "=" * 40)
                        print("🏆 SELAMAT!")
                        print("Kamu mengalahkan Naga Kegelapan!")
                        print("🎉 KERAJAAN BERHASIL DISELAMATKAN!")
                        print("=" * 40)
                        break
                else:
                    print(
                        "❌ Kamu terlalu lemah untuk melawan Boss!"
                    )
                    print("Naikkan level minimal ke Level 3.")

            if player["hp"] <= 0:
                print("\n💀 GAME OVER")
                break

        # STATUS
        elif choice == "2":
            show_status()
            pause()

        # TOKO
        elif choice == "3":
            shop()

        # KELUAR
        elif choice == "4":
            print("\n👋 Terima kasih sudah bermain!")
            break

        else:
            print("❌ Pilihan tidak valid!")


# =========================
# JALANKAN GAME
# =========================
if __name__ == "__main__":
    main()
