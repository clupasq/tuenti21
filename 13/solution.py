import codecs
from rich import print
from string import ascii_uppercase
import time

def get_user_and_password():
    print(codecs.encode('plyba', 'rot_13'))
    print(codecs.encode('xvyy_nyy_uhznaf', 'rot_13'))

# xxd -r here-is-the-position herebin
# cat herebin | gunzip > text
# xxd text # wow, some nasty chars in there.

# bs = None
# with open("./text", "rb") as f:
#     bs = f.read()
# for b in bs:
#     print(b)

text = None
with open("./text", "r", encoding="utf8") as f:
    text = f.read()

weird = []
for i, c in enumerate(text):
    if ord(c) > 255 and c < "\u2019":
        weird.append((i, ord(c)))

text = text.replace("\u200b", "\u2592")
text = text.replace("\u200c", "\u2593")
# text = text.replace("\u2019", "#")

print(text)

# print(weird)

binary = [""]
for i, w in weird:
    # print(i)
    # if w == 8217:
    #     binary.append("0")
        # binary[-1] += "-"
    if w == 8203:
        binary[-1] += "1"
    elif w == 8204:
        binary[-1] += "0"
    else:
        raise Exception("NOT EXPECTED!")

print(len(weird))

print(binary)
for b in binary:
    x = int(b, 2)
    if x < 26:
        print(chr(x + 64))
    print(x, len(str(x)))
    # print(time.gmtime(x / 1000000))

b = binary[0]

print("===============")



solution = "TODO"

with open("./output.txt", "w") as f:
    f.write(solution)
    f.write("\n")
# print(425318713386023)
