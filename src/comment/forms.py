from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):

    content = forms.CharField(
        label='评论*',
        max_length=100,
        required=True,
        widget=forms.widgets.Textarea(
            attrs={'class': 'form-control', 'rows': 4, 'cols': 60}
        )
    )
    nickname = forms.CharField(
        label='昵称*',
        max_length=50,
        required=True,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': "width: 100%;"}
        )
    )
    email = forms.CharField(
        label='Email*',
        max_length=50,
        required=True,
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control', 'style': "width: 100%;"}
        )
    )
    website = forms.CharField(
        label='网站',
        max_length=100,
        required=False,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control', 'style': "width: 100%;"}
        )
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('内容长度过短')
        return content
    
    class Meta:
        model = Comment
        fields = [
            'content',
            'nickname',
            'email',
            'website',
        ]
