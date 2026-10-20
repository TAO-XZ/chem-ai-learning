# ======== 准备计数器 ========
ok = 0
bad = 0
total = 0

with open("data\messy_data.csv", "r") as f:
    lines = f.readlines()[1:]  # 跳过第一行标题

for i, line in enumerate(lines,start=2): # 从第二行开始计数
    parts = line.strip().split(",")

    try:
        # ======== 容易出错的两行代码 ========
        conc = float(parts[1])  # 转换浓度为浮点数
        temp = float(parts[2])  # 转换温度为浮点数

    except (ValueError, IndexError) as e:
        bad += 1
        print(f"第{i}行数据有误: {line.strip()}，错误信息: {e}")
        continue  # 跳过本次循环，继续处理下一行

    # ======== 计数器更新 ========
    ok += 1
    total += conc

print("-" * 45)
print(f"成功 {ok} 行,跳过 {bad} 行")
print(f"平均浓度: {total/ok:.4f}")  # 计算平均浓度