from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class GoodsAdminForm(forms.ModelForm):
    goods_desc = forms.CharField(widget=CKEditorUploadingWidget(), label='详细描述', required=True)
