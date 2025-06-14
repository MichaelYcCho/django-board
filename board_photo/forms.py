from django import forms
from .models import PhotoBoard


class PhotoBoardForm(forms.ModelForm):
    password_confirm = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '비밀번호를 다시 입력하세요'
        })
    )

    class Meta:
        model = PhotoBoard
        fields = ['title', 'first_name', 'last_name', 'email', 'password', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목을 입력하세요'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '이름'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '성'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@example.com'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '비밀번호를 입력하세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '내용을 입력하세요'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

        return cleaned_data


class PhotoBoardUpdateForm(forms.ModelForm):
    password_verify = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '수정을 위해 비밀번호를 입력하세요'
        })
    )

    class Meta:
        model = PhotoBoard
        fields = ['title', 'first_name', 'last_name', 'email', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }


class PasswordVerifyForm(forms.Form):
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '비밀번호를 입력하세요'
        })
    )
