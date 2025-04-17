from django import forms
from django.db import models
from django.conf import settings
from django.contrib.admin import widgets
from django.urls import reverse
import json


class AiEditorWidget(forms.Textarea):
    template_name = 'django_aieditor/widget.html'

    def __init__(self, attrs=None):
        default_attrs = {'class': 'aieditor'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    @property
    def media(self):
        return forms.Media(
            css={
                'all': (
                    'django_aieditor/css/aieditor.min.css',
                )
            },
            js=(
                'django_aieditor/js/aieditor.umd.js',
                'django_aieditor/js/init.js',
            )
        )

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # 获取默认配置
        default_config = {
            'placeholder': '请输入内容...',  # 占位提示文本
            'toolbarKeys': ["undo", "redo", "brush", "eraser",
                "|", "heading", "font-family", "font-size",
                "|", "bold", "italic", "underline", "strike", "link", "code", "subscript", "superscript", "hr", "todo", "emoji",
                "|", "highlight", "font-color",
                "|", "align", "line-height",
                "|", "bullet-list", "ordered-list", "indent-decrease", "indent-increase", "break",
                "|", "image", "video", "attachment", "quote", "code-block", "table", "container",
                "|", "source-code", "printer", "fullscreen", "ai"
            ],
            'textCounter': True,  # 显示文字计数器
            'toolbarSize': 'medium',  # 工具栏按钮大小
            'image': {
                'uploadUrl': reverse('django_aieditor:upload_image'),  # 上传接口地址
                'allowBase64': False,  # 禁用base64
                'defaultSize': 350,  # 默认图片宽度
                'uploadFormName': 'file',  # 上传字段名
                'maxFileSize': 5 * 1024 * 1024,  # 限制文件大小为5MB
                'bubbleMenuEnable': True,  # 启用图片浮动菜单
                'headers': {
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            },
            'htmlPasteConfig': {
                'removeEmptyParagraphs': True,  # 移除空段落
                'clearLineBreaks': True  # 清除换行符
            }
        }

        # 获取用户配置
        user_config = getattr(settings, 'AIEDITOR_CONFIG', {})

        # 递归合并配置
        def merge_config(default, user):
            result = default.copy()
            for key, value in user.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_config(result[key], value)
                else:
                    result[key] = value
            return result

        # 合并配置
        final_config = merge_config(default_config, user_config)

        # 将配置转换为JSON字符串,确保正确序列化
        context['widget']['config'] = json.dumps(final_config)
        return context


class AiEditorAdminWidget(AiEditorWidget, widgets.AdminTextareaWidget):
    pass


class AiEditorField(forms.CharField):
    widget = AiEditorWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AiEditorModelField(models.TextField):
    def formfield(self, **kwargs):
        if kwargs.get('widget') == widgets.AdminTextareaWidget:
            kwargs['widget'] = AiEditorAdminWidget
        else:
            kwargs['widget'] = AiEditorWidget
        return super().formfield(**kwargs)