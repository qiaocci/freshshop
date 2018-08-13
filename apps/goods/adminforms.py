from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class GoodsAdminForm(forms.ModelForm):
    goods_desc = forms.CharField(widget=CKEditorUploadingWidget(), label='详细描述', required=True)
