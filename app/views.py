# from django.db.models import Model
from django.shortcuts import redirect, render
from .models import User,Product

# Create your views here.
def landing(req):
    return render(req, 'landing.html')

def login(req):
    if req.method == 'POST':

        e = req.POST.get('email')

        p = req.POST.get('password')


        # ADMIN LOGIN

        if e == 'admin@gmail.com' and p == 'admin':

            req.session["admin"] = True

            return redirect(
                'admindash'
            )


        user = User.objects.filter(

            useremail=e

        )


        if not user.exists():

            message = 'User does not exist'

            print(user)

            return render(

                req,

                'login.html',

                {

                    'error': message

                }

            )


        else:

            user_data = User.objects.get(

                useremail=e

            )


            if p == user_data.userpassword:

                req.session["user_id"] = user_data.id

                return redirect(
                    'dashboard'
                )


            else:

                message = 'Incorrect password'

                return render(

                    req,

                    'login.html',

                    {

                        'error': message

                    }

                )


    return render(

        req,

        'login.html'

    )


def register(req):
    if req.method == 'POST':
        n = req.POST.get('username')
        e = req.POST.get('useremail')
        c = req.POST.get('usercontact')
        g = req.POST.get('usergender')
        pr = req.FILES.get('userprofile')
        p = req.POST.get('userpassword')
        cp = req.POST.get('userconfirmpassword')

        user=User.objects.filter(useremail=e)       
        if user.exists():
            message = 'User already exists'
            return render(req, 'register.html', {'error': message})
        else:
            new_user=User(username=n,useremail=e,usercontact=c,usergender=g,userprofile=pr,userpassword=p,userconfirmpassword=cp)
            new_user.save()
            return redirect('login')
    return render(req, 'register.html')

def admindash(req):
    if not req.session.get("admin"):
        return redirect("login")
    return render(req, "admindash.html")

def dashboard(req):

    user_id = req.session.get("user_id")

    if not user_id:

        return redirect("login")

    user = User.objects.get(
        id=user_id
    )

    return render(
        req,
        "dashboard.html",
        {
            "user": user
        }
    )

def logout(req):
    req.session.flush()
    return redirect("login")

def addpro(req):
    if req.method == 'POST':
        productname = req.POST.get('productname')
        productdescription = req.POST.get('productdescription')
        productprice = req.POST.get('productprice')
        productimage = req.FILES.get('productimage')

        new_product = Product(
            productname=productname,productdescription=productdescription,productprice=productprice,productimage=productimage)
        new_product.save()
        return redirect('admindash')
    return render(req, 'addpro.html')


def allpro(req):
    products = Product.objects.all()
    return render(req, 'allpro.html', {'products': products})
