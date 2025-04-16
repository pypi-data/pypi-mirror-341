import re

from django import template

register = template.Library()


@register.filter
def field_type(field):
    """
    返回字段的类型名称
    """

    return field.__class__.__name__


@register.filter
def split(value, arg):
    """
    将字符串按指定分隔符分割为列表
    """
    return value.split(arg)


@register.filter
def table_item_type(item, instance):
    """
    返回字段类型和值信息，使用实例直接获取字段值
    """
    item_str = str(item)

    # 提取字段名
    field_match = re.search(r"field-(\w+)", item_str)
    if not field_match:
        return item  # 不是字段单元格，直接返回

    field_name = field_match.group(1)

    # 尝试获取模型字段
    try:
        model = instance.__class__
        model_field = model._meta.get_field(field_name)
        field_type = model_field.__class__.__name__

        # 处理布尔字段
        if field_type == "BooleanField":
            # 直接从实例获取值
            is_true = getattr(instance, field_name, False)

            # 提取input的id和name
            input_id = None
            input_name = None

            id_match = re.search(r'id="([^"]+)"', item_str)
            if id_match:
                input_id = id_match.group(1)

            name_match = re.search(r'name="([^"]+)"', item_str)
            if name_match:
                input_name = name_match.group(1)

            return {
                "field_name": field_name,
                "field_type": "boolean",
                "value": is_true,
                "editable": '<input type="checkbox"' in item_str,
                "input_id": input_id,
                "input_name": input_name,
            }

        # 处理图片字段
        elif field_type in ["ImageField", "FileField"]:
            # 直接从实例获取值
            field_value = getattr(instance, field_name, None)
            img_url = (
                field_value.url if field_value and hasattr(field_value, "url") else ""
            )

            return {"field_name": field_name, "field_type": "image", "value": img_url}

        # 处理TagField
        elif field_type == "TagField":
            # 获取字段值
            value = getattr(instance, field_name, None)

            # 获取显示名称
            display_name = ""
            tag_type = "info"  # 默认标签类型

            # 如果有choices，获取对应的显示名称
            if hasattr(model_field, "choices") and model_field.choices:
                choices_dict = dict(model_field.choices)
                if value in choices_dict:
                    display_name = choices_dict[value]

            # 如果有tag_colors，获取对应的标签类型
            if (
                hasattr(model_field, "tag_colors")
                and model_field.tag_colors
                and value in model_field.tag_colors
            ):
                tag_type = model_field.tag_colors[value]

            return {
                "field_name": field_name,
                "field_type": "tag",
                "value": value,
                "display_name": display_name,
                "tag_type": tag_type,
            }

    except Exception as e:
        # 如果出现错误，记录错误并返回原始项
        print(f"Error processing field {field_name}: {str(e)}")

    # 对于其他所有情况，直接返回原始项
    return item
