# 打开并读取文件内容
with open('data.txt', 'r') as file:
    lines = file.readlines()

# 新的文件名
new_filename = 'after_change_data.txt'

# 准备写入新文件
with open(new_filename, 'w') as new_file:
    # 遍历每一行进行处理
    for line in lines:
        # 去除行尾的换行符并分割字符串
        columns = line.strip().split()
        
        # 确保行中有足够多的列
        if len(columns) >= 6:
            # 尝试转换第5列和第6列为浮点数
            try:
                # 转换第5列和第6列为浮点数
                decimal_column_5 = float(columns[4])
                decimal_column_6 = float(columns[5])
                
                # 保留整数部分的前四位，如果小于1000则保留小数点后两位
                if decimal_column_5 >= 1000:
                    formatted_column_5 = f"{decimal_column_5:.1f}"[:4]
                else:
                    formatted_column_5 = f"{decimal_column_5:.2f}"
        
                if decimal_column_6 >= 1000:
                    formatted_column_6 = f"{decimal_column_6:.1f}"[:4]
                else:
                    formatted_column_6 = f"{decimal_column_6:.1f}"
                
                # 替换原行中的第5列和第6列
                columns[4] = formatted_column_5
                columns[5] = formatted_column_6
                
                # 将处理后的行写入新文件
                new_file.write('	'.join(columns) + '\n')
            except ValueError as e:
                # 如果转换失败，打印错误信息
                print(f"错误：第5列或第6列的值无法转换为浮点数。{e}")
        else:
            print(f"警告：行 '{line}' 的列数不足6列，跳过此行。")

print(f"处理完成，结果已保存到 '{new_filename}'。")