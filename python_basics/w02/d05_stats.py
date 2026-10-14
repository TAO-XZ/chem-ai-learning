#把一组重复测量的浓度数据存成一个列表： 0.1021, 0.1018, 0.1035, 0.1012, 0.1029
#① 先用 for 循环把每个值打印出来 ② 再算出并打印：个数、最大值、最小值、平均值、极差
concentrations = [0.1021, 0.1018, 0.1035, 0.1012, 0.1029]
for conc in concentrations:
    print(conc)

print(f"个数: {len(concentrations)}")
print(f"最大值: {max(concentrations)}")
print(f"最小值: {min(concentrations)}")
print(f"平均值: {sum(concentrations)/len(concentrations):.4f}")
print(f"极差: {max(concentrations) - min(concentrations):.4f}")