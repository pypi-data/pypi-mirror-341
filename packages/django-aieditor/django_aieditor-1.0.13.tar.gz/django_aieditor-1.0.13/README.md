# Django-AiEditor

Django-AiEditor 是一个为 Django 框架提供的 AiEditor 富文本编辑器集成包。AiEditor 是一个强大的 Web 富文本编辑器。

## 安装

```bash
pip install django-aieditor
```

## 快速开始

1. 将 'django_aieditor' 添加到你的 INSTALLED_APPS 中：

```python
INSTALLED_APPS = [
    ...
    'django_aieditor',
]
```

2. 配置上传URL路由，在项目的urls.py中添加：

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('aieditor/', include('django_aieditor.urls')),
]
```


3. 在你的模型中使用：

```python
from django_aieditor.fields import AiEditorModelField

class MyModel(models.Model):
    content = AiEditorModelField("内容")
```

4. 在你的表单中使用：

```python
from django_aieditor.fields import AiEditorField

class MyForm(forms.Form):
    content = AiEditorField()
```

## 配置

在你的 settings.py 中可以添加以下配置：

```python
AIEDITOR_CONFIG = {
    'toolbar': ['bold', 'italic', 'link', 'image'], # 工具栏
}
```
更多配置请访问：[https://aieditor.dev/zh/](https://aieditor.dev/zh/)

## 特性

- 完整支持 AiEditor 的所有功能
- 简单的 Django 集成
- 支持文件上传（支持本地存储和云存储）
- 支持自定义配置
- Django Admin 集成

## 更新日志

### v1.0.13 (2025-04-16)
- 升级 AiEditor 到 1.3.6 版本
- 新增高亮块功能支持
- 新增文字计数器功能
- 新增工具栏按钮大小调整功能
- 优化粘贴配置，增强粘贴体验

## 文档

aiEditor 文档请访问：[https://aieditor.dev/zh/](https://aieditor.dev/zh/)

Django-AiEditor 文档请访问：[https://github.com/mircool/django-aieditor](https://github.com/mircool/django-aieditor)

## License

MIT License