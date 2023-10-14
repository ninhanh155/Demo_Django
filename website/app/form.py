from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

us_help_text='''
    <ul>
        <li>Bắt buộc.</li>
        <li>Tối đa 150 kí tự.</li>
    </ul>
'''

pas1_help_text='''
    <ul>
        <li>Mật khẩu của bạn không được quá giống với thông tin cá nhân khác của bạn.</li>
        <li>Mật khẩu của bạn phải chứa ít nhất 8 ký tự.</li>
        <li>Mật khẩu của bạn không được là mật khẩu thường được sử dụng.</li>
        <li>Mật khẩu của bạn không được hoàn toàn bằng số.</li>
    </ul>
'''

pas2_help_text='''Nhập cùng một mật khẩu như trước, để xác minh.'''
     
class Bieumau_dangky_thanhvien(UserCreationForm):
    email = forms.CharField(max_length=254, 
                          required=True, 
                          widget=forms.EmailInput(),
                          label='Thư điện tử')
  
    def __init__(self, *args, **kwargs):
        super(Bieumau_dangky_thanhvien, self).__init__(*args, **kwargs)
    
        self.fields['username'].label = "Tài khoản"
        self.fields['username'].help_text = us_help_text
    
        self.fields['password1'].label = "Mật khẩu"
        self.fields['password1'].help_text = pas1_help_text
        self.fields['password2'].label = "Xác nhận mật khẩu"
        self.fields['password2'].help_text = pas2_help_text
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class Bieumau_doimatkhau(PasswordChangeForm):
    old_password = forms.CharField(label='Mật khẩu cũ' , widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='Mật khẩu mới' , widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Xác nhận mật khẩu' , widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Họ và tên', max_length=100)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Nội dung', widget=forms.Textarea)