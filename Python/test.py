mantissa_pos = 1
s = "1.1010101001010011010111010011110100001100000000000010".replace(".","") # len 53
pos = mantissa_pos + 53

if len(s)<pos:
    for _ in range(pos-len(s) ):
        s+="0"

l = list(s)
l.insert(pos,".")

print("".join(l))