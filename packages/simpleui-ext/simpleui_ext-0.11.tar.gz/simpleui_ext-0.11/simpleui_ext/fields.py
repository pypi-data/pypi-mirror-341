from django.db import models

from simpleui_ext.widgets import ElSelect


class TagField(models.IntegerField):
    """
    自定义标签字段，支持在管理界面中以 El-Tag 组件显示
    """

    def __init__(self, *args, choices=None, tag_colors=None, **kwargs) -> None:
        self.tag_colors = tag_colors or {}
        super().__init__(*args, choices=choices, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.tag_colors:
            kwargs["tag_colors"] = self.tag_colors
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        super().formfield()
        from django.forms import TypedChoiceField

        defaults = {
            "form_class": TypedChoiceField,
            "choices": self.choices,
            "widget": ElSelect,
            "coerce": int,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
