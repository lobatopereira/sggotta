from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.contrib.auth.models import Group,User
from users.models import Profile

class DateInput(forms.DateInput):
	input_type = 'date'

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username','email']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('username', css_class='form-group col-md-6 mb-0'),
				Column('email', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <div class="form-group text-right"><button class="btn btn-sm btn-success" type="submit">Save <i class="fa fa-save"></i></button> """),
			HTML(""" <span class="btn btn-sm btn-secondary"  onclick=self.history.back()><i class="fa close"></i> Cancel</span></div> """)
		)

class ProfileUpdateForm(forms.ModelForm):
	dob = forms.DateField(label='Data Moris', widget=DateInput())
	class Meta:
		model = Profile
		fields = ['firstname','lastname','dob','pob','sex']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('firstname', css_class='form-group col-md-6 mb-0'),
				Column('lastname', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('sex', css_class='form-group col-md-4 mb-0'),
				Column('pob', css_class='form-group col-md-4 mb-0'),
				Column('dob', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),

			HTML(""" <div class="form-group text-right"><button class="btn btn-sm btn-success" type="submit">Save <i class="fa fa-save"></i></button> """),
			HTML(""" <span class="btn btn-sm btn-secondary"  onclick=self.history.back()><i class="fa close"></i> Cancel</span></div> """)
		)

class PhotoProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('image', css_class='form-group col-md-6 mb-0', onchange="myFunction()"),
				css_class='form-row'
			),
			HTML(""" <center> <img id='output' width='200' /> </center> """),
			HTML(""" <div class="form-group text-right"><button class="btn btn-sm btn-success" type="submit">Save <i class="fa fa-save"></i></button> """),
			HTML(""" <span class="btn btn-sm btn-secondary"  onclick=self.history.back()><i class="fa close"></i> Cancel</span></div> """)
		)

