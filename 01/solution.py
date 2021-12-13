# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201

def read_int():
    return int(input())

def read_int_array():
    return [int(ss) for ss in input().split()]

def solution(x, y):
    s = x + y
    if s == 12:
        return "-"
    return s + 1

def main():
    t = read_int()

    for i in range(t):
        x, y = [int(n) for n in input().strip().split(":")]
        s = solution(x, y)
        print(f"Case #{ i + 1 }: {s}")

if __name__ == "__main__":
    main()
