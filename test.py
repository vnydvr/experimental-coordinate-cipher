from decimal import Decimal, getcontext
import math

# ================== ИНСТРУКЦИЯ ===============
INSTRUCTION_TEXT = """
====================================================
        IRRATIONAL CIPHER — КРАТКАЯ ИНСТРУКЦИЯ
====================================================

Это консольная программа для скрытого обмена сообщениями.
Сообщения НЕ передаются напрямую — вместо них передаются
числа (позиции), по которым сообщение восстанавливается
на стороне собеседника.

----------------------------------------------------
ОБЩИЙ ПРИНЦИП РАБОТЫ
----------------------------------------------------
1. Один человек создаёт ключ и отправляет его собеседнику.
2. Второй человек вводит этот ключ.
3. Далее общение идёт по очереди:
   - один принимает сообщение
   - другой отправляет
   - затем роли меняются
4. После КАЖДОГО сообщения используется новое число,
   поэтому одинаковые сообщения никогда не выглядят одинаково.

----------------------------------------------------
КАК НАЧАТЬ
----------------------------------------------------
При запуске выберите:
1 — если вы создаёте ключ (вы отправляете сообщение первым)

* если вы НЕ ЗНАЕТЕ что делают отдельные строки в ключе:
пропишите ЛЮБЫЕ значения, соответствующие условиям в скобках

2 — если вы получили ключ (вы принимаете сообщение первым)

----------------------------------------------------
КОМАНДЫ
----------------------------------------------------
reset — экстренный сброс состояния
exit  — выход из программы

====================================================
"""
print(INSTRUCTION_TEXT)
input('Нажмите Enter для продолжения...')

# ================== АЛФАВИТ ==================
CHAR_TO_CODE = {}

# a-z → 01–26
for i, c in enumerate("abcdefghijklmnopqrstuvwxyz", start=1):
    CHAR_TO_CODE[c] = f"{i:02d}"

# пробел2
CHAR_TO_CODE[" "] = "27"

# 0–9 → 28–37
for i, c in enumerate("0123456789", start=28):
    CHAR_TO_CODE[c] = f"{i:02d}"

# спецсимволы → 38–44
SPECIAL = ".,?!:-\'"
for i, c in enumerate(SPECIAL, start=38):
    CHAR_TO_CODE[c] = f"{i:02d}"

CODE_TO_CHAR = {v: k for k, v in CHAR_TO_CODE.items()}

SUPPORTED_CHARS_HINT = "a-z 0-9 пробел . , ? ! : - \'"

# ================== КОДИРОВАНИЕ ==================
def encode_text(text):
    text = text.lower()
    filtered = [c for c in text if c in CHAR_TO_CODE]
    if len(filtered) % 2 == 1:
        filtered.append(" ")
    return [
        CHAR_TO_CODE[filtered[i]] + CHAR_TO_CODE[filtered[i+1]]
        for i in range(0, len(filtered), 2)
    ]


def decode_blocks(blocks):
    out = ""
    for b in blocks:
        out += CODE_TO_CHAR.get(b[:2], "?")
        out += CODE_TO_CHAR.get(b[2:], "?")
    return out.rstrip()

# ================== МАТЕМАТИКА ==================
def sqrt_digits(n, precision):
    getcontext().prec = precision + 5
    s = str(Decimal(n).sqrt())
    return s.split(".")[1][:precision].ljust(precision, "0")

# ================== ПРОВЕРКА КОРНЕЙ ==================
def is_perfect_square(n):
    r = math.isqrt(n)
    return r * r == n

def skip_perfect_square(n):
    while is_perfect_square(n):
        n += 1
    return n

# ================== КЛЮЧ ==================
def key_encode(start, precision, jump):
    return (
        f"{len(str(start)):X}{start}"
        f"{len(str(precision)):X}{precision}"
        f"{len(str(jump)):X}{jump}"
    )

def key_decod(key):
    l1 = int(key[0], 16)
    start = int(key[1:1+l1])

    l2 = int(key[1+l1], 16)
    precision = int(key[2+l1:2+l1+l2])

    l3 = int(key[2+l1+l2], 16)
    jump = int(key[3+l1+l2:3+l1+l2+l3])

    return start, precision, jump

# ================== СЕССИЯ ==================
class Session:
    def __init__(self, start, precision, jump, recv_first):
        self.start = start
        self.precision = precision
        self.jump = jump
        self.index = 0

        self.initial_recv_first = recv_first  # ← НОВОЕ
        self.waiting_receive = recv_first

    def reset(self):
        self.index = 0
        self.waiting_receive = self.initial_recv_first  # ← ИСПРАВЛЕНО

    def root(self):
        base = self.start + self.jump * self.index
        return skip_perfect_square(base)

    def advance(self):
        self.index += 1
        self.waiting_receive = not self.waiting_receive

# ================== ПОИСК ==================
def find_blocks(digits, blocks):
    positions = []
    cursor = 0
    for b in blocks:
        idx = digits.find(b, cursor)
        if idx == -1:
            return None
        positions.append(idx + 1)
        cursor = idx + len(b)
    return positions

def extract_blocks(digits, positions):
    return [digits[p-1:p+3] for p in positions]

# ================== CLI ==================
def main():
    print("Irrational Cipher CLI\n")
    print("1) Создать ключ (вы отправляете сообщение первым)")
    print("2) Ввести ключ (вы принимаете сообщение первым)")
    mode = input("> ").strip()

    if mode == "1":
        start = int(input("Стартовое подкоренное число (до 16-ти символов в длину): "))
        precision = int(input("Точность (до 16-ти символов в длину,300000 — быстро, 500000 — сбалансировано, 1000000 — медленно): "))
        jump = int(input("Шаг (до 16-ти символов в длину): "))
        key = key_encode(start, precision, jump)
        print("\nКЛЮЧ:\n", key, "\n")
        session = Session(start, precision, jump, recv_first=False)
    else:
        key = input("Введите ключ: ")
        start, precision, jump = key_decod(key)
        session = Session(start, precision, jump, recv_first=True)

    print("\nКоманды: reset / exit")
    print("при рассинхронизации(отсутствии смысла в сообщениях) - пропиши reset.\n")

    while True:
        if session.waiting_receive:
            print("[ПРИЁМ]")
            print("Вставьте строку позиций (через пробел):")
            raw = input("> ").strip().lower()
            if raw == "exit":
                return
            if raw == "reset":
                session.reset()
                print("Сброс\n")
                continue

            try:
                positions = list(map(int, raw.split()))
            except ValueError:
                print("Ошибка ввода\n")
                continue

            digits = sqrt_digits(session.root(), session.precision)
            blocks = extract_blocks(digits, positions)
            print("\nПОЛУЧЕНО:")
            print(decode_blocks(blocks), "\n")
            session.advance()

        else:
            print("[ОТПРАВКА]")
            print("Поддерживаемые символы:", SUPPORTED_CHARS_HINT)
            text = input("> ").strip().lower()
            if text == "exit":
                return
            if text == "reset":
                session.reset()
                print("Сброс\n")
                continue

            blocks = encode_text(text)
            digits = sqrt_digits(session.root(), session.precision)
            positions = find_blocks(digits, blocks)

            if positions is None:
                print("Не удалось закодировать сообщение\n")
                continue

            print("\nОТПРАВЬТЕ:")
            print(" ".join(map(str, positions)), "\n")
            session.advance()

if __name__ == "__main__":
    main()
