from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.contrib.auth.models import Group,User
from client.models import Client

class DateInput(forms.DateInput):
	input_type = 'date'


class ClientForm(forms.ModelForm):
	dob = forms.DateField(label='Data Moris', widget=DateInput(), required=False)
	class Meta:
		model = Client
		fields = ['firstname','lastname','pob','dob','sex','address','phone','image','is_active','municipality','administrativepost','village']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['firstname'].required = True
		self.fields['lastname'].required = True
		self.fields['phone'].required = True
		self.fields['address'].required = True
		self.fields['municipality'].required = True
		self.fields['administrativepost'].required = True
		self.fields['village'].required = True
		self.helper.layout = Layout(
			Row(
				Column('firstname', css_class='form-group col-md-4 mb-0'),
				Column('lastname', css_class='form-group col-md-4 mb-0'),
				Column('sex', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('pob', css_class='form-group col-md-6 mb-0'),
				Column('dob', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <hr> <b>Hela Fatin Atual</b> <hr> """),
			Row(
				Column('municipality', css_class='form-group col-sm-4 mb-0'),
				Column('administrativepost', css_class='form-group col-sm-4 mb-0'),
				Column('village', css_class='form-group col-sm-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('address', css_class='form-group col-md-6 mb-0'),
				Column('phone', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('is_active', css_class='form-group col-md-6 mb-0'),
				Column('image', css_class='form-group col-md-6 mb-0', onchange="myFunction()"),
				css_class='form-row'
			),
			HTML(""" <center> <img id='output' width='200' /> </center> """),
			HTML(""" <div class="form-group text-right"><button class="btn btn-sm btn-info" type="submit">Save <i class="fa fa-save"></i></button> """),
			HTML(""" <span class="btn btn-sm btn-secondary"  onclick=self.history.back()><i class="fa close"></i> Cancel</span></div> """)
		)
