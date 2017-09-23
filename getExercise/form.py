from django import forms
from django.core.exceptions import ValidationError
# Create your forms here.

def words_validator(comment):
    if len(comment) < 4:
        raise ValidationError('字数不够')

def comment_validator(comment):
    # if 'a' in comment:
    #     raise ValidationError('内容不能包含a')
    keywords = ['发票','钱']
    for keyword in keywords:
        if keyword in comment:
            raise ValidationError("你的评论不能包含'发票'和'钱'关键字")

class CommentForm(forms.Form):
    name = forms.CharField(max_length=50)
    comment = forms.CharField(
        widget=forms.Textarea(),
        error_messages={
            'required':'wow, such words'
        },
        validators=[words_validator, comment_validator]
                              )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()