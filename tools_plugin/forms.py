from django import forms


class MathPlugin(forms.Form):
    lim_min = forms.IntegerField(label="最小值(数字)",
                                 widget=forms.NumberInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': '请输入最小范围(比如0)',
                                 }
                                 ))
    lim_max = forms.IntegerField(label="最大值(数字)",
                                 widget=forms.NumberInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': '请输入最大范围(比如10)',
                                 }
                                 ))
    bit_mode = forms.IntegerField(min_value=2,
                                  label="运算位数",
                                  widget=forms.NumberInput(attrs={
                                      'class': 'form-control',
                                      'placeholder': '请输入位数(比如2)',
                                  }
                                  ))
    max_num = forms.IntegerField(min_value=1,
                                 label="生成数量",
                                 widget=forms.NumberInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': '请输入生成的习题数量(比如100)',
                                 }
                                 ))
    page_num = forms.IntegerField(min_value=1,
                                  label="生成页数",
                                  widget=forms.NumberInput(attrs={
                                      'class': 'form-control',
                                      'placeholder': '需要生成的页数(比如2页)',
                                  }
                                  ))

    def clean(self):
        lim_min = self.cleaned_data.get('lim_min')
        lim_max = self.cleaned_data.get('lim_max')

        if lim_min >= lim_max:
            raise forms.ValidationError({'lim_min': '最小值不能大于等于最大值'})
        return self.cleaned_data
