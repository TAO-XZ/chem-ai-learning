#阅读D:\study\chem-ai-learning\.vscode\measurements.csv输出
#S-01  浓度 0.1021  温度 25.3 ℃
#S-02  浓度 0.1018  温度 25.1 ℃
#S-03  浓度 0.1035  温度 25.4 ℃
#S-04  浓度 0.1012  温度 25.0 ℃
#S-05  浓度 0.1029  温度 25.2 ℃
#--------------------------------
#样品个数: 5
#浓度平均值: 0.1023
#温度平均值: 25.2
with open("data/measurements.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()[1:]  # 跳过第一行标题
    total_concentration = 0
    total_temperature = 0
    sample_count = len(lines)
    
    for line in lines:
        parts = line.strip().split(",")
        sample_name = parts[0].strip()
        concentration = float(parts[1].strip())
        temperature = float(parts[2].strip())
        
        print(f"{sample_name}  浓度 {concentration}  温度 {temperature} ℃")
        
        total_concentration += concentration
        total_temperature += temperature
    
    average_concentration = total_concentration / sample_count
    average_temperature = total_temperature / sample_count
    
    print("--------------------------------")
    print(f"样品个数: {sample_count}")
    print(f"浓度平均值: {average_concentration:.4f}")
    print(f"温度平均值: {average_temperature:.1f}")