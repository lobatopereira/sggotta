from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.contrib.auth.models import Group,User
from product.models import Product,ProductUnit,ProductTransaction
from distribution.models import ProductSell

class DateInput(forms.DateInput):
	input_type = 'date'


class ProductSellForm(forms.ModelForm):
	date = forms.DateField(label='Data Distribui', widget=DateInput())
	class Meta:
		model = ProductSell
		fields = ['date','total_out','totalprice','unit','client']
		labels={'client':'Kliente','unit':'Produtu GOTTA',}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['unit'].queryset = ProductUnit.objects.filter(productstock__total_update__gt=0)
		self.fields['total_out'].required = True
		self.fields['total_out'].widget.attrs.update({'min':0,'value':1,'oninput':"validity.valid||(value='');"})
		# self.fields['totalprice'].readonly = True
		self.fields['totalprice'].widget.attrs['readonly'] = True
		self.helper.layout = Layout(
			Row(
				Column('date', css_class='form-group col-md-4 mb-0'),
				Column('client', css_class='form-group col-md-4 mb-0'),
				Column('unit', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <div class='d-flex justify-content-end'> <div class='col-md-4' id='id_product_price'> </div> </div>"""),	
			Row(
				Column('total_out', css_class='form-group col-md-6 mb-0'),
				Column('totalprice', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <div class="form-group text-right"><button class="btn btn-sm btn-info" type="submit">Save <i class="fa fa-save"></i></button> """),
			HTML(""" <span class="btn btn-sm btn-secondary"  onclick=self.history.back()><i class="fa close"></i> Cancel</span></div> """)
		)

class ProductSellForm1(forms.ModelForm):
	date = forms.DateField(label='Data Distribui', widget=DateInput())
	class Meta:
		model = ProductSell
		fields = ['date','total_out','totalprice','client']
		labels={'client':'Kliente','unit':'Produtu GOTTA',}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['total_out'].required = True
		self.fields['total_out'].widget.attrs.update({'min':0,'value':1,'oninput':"validity.valid||(value='');"})
		self.fields['totalprice'].widget.attrs['readonly'] = True
		self.helper.layout = Layout(
			HTML(""" <div class='d-flex justify-content-begin mb-4'> Presu / {{productunit.unit}} : <b class='badge badge-warning badge-sm'>$ {{productunit.price}}</b> </div>"""),	
			Row(
				Column('date', css_class='form-group col-md-4 mb-0'),
				Column('client', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('total_out', css_class='form-group col-md-6 mb-0'),
				Column('totalprice', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <div class="form-group text-right"><button class="btn btn-sm btn-info" type="submit">Save <i class="fa fa-save"></i></button> """),
			HTML(""" <span class="btn btn-sm btn-secondary"  onclick=self.history.back()><i class="fa close"></i> Cancel</span></div> """)
		)
