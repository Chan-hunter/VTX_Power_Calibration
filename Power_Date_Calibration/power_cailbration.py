def read_file_lines(filename):
    """读取文件中的所有行，并返回行列表"""
    with open(filename, 'r') as file:
        return file.readlines()

def process_columns(lines):
    """处理每一行的第5列和第6列，仅保留整数部分的前4位和一个小数位"""
    processed_lines = []
    for line in lines:
        columns = line.strip().split()
        if len(columns) >= 6:
            try:
                # 转换第5列和第6列为浮点数
                decimal_column_1 = float(columns[0])
                decimal_column_2 = float(columns[1])
                decimal_column_5 = float(columns[4])
                decimal_column_6 = float(columns[5])
                # 保留整数部分的前四位，如果小于1000则保留小数点后两位
                if decimal_column_5 >= 1000:
                    formatted_column_5 = f"{decimal_column_5:.1f}"[:4]
                else:
                    formatted_column_5 = f"{decimal_column_5:.2f}"
                prefix_column_5  = float(str(formatted_column_5))
        
                if decimal_column_6 >= 1000:
                    formatted_column_6 = f"{decimal_column_6:.1f}"[:4]
                else:
                    formatted_column_6 = f"{decimal_column_6:.1f}"
                prefix_column_6 = int(str(formatted_column_6))

                error = abs(decimal_column_6 - decimal_column_1)
                
                    # 替换原行中的第5列和第6列
                columns[4] = formatted_column_5
                columns[5] = formatted_column_6

                error = abs(prefix_column_6 - decimal_column_1)
                #仅输出测量频率与目标频率的误差小于2的，PWM值正常的行
                if (error <= 2) & (decimal_column_2 != 2000) & (decimal_column_2 != 2):
                     # 根据第5列的值分类
                    if 13.8 <= prefix_column_5 <= 14.2:
                        group = 'A'
                    elif 19.8 <= prefix_column_5 <= 20.2:
                        group = 'B'
                    elif 22.8 <= prefix_column_5 <= 23.2:
                        group = 'C'
                    elif 25.8 <= prefix_column_5 <= 26.2:
                        group = 'D'
                    else :
                        group = '其他'
                    
                    if group in ['A', 'B','C', 'D']:
                        # 将处理后的行写入新文件
                        processed_lines.append('	'.join(columns) + '\n')
                print(f"{error}")

            except ValueError:
                print(f"错误：无法转换第5列或第6列的值。")
        else:
            print(f"警告：列数不足6列，跳过此行。")
    return processed_lines

def write_to_new_file(processed_lines, new_filename):
    """将处理后的数据写入新文件"""
    with open(new_filename, 'w') as new_file:
        new_file.writelines(processed_lines)
    print(f"处理完成，结果已保存到 '{new_filename}'。")

# 主逻辑
if __name__ == "__main__":
    original_filename = 'data.txt'
    new_filename = 'after_collating_data.txt'
    lines = read_file_lines(original_filename)
    processed_lines = process_columns(lines)
    write_to_new_file(processed_lines, new_filename)