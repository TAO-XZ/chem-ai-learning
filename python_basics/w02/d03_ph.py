#问用户一个 pH 值，然后判断并打印出 酸性 / 中性 / 碱性。
#pH < 7 → 酸性
#pH = 7 → 中性
#pH > 7 → 碱性
pH = float(input("请输入一个pH值："))
if pH < 7:
    print("酸性")
elif pH == 7:
    print("中性")
else:
    print("碱性")