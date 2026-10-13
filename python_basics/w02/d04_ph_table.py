#用 for 循环，把 pH 从 1 打印到 14， 每一行显示 pH 值和它的酸碱性
for pH in range(1, 15):
    if pH < 7:
        print(f"pH值: {pH} → 酸性")
    elif pH == 7:
        print(f"pH值: {pH} → 中性")
    else:
        print(f"pH值: {pH} → 碱性")  