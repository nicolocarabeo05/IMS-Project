from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
from .enums import OrderStatus, Category
from django.db.models import Q

# Create your views here.


@login_required
def index(request):
    orders = Order.objects.order_by("-order_date")
    products = Product.objects.all()
    orders_count = orders.count()
    product_count = Product.objects.all().count()
    workers_count = User.objects.all().count()

    product = request.GET.get('product')
    category = request.GET.get('category')
    status = request.GET.get('status')
    order_date = request.GET.get('order_date')

    if product:
        orders = orders.filter(product__name__icontains=product)

    if category and category != "All":
        orders = orders.filter(product__category=category)

    if status and status != "All":
        orders = orders.filter(status=status)

    if order_date:
        orders = orders.filter(order_date__date=order_date)


    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            product = instance.product

            if product.quantity <= 0:
                messages.error(request, "Product is out of stock.")
                return redirect("dashboard-index")

            if product.quantity >= instance.order_quantity:

                product.quantity -= instance.order_quantity
                product.save()

                instance.staff = request.user
                instance.status = "Processing"
                instance.save()

                return redirect("dashboard-index")

            else:
                messages.error(request, "Not enough stock available.")
                return redirect("dashboard-index")

    else:
        form = OrderForm()

    context = {
        "orders": orders,
        "form": form,
        "products": products,
        "orders_count": orders_count,
        "product_count": product_count,
        "workers_count": workers_count,

        "category_choices": Category.choices,
        "status_choices": OrderStatus.choices,
    }
    return render(request, "dashboard/index.html", context)


@login_required
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders = Order.objects.filter(staff=request.user).order_by("-order_date")
    orders_count = orders.count()
    product_count = Product.objects.all().count()

    product = request.GET.get('product')
    category = request.GET.get('category')
    status = request.GET.get('status')
    order_date = request.GET.get('order_date')

    if product:
        orders = orders.filter(product__name__icontains=product)

    if category and category != "All":
        orders = orders.filter(product__category=category)

    if status and status != "All":
        orders = orders.filter(status=status)

    if order_date:
        orders = orders.filter(order_date__date=order_date)

    context = {
        "workers": workers,
        "workers_count": workers_count,
        "orders": orders,
        "orders_count": orders_count,
        "product_count": product_count,

        "category_choices": Category.choices,
        "status_choices": OrderStatus.choices,
    }
    return render(request, "dashboard/staff.html", context)


@login_required
def staff_details(request, pk):
    workers = User.objects.get(id=pk)
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()
    product_count = Product.objects.all().count()

    context = {
        "workers": workers,
        "workers_count": workers_count,
        "orders_count": orders_count,
        "product_count": product_count,
    }
    return render(request, "dashboard/staff_details.html", context)


@login_required
def product(request):
    items = Product.objects.all()
    product_count = Product.objects.all().count()
    orders = Order.objects.all()
    orders_count = orders.count()
    workers = User.objects.all()
    workers_count = workers.count()

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get("name")
            messages.success(request, f"{product_name} has been added successfully!")
            return redirect("dashboard-product")
    else:
        form = ProductForm()
    context = {
        "items": items,
        "form": form,
        "workers": workers,
        "workers_count": workers_count,
        "orders": orders,
        "orders_count": orders_count,
        "products": items,
        "product_count": product_count,
    }
    return render(request, "dashboard/product.html", context)


@login_required
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect("dashboard-product")
    return render(request, "dashboard/product_delete.html")


@login_required
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-product")
    else:
        form = ProductForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/product_update.html", context)


@login_required
def order(request):
    orders = Order.objects.order_by("-order_date")
    orders_count = orders.count()
    workers = User.objects.all()
    workers_count = workers.count()
    items = Product.objects.all()
    product_count = items.count()

    product = request.GET.get('product')
    category = request.GET.get('category')
    status = request.GET.get('status')
    order_date = request.GET.get('order_date')

    if product:
        orders = orders.filter(product__name__icontains=product)

    if category and category != "All":
        orders = orders.filter(product__category=category)

    if status and status != "All":
        orders = orders.filter(status=status)

    if order_date:
        orders = orders.filter(order_date__date=order_date)

    context = {
        "orders": orders,
        "orders_count": orders_count,
        "workers": workers,
        "workers_count": workers_count,
        "products": items,
        "product_count": product_count,
        "category_choices": Category.choices,
        "status_choices": OrderStatus.choices,
    }
    return render(request, "dashboard/order.html", context)


@login_required
def cancel_order(request, pk):
    order = Order.objects.get(id=pk)

    if order.status != OrderStatus.CANCELLED:
        product = order.product

        product.quantity += order.order_quantity
        product.save()

        order.status = OrderStatus.CANCELLED
        order.save()

    return redirect("dashboard-order")

@login_required
def update_order_status(request, pk, status):
    order = Order.objects.get(id=pk)

    if order.status in [
        OrderStatus.CANCELLED,
        OrderStatus.DELIVERED
    ]:
        return redirect("dashboard-order")

    if status == "for_delivery":
        order.status = OrderStatus.FOR_DELIVERY

    elif status == "delivered":
        order.status = OrderStatus.DELIVERED

    order.save()

    return redirect("dashboard-order")

@login_required
def staff_cancel_order(request, pk):
    order = Order.objects.get(id=pk)

    if order.status == OrderStatus.PROCESSING:
        product = order.product

        product.quantity += order.order_quantity
        product.save()

        order.status = OrderStatus.CANCELLED
        order.save()

    return redirect("dashboard-index")