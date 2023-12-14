from django.urls import path
from charts.api import views


urlpatterns = [
    path('g/product/stock/', views.APIGProductStock.as_view(), name="api-g-product-stock"),
    path('g/product/summury/', views.APIGProductSumm.as_view(), name="api-g-product-summury"),

    # report
    path('g/product/summury/chart/all/time/', views.APIGProductSummAll.as_view(), name="api-g-product-summury-all"),
    path('g/product/report/summury/by-month/this-year', views.APIGProductSummByMonthThisYear.as_view(), name="api-g-product-report-summury-month-this-year"),
    path('g/distribution/report/summury/by-month/this-year', views.APIGDistributionSummByMonthThisYear.as_view(), name="api-g-distribution-report-summury-month-this-year"),
    
    path('g/distribution/report/summury/by-month/this-year/total-price/', views.APIGDistributionSummByMonthThisYearPrice.as_view(), name="APIGDistributionSummByMonthThisYearPrice"),

    path('g/product/report/summury/by-year', views.APIGProductSummByYear.as_view(), name="api-g-product-report-summury-by-year"),
    path('g/distribution/report/summury/by-year', views.APIGDistributionSummByYear.as_view(), name="api-g-distribution-report-summury-by-year"),


 
]