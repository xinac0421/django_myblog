import random


def scope_limit(num, lim_min, lim_max, symbol):
    """
    限制范围内的基础运算
    :param num: 传入的数字
    :param lim_min: 运算的最小范围
    :param lim_max: 运算的最大范围
    :param symbol: 符号，'+'，'-'等
    :return: 返回列表[符号, 运算的数字, 运算结果]
    """
    s_num = random.randint(lim_min, lim_max)
    if s_num < 0:
        symbol = '-'
        s_num = abs(s_num)
    if symbol == '+':
        result = num + s_num
        if result > lim_max:  # 如果相加结果大于范围最大值，则改成相减
            result = num - s_num
            symbol = '-'
            while result < lim_min:  # 若干相减后值小于范围最小值，则减数整除2，直到相减不小于最小值
                s_num = s_num//2
                result = num - s_num
    elif symbol == '-':
        result = num - s_num
        if result < 0:  # 如果相减结果小于范围最小值，则改成相加
            result = num + s_num
            symbol = '+'
            while result > lim_max:
                s_num = s_num // 2
                result = num + s_num
    else:
        result = False
    return [symbol, s_num, result]


def math_add_reduce_vary(lim_min, lim_max, bit_mode=2):
    """
    数学运算出题(变换)
    :param lim_min: 最小范围
    :param lim_max: 最大范围
    :param bit_mode: 运算位数，默认2位
    :return: 返回列表[运算等式, 已格式化其中一个数字为()的等式]
    """
    format_str = '___'  # 格式化计输入格式，可以是___，也可以为( )
    one_num = random.randint(lim_min, lim_max)  # 生成第一个数
    result = one_num
    result_str = result_str_format = '%s' % result
    format_index = random.randint(0, bit_mode)  # 按随机数格式化输出的格式，比如( ) + 1 = 9
    if format_index == 0:  # 若随机到第一个数，则格式化为（ ）
        result_str_format = '%s' % format_str

    # 按bit_mode数，循环做运算，保存运算的过程和结果
    for i in range(bit_mode-1):
        symbol = random.choice(['+', '-'])
        if symbol == '+':
            symbol, s_num, result = scope_limit(result, lim_min, lim_max, '+')
        else:
            symbol, s_num, result = scope_limit(result, lim_min, lim_max, '-')
        result_str += ' %s %s' % (symbol, s_num)
        if format_index == i+1:
            result_str_format += ' %s %s' % (symbol, format_str)
        else:
            result_str_format += ' %s %s' % (symbol, s_num)
    # 等式是左还是右，统一格式输出
    is_left = random.choice([True, False])  # 随机等式是左还是右
    if is_left:
        result_str = '%s = %s' % (result_str, result)
        if format_index == bit_mode:
            result_str_format = '%s = %s' % (result_str_format, format_str)
        else:
            result_str_format = '%s = %s' % (result_str_format, result)
    else:
        result_str = '%s = %s' % (result, result_str)
        if format_index == bit_mode:
            result_str_format = '%s = %s' % (format_str, result_str_format)
        else:
            result_str_format = '%s = %s' % (result, result_str_format)
    return [result_str, result_str_format]


def math_add_reduce_base(lim_min, lim_max, bit_mode=2):
    """
    数学运算出题(基础)，比如3+2=____
    :param lim_min: 最小范围
    :param lim_max: 最大范围
    :param bit_mode: 运算位数，默认2位
    :return: 返回列表[运算等式, ]
    """
    format_str = '___'  # 格式化计输入格式，可以是___，也可以为( )
    one_num = random.randint(lim_min, lim_max)  # 生成第一个数
    result = one_num
    result_str = '%s' % result

    # 按bit_mode数，循环做运算，保存运算的过程和结果
    for i in range(bit_mode-1):
        symbol = random.choice(['+', '-'])
        if symbol == '+':
            symbol, s_num, result = scope_limit(result, lim_min, lim_max, '+')
        else:
            symbol, s_num, result = scope_limit(result, lim_min, lim_max, '-')
        result_str += ' %s %s' % (symbol, s_num)

    return ['%s = %s' % (result_str, result), '%s = %s' % (result_str, format_str)]