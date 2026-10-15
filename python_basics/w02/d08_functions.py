#① 写一个函数 describe_ph(ph)
def describe_ph(ph):
    #项	要求
    #参数	一个 pH 值
    #返回	「酸性」/「中性」/「碱性」三个字符串之一
    #⚠️ 禁止	函数里不许用 print —— 只能 return
    if ph < 7:
        return "酸性"
    elif ph == 7:
        return "中性"
    else:
        return "碱性"
    #② 在函数外面，用 for 循环把 pH = 3、7、11 各调用一次并打印：
for ph in [3, 7, 11]:
    print(f"pH = {ph} 是 {describe_ph(ph)}")
