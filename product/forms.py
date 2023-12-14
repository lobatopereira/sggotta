from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.contrib.auth.models import Group,User
from product.models import Product,ProductUnit,ProductTransaction

class DateInput(forms.DateInput):
	input_type = 'date'


class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['name','volume','image','is_active']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['name'].required = True
		self.fields['volume'].required = True
		self.fields['image'].required = True
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-6 mb-0'),
				Column('volume', css_class='form-group col-md-6 mb-0'),
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

class ProductUnitForm(forms.ModelForm):
	class Meta:
		model = ProductUnit
		fields = ['unit','is_active','price']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['unit'].required = True
		self.fields['price'].required = True
		self.helper.layout = Layout(
			Row(
				Column('unit', css_class='form-group col-md-4 mb-0'),
				Column('price', css_class='form-group col-md-4 mb-0'),
				Column('is_active', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <div class="form-group text-right"><button class="btn btn-sm btn-info" type="submit">Save <i class="fa fa-save"></i></button> """),
			HTML(""" <span class="btn btn-sm btn-secondary"  onclick=self.history.back()><i class="fa close"></i> Cancel</span></div> """)
		)

class ProductTransactionForm(forms.ModelForm):
	date = forms.DateField(label='Data Produsaun', widget=DateInput())
	class Meta:
		model = ProductTransaction
		fields = ['total_in','date']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['date'].required = True
		self.fields['total_in'].required = True
		self.helper.layout = Layout(
			Row(
				Column('date', css_class='form-group col-md-4 mb-0'),
				Column('total_in', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <div class="form-group text-left"><button class="btn btn-sm btn-info" type="submit">Save <i class="fa fa-save"></i></button> """),
			HTML(""" <span class="btn btn-sm btn-secondary"  onclick=self.history.back()><i class="fa close"></i> Cancel</span></div> """)
		)