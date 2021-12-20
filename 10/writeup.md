Challenge 10 - Packets delivery
===============================

The challenge provides [a pcap](https://codechallenge.0x14.net/resources/icmps.pcap) file that represents a piece of intercepted network traffic.

The .pcap file can transformed to plain text using a number of tools, the most famous of which are [Wireshark and tcpdump](https://serverfault.com/a/38632/85448).

Using tcpdump, the following command will do (note that you may need to use `sudo`):

```shell
tcpdump -qns 0 -X -r icmps.pcap > icmps.txt
```

The output saved to `icmps.txt` looks like this:

```
14:59:31.802161 IP 127.0.0.1 > 127.0.0.1: ICMP echo request, id 87, seq 137, length 9
	0x0000:  4500 001d 0001 0000 4001 7cdd 7f00 0001  E.......@.|.....
	0x0010:  7f00 0001 0800 e71f 0057 0089 10         .........W...
14:59:31.803833 IP 127.0.0.1 > 127.0.0.1: ICMP echo request, id 104, seq 195, length 9
	0x0000:  4500 001d 0001 0000 4001 7cdd 7f00 0001  E.......@.|.....
	0x0010:  7f00 0001 0800 75d4 0068 00c3 81         ......u..h...
14:59:31.804761 IP 127.0.0.1 > 127.0.0.1: ICMP echo request, id 97, seq 96, length 9
	0x0000:  4500 001d 0001 0000 4001 7cdd 7f00 0001  E.......@.|.....
	0x0010:  7f00 0001 0800 a03e 0061 0060 57         .......>.a.`W
14:59:31.805735 IP 127.0.0.1 > 127.0.0.1: ICMP echo request, id 116, seq 20, length 9
	0x0000:  4500 001d 0001 0000 4001 7cdd 7f00 0001  E.......@.|.....
	0x0010:  7f00 0001 0800 da77 0074 0014 1d         .......w.t...

...full output trimmed
```

Analyzing the hex data, we can notice the following:

- there are 213 records
- each record is 29 bytes in length

Looking more deeply into the data, here's what we can say about each of the 29 bytes (bytes positions are 0-based):

- bytes 0-21, 24, 26: all have constant values, so they probably encode some metadata (ex: the 127.0.0.1 IP address) and are not interesting for our purposes

- byte 22: min=2 max=255 distinct=109
- byte 23: min=0 max=255 distinct=145
- byte 25: **min=32 max=121** distinct=22 (**interesting!** - all characters are printable!)
- byte 27: min=1 max=213 distinct=213 (equivalent to the seq value)
- byte 28: min=0 max=255 distinct=103

Noticing that all bytes at position 25 contains printable characters, we can try to display them. Perhaps not surprisingly, a message is there, suggesting that the data is not in the right order and needs to be sorted by something else:

> What a mess, you will need to reorder everything to get the priceWhat a mess, you will need to reorder everything to get the priceWhat a mess, you will need to reorder everything to get the priceWhat a mess, you w

Looking again at the "interesting" bytes, it seems that byte 27 (the one equal to the `seq` field) is a good candidate for the sorting key, as it contains 213 consecutive and distinct values, exactly as many as there are records.

OK, so let's sort the records by the 27th byte (or the metadata `seq` field, which is equivalent) and have a new look at all "interesting" data in the new order.
Here I'm using Python, and I have all the .pcap information loaded into the `records` list, each item containing the raw bytes in a list named `.data`, and the other metadata in fields `id`, `seq`, etc.

```python
records = list(sorted(records, key=lambda x: x.seq))
for i in [22, 23, 27, 28]:
    print(f"\nByte {i}:")
    print("".join([chr(r.data[i]) for r in records]))
```

Looking at the output, something looks suspicious about the information contained in the bytes at position 28:

```
(previous output removed for brevity)

Byte 28:
PNG

IHDR~èZ¢IDATxnÿh|n  ðÈ5 Ã ¸à8»(àÿÿÓïø]×?ØÛWuð@q³íJ
                                                        4R°øÑÜÎ:[ã¸àZ
üÇÓÑ¤ð                                                               cÃð
5ÞÆkèIEND®B`+|,YÈÙX?ðEõí98ZÍØ¯­
```

It seems to contain a [PNG Image Header](https://en.wikipedia.org/wiki/Portable_Network_Graphics#File_header), so let's try to save this binary information in a separate file:

```python
pngBytes = [r.data[28] for r in records]
with open("./secret.png", "wb") as pngf:
    pngf.write((''.join(chr(i) for i in pngBytes)).encode('charmap'))
```

Then, let's open the secret.png file. Surprise! It's a QR code:

![Secret QR Code](./secret.png)

Read this with a QR Code reader of your choice and it will reveal the secret password that solves the challenge:

> KFXSMGTAJ9KT20

