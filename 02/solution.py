# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201

def read_int():
    return int(input())

def read_int_array():
    return [int(ss) for ss in input().split()]

def reverse_str(s):
    return "".join(reversed(s))

def indexof(needle, haystack):
    try:
        return haystack.indexof(needle)
    except ValueError:
        return None

def solution(n, r, c, pokems, board):
    text = "".join(board)
    safe = False
    pokems = set(pokems)
    while not safe:
        safe = True
        for pok in pokems:
            l = len(text)
            text = text.replace(pok, "")
            if len(text) < l:
                safe = False
                break
            rpok = reverse_str(pok)
            text = text.replace(rpok, "")
            if len(text) < l:
                safe = False
                break
    return text

def main():
    t = read_int()

    for i in range(t):
        n, r, c = read_int_array()
        pokems = [input().strip() for _ in range(n)]
        board = [input().strip().replace(" ", "")
                for _ in range(r)]
        s = solution(n, r, c, pokems, board)
        print(f"Case #{ i + 1 }: {s}")

if __name__ == "__main__":
    main()
