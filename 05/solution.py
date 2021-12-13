

bs = []
with open("./Invictus.txt", "rb") as f:
    while (byte := f.read(1)):
        bs.append(byte)


weird = b""
prev = None
for b in bs:
    i = int.from_bytes(b, byteorder='big')
    if i > 127:
        weird += b

print(weird)

print(weird.decode("utf-32"), )

# for i, w in enumerate(weird):
#     print(w, end = " ")
#     if i % 4 == 3:
#         print()

