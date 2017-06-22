from django.shortcuts import render
import shopify
from shopify_app.decorators import shop_login_required
from .forms import ExportForm, UploadFileForm
import unicodecsv as csv
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, View
from django.contrib import messages


def welcome(request):
    return render(request, 'home/welcome.html', {
        'callback_url': "http://%s/login/finalize" % (request.get_host()),
    })


@shop_login_required
def index(request):
    products = shopify.Product.find(limit=3)
    orders = shopify.Order.find(order="created_at DESC", status='any')
    return render(request, 'home/index.html', {
        'products': products,
        'orders': orders,
    })


@shop_login_required
def export_csv(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # If we doing export

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        # create a form instance and populate it with data from the request:
        ex_form = ExportForm(request.POST)
        orders = shopify.Order.find(order="created_at ASC", status='any')
        orders_list = []
        for order in orders:
            orders_list.append(order.to_dict())

        # with open('orders.csv', 'wb') as output_file:
        keys = orders_list[0].keys()
        dict_writer = csv.DictWriter(response, keys)
        dict_writer.writeheader()
        dict_writer.writerows(orders_list)

        # check whether it's valid:
        if ex_form.is_valid():
            return response

    # if a GET (or any other method) we'll create a blank form
    else:
        ex_form = ExportForm()

    return render(request, 'home/export.html', {'ex_form': ex_form})


@shop_login_required
def import_csv(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            r = request.FILES['file']
            list_of_rows = [{k: v for k, v in row.items()} for row in csv.DictReader(r, skipinitialspace=True)]
            add_tracking(list_of_rows)
            return HttpResponseRedirect(reverse('root_import'))
    else:
        form = UploadFileForm()

    return render(request, 'home/import.html', {'form': form})


def add_tracking(list_of_rows):
    """
    products = shopify.Product.find(limit=3)
    orders = shopify.Order.find(order="created_at DESC", status='any')
    fulfill = shopify.Fulfillment.find(order_id=5704067220)[0]

    fulfill.tracking_numbers = ['00000000000']
    shopify.Fulfillment.save(fulfill)
    return render(request, 'home/index.html', {
        'products': products,
        'orders': orders,
    })
    """
    for row in list_of_rows:
        tracking_id = row.get('tracking_id')
        order_id = row.get('id')
        print(tracking_id)
        if tracking_id:
            fulfill = shopify.Fulfillment.find(order_id=order_id)
            if len(fulfill) > 0:
                # update
                fulfill = shopify.Fulfillment.find(order_id=order_id)[0]
                fulfill.tracking_numbers = [tracking_id]
                shopify.Fulfillment.save(fulfill)
            else:
                # create new
                fulfill = shopify.Fulfillment(prefix_options=dict(order_id=order_id))
                fulfill.tracking_numbers = [tracking_id]
                fulfill.save()


class MixedView(View):
    template_name = 'home/mix.html'
    form_class1 = ExportForm
    form_class2 = UploadFileForm

    def get(self, request):
        form1 = self.form_class1(None)
        form2 = self.form_class2(None)
        return render(request, self.template_name, {'export': form1, 'import': form2, })

    def post(self, request):
        if request.method == 'POST' and 'export' in request.POST:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="orders.csv"'
            # create a form instance and populate it with data from the request:
            ex_form = ExportForm(request.POST)
            orders = shopify.Order.find(order="created_at ASC", status='any')
            orders_list = []
            for order in orders:
                orders_list.append(order.to_dict())

            # with open('orders.csv', 'wb') as output_file:
            keys = orders_list[0].keys()
            dict_writer = csv.DictWriter(response, keys)
            dict_writer.writeheader()
            dict_writer.writerows(orders_list)

            # check whether it's valid:
            if ex_form.is_valid():
                return response
        if request.method == 'POST' and 'import' in request.POST:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                r = request.FILES['file']
                list_of_rows = [{k: v for k, v in row.items()} for row in csv.DictReader(r, skipinitialspace=True)]
                add_tracking(list_of_rows)
                messages.info(request, "Successfully uploaded")
                return render(request, self.template_name, {'export': self.form_class1(None), 'import': self.form_class2(None)})
        return render(request, self.template_name,
                      {'export': self.form_class1(None), 'import': self.form_class2(None)})


def design(request):
    return render(request, 'home/design.html', {})
