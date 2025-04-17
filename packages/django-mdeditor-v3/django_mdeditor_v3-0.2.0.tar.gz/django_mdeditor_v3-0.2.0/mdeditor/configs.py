# -*- coding:utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


# md-editor-v3 默认配置
DEFAULT_CONFIG = {
    'width': '100%',
    'height': 500,
    'toolbar': [
        'bold', 'underline', 'italic', 'strikeThrough', '-',
        'title', 'sub', 'sup', 'quote', 'unorderedList', 'orderedList', '-',
        'codeRow', 'code', 'link', 'image', 'table', 'mermaid', 'katex', '-',
        'revoke', 'next', 'save', '=',
        'pageFullscreen', 'fullscreen', 'preview', 'htmlPreview', 'catalog'
    ],
    'upload_image_formats': ["jpg", "JPG", "jpeg", "JPEG", "gif", "GIF", "png",
                             "PNG", "bmp", "BMP", "webp", "WEBP"],
    'upload_image_url': '/mdeditor/uploads/',
    'image_folder': 'editor',
    'theme': 'light',  # dark / light
    'preview_theme': 'default',  # default / github / vuepress / mk-cute / smart-blue / cyanosis
    'editor_theme': 'default',  # default / github / gradient / kimbie / 等
    'toolbar_autofixed': True,
    'language': 'zh-CN',  # zh-CN / en-US
    'placeholder': '请输入内容...',
    'lineWrapping': False,
    'lineNumbers': False
}


class MDConfig(dict):

    def __init__(self, config_name='default'):
        self.update(DEFAULT_CONFIG)
        self.set_configs(config_name)

    def set_configs(self, config_name='default'):
        """
        set config item
        :param config_name:
        :return:
        """
        # Try to get valid config from settings.
        configs = getattr(settings, 'MDEDITOR_CONFIGS', None)
        if configs:
            if isinstance(configs, dict):
                # Make sure the config_name exists.
                if config_name in configs:
                    config = configs[config_name]
                    # Make sure the configuration is a dictionary.
                    if not isinstance(config, dict):
                        raise ImproperlyConfigured('MDEDITOR_CONFIGS["%s"] \
                                        setting must be a dictionary type.' %
                                                   config_name)
                    # Override defaults with settings config.
                    self.update(config)
                else:
                    raise ImproperlyConfigured("No configuration named '%s' \
                                    found in your MDEDITOR_CONFIGS setting." %
                                               config_name)
            else:
                raise ImproperlyConfigured('MDEDITOR_CONFIGS setting must be a\
                                dictionary type.')

