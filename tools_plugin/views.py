from django.shortcuts import render
from .forms import MathPlugin
from .utils.math_plugin import math_add_reduce_vary, math_add_reduce_base


def tools_index(request):
    context = {}
    return render(request, "tools_base.html", context)


def tools_math_plugin(request):
    if request.method == 'POST':
        math_form = MathPlugin(request.POST)
        if math_form.is_valid():
            columns_num = 4  # 分为5列
            lim_min = math_form.cleaned_data['lim_min']
            lim_max = math_form.cleaned_data['lim_max']
            max_num = math_form.cleaned_data['max_num']
            bit_mode = math_form.cleaned_data['bit_mode']
            page_num = math_form.cleaned_data['page_num']
            # 判断范围是否倒挂
            # if input_data['lim_min'] >= input_data['lim_max']:
            #   return render(request, 'tools_plugin/arithmetic.html', {'error_msg': {'lim_min': '最小值不能大于等于最大值'}})
            all_page_list = []
            all_page_format_list = []
            for p in range(page_num):
                math_list = []
                math_format_list = []
                for i in range(max_num):
                    # 按八二原则来分配基础题和变换题
                    if i <= max_num * 0.8:
                        math_str, math_str_format = math_add_reduce_base(lim_min, lim_max, bit_mode)
                    else:
                        math_str, math_str_format = math_add_reduce_vary(lim_min, lim_max, bit_mode)
                    math_list.append(math_str)
                    math_format_list.append(math_str_format)

                # 大列表拆成多个小列表
                all_math_list = [math_list[x:x + columns_num] for x in range(0, len(math_list), columns_num)]
                all_math_format_list = [math_format_list[x:x + columns_num] for x in range(0, len(math_format_list), columns_num)]
                all_page_list.append(all_math_list)
                all_page_format_list.append(all_math_format_list)
            context = {'all_page_list': all_page_list, 'all_page_format_list': all_page_format_list}
            return render(request, 'tools_plugin/arithmetic_detail.html', context)
    else:
        math_form = MathPlugin()
    context = {'math_form': math_form}
    return render(request, "tools_plugin/arithmetic.html", context)
