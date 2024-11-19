from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Unit, Category, Inventory

from .forms import AddProductForm, AddCategoryForm, UpdateProductForm, AddUnitForm
from  django.contrib import messages
from django_pandas.io import read_frame
import plotly
import plotly.express as px
import json





"""authentication logic"""
def loginUser(request):

    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user does'nt exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, "username or password incorrect")
    context = {'page':page}
    return render(request, 'authentication/auth.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
   
    form = UserCreationForm()

    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.username = user.username.lower()
            user.save()
            return redirect('login')
        else:
            messages.error(request, "error occurred during registration")
    context = {'form':form}
    return render(request, 'authentication/auth.html', context)


"""main system logic """
@login_required(login_url='login')
def index(request):

    context = {'title': 'index page'}
    return render(request, 'inventory/index.html', context)

@login_required(login_url='login')
def store_list(request):
    inventories = Inventory.objects.all()

    context = {
        'title':'products',
        'inventories': inventories
        }
    return render(request, 'inventory/store_list.html', context)


@login_required(login_url='login')
def per_product(request, pk):
    inventory = get_object_or_404(Inventory, pk = pk)
    context = {
        'inventory':inventory
    }

    return render(request, 'inventory/per_product.html', context)


"""crud operations"""
@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        add_form = AddProductForm(data=request.POST)
        if add_form.is_valid():
            new_inventory = add_form.save(commit=False)
            quantity_sold = int(add_form.cleaned_data['quantity_sold'])
            sell_price = float(add_form.cleaned_data['sell_price'])
            buy_price = float(add_form.cleaned_data['buy_price'])
            quantity_in_stock = int(add_form.cleaned_data['quantity_in_stock'])
            
            new_inventory.sales = sell_price * quantity_sold
            #new_inventory.profit_loss = sell_price - buy_price
            new_inventory.profit_loss = (sell_price - buy_price) * quantity_sold
            new_inventory.quantity_remaining = quantity_in_stock - quantity_sold
            new_inventory.save()

            
            
            messages.success(request, "Successfully added a product")
            return redirect('store')
        
    else:
        add_form = AddProductForm()
    context = {"form":add_form}
    return render(request, 'inventory/add_product.html', context)



@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        add_category = AddCategoryForm(data=request.POST)
        if add_category.is_valid():
            new_category = add_category.save(commit=False)
            new_category.save()
            return redirect('store')
    else:
        add_category = AddCategoryForm()
    context = {"categoryform":add_category}
    return render(request, 'inventory/add_category.html', context)

@login_required(login_url='login')
def add_unit(request):
    if request.method =='POST':
        add_unit = AddUnitForm(data=request.POST)
        if add_unit.is_valid():
            new_unit = add_unit.save(commit=False)
            new_unit.save()
            return redirect ('store')
    else:
        add_unit = AddUnitForm()
    context = {"unitForm": add_unit}
    return render(request, 'inventory/add_unit.html', context)
        


@login_required(login_url='login')
def delete_product(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.danger(request, "product deleted")
    return redirect('store')

@login_required(login_url='login')
def update_product(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
  
    if request.method == 'POST':
        updateForm = UpdateProductForm(data=request.POST, instance=inventory)
        if updateForm.is_valid():
            inventory.name = updateForm.cleaned_data['name']
            inventory.category = updateForm.cleaned_data['category']
            inventory.unit = updateForm.cleaned_data['unit']
            inventory.quantity_in_stock = updateForm.cleaned_data['quantity_in_stock']
            inventory.quantity_sold = updateForm.cleaned_data['quantity_sold']
            inventory.buy_price = updateForm.cleaned_data['buy_price']
            inventory.sell_price = updateForm.cleaned_data['sell_price']
            inventory.stock_alert = updateForm.cleaned_data['stock_alert']
            
            inventory.sales = float(inventory.sell_price) * float(inventory.quantity_sold)
            inventory.quantity_remaining = int(inventory.quantity_in_stock) - int(inventory.quantity_sold)
            inventory.profit_loss = (inventory.sell_price - inventory.buy_price) * inventory.quantity_sold
            inventory.save()

            messages.success(request, "product updated")

            if inventory.quantity_remaining <= inventory.stock_alert:
             messages.warning(request, f"Warning: The stock for {inventory.name} is low! Only {inventory.quantity_remaining} remaining.")

            return redirect('store')
    else:
        updateForm = UpdateProductForm(instance=inventory)
    context = {"updateForm": updateForm}
    
    return render(request, 'inventory/update_product.html', context)


"""visualization"""
@login_required(login_url='login')
def dashboard(request):
    inventories = Inventory.objects.all()

    df = read_frame(inventories)

    """bar graph for the most sold product"""
    most_sold_product_df = df.groupby(by="name")[['quantity_sold']].sum().sort_values(by="quantity_sold")
    most_sold_product = px.bar(most_sold_product_df, 
                                            x = most_sold_product_df.index,
                                            y = most_sold_product_df.quantity_sold,
                                            title = "best performing product"
                                         )
    
    most_sold_product = json.dumps(most_sold_product, cls = plotly.utils.PlotlyJSONEncoder)

    """bar graph for most stocked products"""
    most_stocked_products_df = df.groupby(by="name")[['quantity_in_stock']].sum().sort_values(by="quantity_in_stock")
    most_stocked_products = px.bar(most_stocked_products_df,
                                          x = most_stocked_products_df.index,
                                          y = most_stocked_products_df.quantity_in_stock,
                                          title = "most stocked products"
                                          )
    most_stocked_products = json.dumps(most_stocked_products, cls=plotly.utils.PlotlyJSONEncoder)


    """pie chart for the most product in stock"""
    most_in_stock_df = df.groupby(by="name")[['quantity_remaining']].sum().sort_values(by="quantity_remaining")
    most_in_stock = px.pie(most_in_stock_df,
                                    names=most_in_stock_df.index,
                                    values=most_in_stock_df.quantity_remaining,
                                    title="most products remaining in stock"
                           )
    most_in_stock = json.dumps(most_in_stock, cls = plotly.utils.PlotlyJSONEncoder)

     # Profit/Loss Bar Graph
    df['profit_loss'] = (df['sell_price'] - df['buy_price']) * df['quantity_sold']
    profit_loss_df = df.groupby(by="name")[['profit_loss']].sum().sort_values(by="profit_loss")
    profit_loss_chart = px.bar(profit_loss_df, 
                               x=profit_loss_df.index, 
                               y='profit_loss', 
                               title="Profit/Loss per Product"
                               )
    profit_loss_chart = json.dumps(profit_loss_chart, cls=plotly.utils.PlotlyJSONEncoder)



    context = {
        "most_sold_product": most_sold_product,
        "most_in_stock":most_in_stock,  
        "most_stocked_products": most_stocked_products,
        "profit_loss_chart": profit_loss_chart

    }

    return render(request, "inventory/dashboard.html", context)
