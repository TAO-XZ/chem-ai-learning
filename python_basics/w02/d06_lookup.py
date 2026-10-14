#① 先建一张摩尔质量表（用 dict）：
#物质	摩尔质量 (g/mol)
#NaOH	40.0
#HCl	36.5
#H2SO4	98.1
#NaCl	58.5
#KOH	56.1
#② 程序做两件事：
#问用户物质名和质量 (g)
#查表，算出物质的量 (mol) 并打印
#③ 关键要求：
#如果用户输入的物质不在表里，打印「表里没有这个物质」， 不许报错（别让 KeyError 蹦出来）。
molar_mass_table = {"NAOH": 40.0, "HCL": 36.5, "H2SO4": 98.1, "NACL": 58.5, "KOH": 56.1}
name = input("请输入物质名：").upper()
mass = float(input("请输入质量 (g)："))
molar_mass = molar_mass_table.get(name)
if molar_mass is None:
    print("表里没有这个物质")
else:
    moles = mass / molar_mass
    print(f"{name}的物质的量是 {moles:.2f} mol")