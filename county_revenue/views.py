from django.shortcuts import render, redirect
from .forms import NewUserForm,CountyCustomerForm, EnterpriseForm, ServiceForm, RevenueForm
from .models import CountyCustomer, Enterprise, Service , Revenue
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate 
from django.contrib import messages
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
# Create your views here.

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			print('it was a valid submission')
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect('county_customer')
		else:
			print('invalid submission, aborting')
			return render(request=request, template_name="login.html", context={"login_form":form})

		
			
		messages.error(request,"Invalid username or password.")
	
		messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})


def register_request(request):
	if request.method == "POST":
		
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			print(f'the user {user} saved successfully')
			messages.success(request, "Thanks for registering. Pleaselogin to continue." )
		else:
			return render (request=request, template_name="register.html", context={"register_form":form})

		return redirect('login')
	messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})
def logout_user(request):
    logout(request)
    messages.success(request, "Thanks You for Reporting!", extra_tags='alert alert-warning alert-dismissible fade show')

    return redirect('/')

def index(request):
	# return redirect(reverse('category'))
    return render(request, 'home.html')
@login_required
def create_county_customer(request):
    if request.method == 'POST':
        form = CountyCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enterprise.html/')
    else:
        form = CountyCustomerForm()
    
    return render(request, 'county_customer.html', {'form': form})
@login_required
def create_enterprise(request):
    if request.method == 'POST':
        form = EnterpriseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enterprise_list')
    else:
        form = EnterpriseForm()
    
    return render(request, 'enterprise.html', {'form': form})
@login_required
def enterprise_list(request):
    enterprises = Enterprise.objects.all()
    return render(request, 'enterprise_list.html', {'enterprises': enterprises})
@login_required

def county_customer_list(request):
    county_customers = CountyCustomer.objects.all()
    return render(request, 'county_customer_list.html', {'county_customers': county_customers})
@login_required
def enterprise_list(request):
    enterprises = Enterprise.objects.all()
    return render(request, 'enterprise_list.html', {'enterprises': enterprises})
@login_required
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    
    return render(request, 'service.html', {'form': form})
@login_required
def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})
from django.shortcuts import render, redirect
from .forms import InvoiceForm
from .models import Invoice
@login_required

def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm()
    
    return render(request, 'invoice.html', {'form': form})
@login_required

def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoice_list.html', {'invoices': invoices})
from .models import Defaulter
@login_required
def track_defaulters(request):
    defaulters = Revenue.objects.filter(payment_status=False)
    #defaulters=Defaulter.objects.all()
    return render(request, 'track_defaulters.html', {'defaulters': defaulters})
def system_report(request):
    reports = Revenue.objects.all()
    #defaulters=Defaulter.objects.all()
    return render(request, 'pdf.html', {'reports': reports})

@login_required
def create_revenue(request):
    if request.method == 'POST':
        form = RevenueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('revenue_list')
    else:
        form = RevenueForm()
    
    return render(request, 'revenue.html', {'form': form})
@login_required
def revenue_list(request):
    revenues = Revenue.objects.all()
    return render(request, 'revenue_list.html', {'revenues': revenues})
@login_required
def facilitate_payment(request, revenue_id):
    revenue = Revenue.objects.get(pk=revenue_id)
    revenue.payment_status = True
    revenue.save()
    return redirect('revenue_list')


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = context_dict
    html  = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % html)
def pdf(request):
    #Retrieve data or whatever you need
	results = []

	for report in Revenue.objects.all():
		data = {

		}
		print(report.id)
		data['county_customer'] = report.county_customer
		data['enterprise'] = report.enterprise
		data['service'] = report.service
		data['payment_status'] = report.payment_status
        
        
		
		results.append(data)

	
	return render_to_pdf(
	'pdf.html',
	{
	'pagesize':'A4',
	'data': results,
	}
	)