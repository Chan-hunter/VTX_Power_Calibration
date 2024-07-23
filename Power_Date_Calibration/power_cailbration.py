import csv

def read_file_lines(filename):
    """读取文件中的所有行，并返回行列表"""
    with open(filename, 'r') as file:
        return file.readlines()

def process_columns(lines):
    processed_lines = []
    error_line = 0
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
                        group = '14'
                    elif 19.8 <= prefix_column_5 <= 20.2:
                        group = '20'
                    elif 22.8 <= prefix_column_5 <= 23.2:
                        group = '23'
                    elif 25.8 <= prefix_column_5 <= 26.2:
                        group = '26'
                    else :
                        group = '其他'
                    #在第7列添加组别
                    columns.append(group)
                    if group in ['14', '20','23', '26']:
                        # 将处理后的行写入新文件
                        processed_lines.append('	'.join(columns) + '\n')

            except ValueError:
                error_line = error_line+1
        else:
            error_line = error_line+1
    print('\n'f"至少有{error_line}处错误数据")

    return processed_lines

def write_to_new_file(processed_lines, new_filename):
    """将处理后的数据写入新文件"""
    with open(new_filename, 'w') as new_file:
        new_file.writelines(processed_lines)
    print(f"处理完成，结果已保存到 '{new_filename}'。"'\n')

def calculate_averages(filename):
    averages = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            try:
                col1 = row[0]
                col7 = row[6]
                col5 = float(row[3])
                key = (col1, col7)
                if key not in averages:
                    averages[key] = []
                averages[key].append(col5)
            except (IndexError, ValueError):
                continue

    # 计算平均值并格式化输出
    result_matrix = {}
    for (col1, col7), values in averages.items():
        average_value = round(sum(values) / len(values))
        result_matrix.setdefault(col7, {})[col1] = average_value

    # 构建最终的输出格式
    output = ["   /*5600,5650,5700,5750,5800,5850,5900,5950,6000*/"]
    for col7 in sorted(result_matrix):
        output.append(f"    {{" + ", ".join(f"{value}" for value in result_matrix[col7].values()) + f"}},  /*{col7}*/")

    if '26' in result_matrix:
        # 获取第4行的数据
        fourth_row = result_matrix['26']
    
        # 计算平均值
        number_of_columns = len(fourth_row)  # 假设有9列数据
        average_of_fourth_row = sum(fourth_row.values()) / number_of_columns
        average_of_fourth_row = int(average_of_fourth_row) + 1
    
        # 打印平均值
        print(f"最大功率的Vpd参考值: {average_of_fourth_row}"'\n')

    return "\n".join(output)

# 主逻辑
if __name__ == "__main__":
    original_filename = 'data.txt'
    new_filename = 'after_collating_data.txt'
    lines = read_file_lines(original_filename)
    processed_lines = process_columns(lines)
    write_to_new_file(processed_lines, new_filename)
    output = calculate_averages(new_filename)
    print(output)