from django.forms import widgets


class ElSelect(widgets.Select):
    """Element UI 风格的日期选择器"""
    template_name = 'widgets/select.html'
    option_template_name = 'widgets/select_opt.html'

    def __init__(self, attrs=None, format=None):
        attrs = attrs or {}
        attrs.update({'class': 'el-select'})
        super().__init__(attrs, format)
