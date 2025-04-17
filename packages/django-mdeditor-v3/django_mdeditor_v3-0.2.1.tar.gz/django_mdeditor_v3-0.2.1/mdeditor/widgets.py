# -*- coding:utf-8 -*-
from __future__ import absolute_import

from django import forms
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt

from .configs import MDConfig


class MDEditorWidget(forms.Textarea):
    """
    Widget providing md-editor-v3 for Rich Text Editing.
    See docs: https://imzbf.github.io/md-editor-v3/zh-CN/
    """
    def __init__(self, config_name='default', *args, **kwargs):
        super(MDEditorWidget, self).__init__(*args, **kwargs)
        # Setup config from defaults.
        self.config = MDConfig(config_name)

    def render(self, name, value, attrs=None, renderer=None):
        """
        renderer: django4+ 参数
        """
        if value is None:
            value = ''

        final_attrs = self.build_attrs(self.attrs, attrs, name=name)
        return mark_safe(render_to_string('markdown.html', {
            'final_attrs': flatatt(final_attrs),
            'value': conditional_escape(force_str(value)),
            'id': final_attrs['id'],
            'config': self.config,
        }))

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        """
        Helper function for building an attribute dictionary.
        """
        attrs = dict(base_attrs or {}, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs

    def _get_media(self):
        return forms.Media(
            css={
                "all": ("mdeditor/css/md-editor-v3.css",)
            },
            js=(
                "mdeditor/js/vue.global.prod.js",
                "mdeditor/js/md-editor-v3.umd.js",
            ))
    media = property(_get_media)
