from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.http import JsonResponse, Http404
from . import models
from .forms import UserOrderForm, AdminOrderForm
from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404

class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

class Index(View):
    def get(self,request):
        products = models.Product.objects.all()
        if not request.user.is_authenticated:
            context = {
            "products":products,
            'user_basket_id':'',
            'products_in_basket':''}
            return render(request, 'Lab1/index.html',context=context)
        user_id = request.user.id
        user_basket = None
        try:
            user_basket = models.Basket.objects.get(user=user_id)

        except models.Basket.DoesNotExist:
            basket = models.Basket(user=request.user)
            basket.save()
            user_basket = basket

        is_basket_ordered = user_basket.in_order
        products_in_basket = [item['product_id'] for item in user_basket.products.values()]
        context = {
        "products":products,
        'user_basket_id':user_basket.id,
        'is_basket_ordered':is_basket_ordered,
        'products_in_basket':products_in_basket}
        return render(request, 'Lab1/index.html',context=context)
        # else:
        #     url = '/accounts/login/?next={}'.format(request.path)
        #     return redirect(url)

class BasketControl(View):
    def post(self,request):
        if request.is_ajax():
            print('ajax method!')
            # username = None
            if request.user.is_authenticated:
                user = request.user
                type = request.POST.get('type', None)
                product_id = request.POST.get('product_id', None)
                product_amount = request.POST.get('amount', 1)
                basket_id = request.POST.get('basket_id', None)
                print(basket_id)
                user_basket = models.Basket.objects.get(id=basket_id)
                try:
                    product = models.Product.objects.get(id=product_id)
                    # raise ValidationError('Такой новострой уже существует.')
                except models.Product.DoesNotExist:
                    raise Http404

                # user_basket = None
                # try:
                #     user_basket = models.Basket.objects.get(user=user.id)
                #     # raise ValidationError('Такой новострой уже существует.')
                # except models.Basket.DoesNotExist:
                #     basket = Basket(user=user)
                #     basket.save()
                #     user_basket = basket
                if type == 'add':
                    be = models.BasketElement(user=user,product=product,amount=product_amount)
                    be.save()
                    user_basket.products.add(be)
                    response = JsonResponse({'message':'Product is added'})
                    response.status_code = 200 # To announce that the user isn't allowed to publish
                    return response
                elif type == 'delete':
                    try:
                        models.BasketElement.objects.get(user=user.id,product=product_id).delete()
                    except models.Product.DoesNotExist:
                        raise Http404

                    response = JsonResponse({'message':'Product is deleted'})
                    response.status_code = 200 # To announce that the user isn't allowed to publish
                    return response
                    # models.BasketElement(user=user,product=product,amount=product_quantity).delete()
            else:
                response = JsonResponse({'message':'Not authenticated'})
                response.status_code = 401 # To announce that the user isn't allowed to publish
                return response
                # url = "/accounts/login/?next=''"
                # return redirect(url)
        else:
            raise Http404

class UserBasket(View):
    def get(self,request):
        if request.user.is_authenticated:
            basket = models.Basket.objects.get(user = request.user.id)
            order_form = UserOrderForm(initial={'basket': basket})
            # common_price = 0
            # for basket_item in basket.products.all():
            #     common_price += basket_item.product.price * basket_item.amount
            context = {
                'basket' : basket,
                'order_form' : order_form,
                'initial_common_price' : basket.calculate_common_price()
            }
            return render(request,'Lab1/basket.html',context=context)
        else:
            raise Http404

    def post(self,request):
        if request.user.is_authenticated:
            print('get post ')
            basket = models.Basket.objects.get(user = request.user.id)

            # print("BASKET:  ",basket)
            # request.POST['basket'] = basket
            # order_form = UserOrderForm()
            order_form = UserOrderForm(request.POST or None)

            if order_form.is_valid():
                print('INITIAL CLEANED DATA', order_form.cleaned_data)
                if order_form.cleaned_data['basket'].id != basket.id:
                    raise Http404
                order_form.save()
                # order.save()
                basket.in_order = True
                basket.save()
                return redirect('user_basket')
            else:
                print(order_form.errors)
        else:
            raise Http404

class DeleteOrder(View):
    def post(self,request):
        if request.user.is_authenticated:
            basket = models.Basket.objects.get(user = request.user.id)
            models.Order.objects.get(basket = basket).delete()
            basket.in_order = False
            basket.save()
            return redirect('user_basket')
            # print("BASKET:  ",basket)
            # request.POST['basket'] = basket
            # order_form = UserOrderForm()
            # order_form = UserOrderForm(request.POST or None)

            # if order_form.is_valid():
            #     print('INITIAL CLEANED DATA', order_form.cleaned_data)
            #     if order_form.cleaned_data['basket'].id != basket.id:
            #         raise Http404
            #     order = order_form.save()
            #     order.save()
            #     basket.in_order = True
            #     basket.save()
            #     return redirect('order-success')

        else:
            raise Http404

    # def delete(self,request):
    #     return redirect('order-success')

class GetNewCommonPrice(View):
    def get(self,request):
        if request.is_ajax():
            print('ajax method!')
            if request.user.is_authenticated:
                user = request.user
                basket_id = request.GET.get('basket_id', None)
                user_basket = models.Basket.objects.get(id = basket_id)
                response = JsonResponse({'common_price' : user_basket.calculate_common_price()})
                response.status_code = 200 # To announce that the user isn't allowed to publish
                return response
            else:
                raise Http404

        else:
            raise Http404

class AdminOrders(View):
    def get(self,request):
        if request.user.is_superuser:
            orders = models.Order.objects.all()
            # order_form = UserOrderForm(initial={'basket': basket})
            # OrderFormSet = formset_factory(AdminOrderForm, extra=0)
            # orders = [(order, AdminOrderForm(instance=order)) for order in models.Order.objects.all()]
            # orders = models.Order.objects.all()

            orders_dict = dict()

            for order in orders:
                orders_dict[order.basket.user.username] = {'products':[{'name':basket_item.product.name,'price':basket_item.product.price,'amount':basket_item.amount} for basket_item in order.basket.products.all()]}
                orders_dict[order.basket.user.username].update({'form':AdminOrderForm(instance=order),'phone_number':order.phone_number,'dont_call':order.dont_call, 'common_price':order.basket.calculate_common_price(),'order_id':order.id, 'wishes':order.wishes})
            # order_formset = OrderFormSet(orders)
            # common_price = 0
            # for basket_item in basket.products.all():
            #     common_price += basket_item.product.price * basket_item.amount
            context = {
                'orders' : orders_dict,
                # 'orders'
            }
            return render(request,'Lab1/admin_orders.html',context=context)
        else:
            raise Http404

    def post(self,request):
        if request.user.is_superuser:
            print(request.POST)
            order_id = request.POST['order_id']
            order = get_object_or_404(models.Order, id=order_id)
            print("ORDER : " , order)
            order_form = AdminOrderForm(request.POST or None, instance=order)
            # try:
            #     product = models.Order.objects.get(basket=product_id)
            #     # raise ValidationError('Такой новострой уже существует.')
            # except models.Product.DoesNotExist:
            #     raise Http404
            if order_form.is_valid():
                order_form.save()
                return redirect('admin-orders')
        else:
            raise Http404
