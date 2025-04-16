import os

import numpy as np
import torch
import wandb


def initialize_results_file(results_file, result_info):
    """
    初始化结果文件，确保文件存在且第一行包含指定的内容。

    参数:
        results_file (str): 结果文件的路径。
        result_info (list): 需要写入的第一行内容列表。
    """
    # 处理 result_info，在每个单词后添加两个空格
    result_info_str = "  ".join(result_info) + '\n'
    # 检查文件是否存在
    if os.path.exists(results_file):
        # 如果文件存在，读取第一行
        with open(results_file, "r") as f:
            first_line = f.readline().strip()
        # 检查第一行是否与 result_info 一致
        if first_line == result_info_str.strip():
            print(f"文件 {results_file} 已存在且第一行已包含 result_info，不进行写入。")
        else:
            # 如果不一致，写入 result_info
            with open(results_file, "w") as f:
                f.write(result_info_str)
            print(f"文件 {results_file} 已被重新初始化。")
    else:
        # 如果文件不存在，创建并写入 result_info
        with open(results_file, "w") as f:
            f.write(result_info_str)
        print(f"文件 {results_file} 已创建并写入 result_info。")


def write_results_file(file_path: str,
                       data_dict: dict,
                       column_order: list,
                       float_precision: int = 5) -> None:
    """
    通用格式化文本行写入函数（支持列表形式数据）

    参数：
    file_path: 目标文件路径
    data_dict: 包含数据的字典，键为列名，值为列表
    column_order: 列顺序列表，元素为字典键
    float_precision: 浮点数精度位数 (默认5位)
    """
    # 验证数据格式
    rows = None
    for key in data_dict:
        if not isinstance(data_dict[key], list):
            raise ValueError(f"Value for key '{key}' is not a list")
        if rows is None:
            rows = len(data_dict[key])
        else:
            if len(data_dict[key]) != rows:
                raise ValueError("All lists in data_dict must have the same length")

    # 辅助函数：格式化单个值
    def format_value(value, column_name):
        if isinstance(value, (int, np.integer)):
            return f"{value:d}"
        elif isinstance(value, (float, np.floating)):
            if column_name in ['train_losses', 'val_losses']:
                return f"{value:.{float_precision + 1}f}"
            elif column_name == 'lrs':
                return f"{value:.8f}"
            else:
                return f"{value:.{float_precision}f}"
        elif isinstance(value, str):
            return value
        else:
            return str(value)

    # 计算列宽
    column_widths = []
    for col in column_order:
        dict_key = 'val_accuracies' if col == 'accuracies' else col
        if dict_key not in data_dict:
            raise ValueError(f"Missing required column: {dict_key}")
        values = data_dict[dict_key]

        max_width = len(col)
        for val in values:
            fmt_val = format_value(val, col)
            max_width = max(max_width, len(fmt_val))
        column_widths.append(max_width)

    # 生成格式化行
    lines = []
    for i in range(rows):
        row = []
        for j, col in enumerate(column_order):
            dict_key = 'val_accuracies' if col == 'accuracies' else col
            val = data_dict[dict_key][i]
            fmt_val = format_value(val, col)

            # 对齐处理
            if j == len(column_order) - 1:
                fmt_val = fmt_val.ljust(column_widths[j])
            else:
                fmt_val = fmt_val.rjust(column_widths[j])
            row.append(fmt_val)
        lines.append("  ".join(row) + '\n')

    # 写入文件
    with open(file_path, 'a', encoding='utf-8') as f:
        f.writelines(lines)


def append_to_results_file(file_path: str,
                           data_dict: dict,
                           column_order: list,
                           float_precision: int = 5) -> None:
    """
    通用格式化文本行写入函数

    参数：
    file_path: 目标文件路径
    data_dict: 包含数据的字典，键为列名
    column_order: 列顺序列表，元素为字典键
    float_precision: 浮点数精度位数 (默认5位)
    """
    # 检查 data_dict 中的值是否为列表
    all_values_are_lists = all(isinstance(value, list) for value in data_dict.values())
    if all_values_are_lists:
        num_rows = len(next(iter(data_dict.values())))
        # 逐行处理
        for row_index in range(num_rows):
            formatted_data = []
            column_widths = []
            for col in column_order:
                # 处理字典键的别名
                dict_key = 'val_accuracies' if col == 'accuracies' else col
                # 如果键不存在，跳过该列
                if dict_key not in data_dict:
                    continue
                value_list = data_dict[dict_key]
                if row_index >= len(value_list):
                    continue
                value = value_list[row_index]

                # 根据数据类型进行格式化
                if isinstance(value, (int, np.integer)):
                    fmt_value = f"{value:d}"
                elif isinstance(value, (float, np.floating)):
                    if col in ['train_losses', 'val_losses']:  # 如果列名是'train_losses'或'val_losses'，保留浮点数精度位数+1位
                        fmt_value = f"{value:.{float_precision + 1}f}"
                    elif col == 'lrs':  # 如果列名是'lrs'，保留8位小数
                        fmt_value = f"{value:.8f}"
                    else:
                        fmt_value = f"{value:.{float_precision}f}"
                elif isinstance(value, str):
                    fmt_value = value
                else:  # 处理其他类型转换为字符串
                    fmt_value = str(value)

                # 取列名长度和数值长度的最大值作为列宽
                column_width = max(len(col), len(fmt_value))
                column_widths.append(column_width)

                # 应用列宽对齐
                if col == column_order[-1]:  # 最后一列左边对齐
                    fmt_value = fmt_value.ljust(column_width)
                else:
                    fmt_value = fmt_value.rjust(column_width)

                formatted_data.append(fmt_value)

            # 构建文本行并写入，列之间用两个空格分隔
            if formatted_data:
                line = "  ".join(formatted_data) + '\n'
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(line)
    else:
        # 非列表情况，原逻辑处理
        # 计算每列的最大宽度
        column_widths = []
        formatted_data = []
        for col in column_order:
            # 处理字典键的别名
            dict_key = 'val_accuracies' if col == 'accuracies' else col
            # 如果键不存在，跳过该列
            if dict_key not in data_dict:
                continue

            value = data_dict[dict_key]

            # 根据数据类型进行格式化
            if isinstance(value, (int, np.integer)):
                fmt_value = f"{value:d}"
            elif isinstance(value, (float, np.floating)):
                if col in ['train_losses', 'val_losses']:  # 如果列名是'train_losses'或'val_losses'，保留浮点数精度位数+1位
                    fmt_value = f"{value:.{float_precision + 1}f}"
                elif col == 'lrs':  # 如果列名是'lrs'，保留8位小数
                    fmt_value = f"{value:.8f}"
                else:
                    fmt_value = f"{value:.{float_precision}f}"
            elif isinstance(value, str):
                fmt_value = value
            else:  # 处理其他类型转换为字符串
                fmt_value = str(value)

            # 取列名长度和数值长度的最大值作为列宽
            column_width = max(len(col), len(fmt_value))
            column_widths.append(column_width)

            # 应用列宽对齐
            if col == column_order[-1]:  # 最后一列左边对齐
                fmt_value = fmt_value.ljust(column_width)
            else:
                fmt_value = fmt_value.rjust(column_width)

            formatted_data.append(fmt_value)

        # 构建文本行并写入，列之间用两个空格分隔
        if formatted_data:
            line = "  ".join(formatted_data) + '\n'
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(line)


# def append_to_results_file(file_path: str,
#                            data_dict: dict,
#                            column_order: list,
#                            column_widths: list = None,
#                            float_precision: int = 5) -> None:
#     """
#     通用格式化文本行写入函数
#
#     参数：
#     file_path: 目标文件路径
#     data_dict: 包含数据的字典，键为列名
#     column_order: 列顺序列表，元素为字典键
#     column_widths: 每列字符宽度列表 (可选)
#     float_precision: 浮点数精度位数 (默认4位)
#     """
#     formatted_data = []
#
#     # 遍历指定列顺序处理数据
#     for i, col in enumerate(column_order):
#         # 处理字典键的别名
#         if col == 'accuracies':
#             dict_key = 'val_accuracies'
#         else:
#             dict_key = col
#
#         if dict_key not in data_dict:
#             raise ValueError(f"Missing required column: {dict_key}")
#
#         value = data_dict[dict_key]
#
#         # 根据数据类型进行格式化
#         if isinstance(value, (int, np.integer)):
#             fmt_value = f"{value:d}"
#         elif isinstance(value, (float, np.floating)):
#             if col in ['train_losses', 'val_losses']:  # 如果列名是'train_losses'或'val_losses'，保留浮点数精度位数+1位
#                 fmt_value = f"{value:.{float_precision + 1}f}"
#             elif col == 'lr':  # 如果列名是'lr'，保留8位小数
#                 fmt_value = f"{value:.8f}"
#             else:
#                 fmt_value = f"{value:.{float_precision}f}"
#         elif isinstance(value, str):
#             fmt_value = value
#         else:  # 处理其他类型转换为字符串
#             fmt_value = str(value)
#
#         # 应用列宽对齐
#         if column_widths and i < len(column_widths):
#             try:
#                 if i == len(column_order) - 1:  # 最后一列左边对齐
#                     fmt_value = fmt_value.ljust(column_widths[i])
#                 else:
#                     fmt_value = fmt_value.rjust(column_widths[i])
#             except TypeError:  # 处理非字符串类型
#                 if i == len(column_order) - 1:  # 最后一列左边对齐
#                     fmt_value = str(fmt_value).ljust(column_widths[i])
#                 else:
#                     fmt_value = str(fmt_value).rjust(column_widths[i])
#
#         formatted_data.append(fmt_value)
#
#     # 构建文本行并写入
#     line = '\t'.join(formatted_data) + '\n'
#     with open(file_path, 'a', encoding='utf-8') as f:
#         f.write(line)


def get_wandb_key(key_path='tools/wandb_key.txt'):
    with open(key_path, 'r', encoding='utf-8') as f:
        key = f.read()
    return key


def wandb_use(project=None, name=None, key_path='tools/wandb_key.txt'):
    run = None
    if project is not None:
        wandb_key = get_wandb_key(key_path)
        wandb.login(key=wandb_key)
        run = wandb.init(project=project, name=name)
    return run
