import random
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from .models import User,Product

# Create your views here.
def landing(req):                                           #For Landing
    return render(req, 'landing.html')

def login(req):                                             #For Login
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


def register(req):                                          #For Register
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
            send_mail(
                        'Account Created Successfully',
                        f'Hello {n}, your account has been created successfully!',
                        'roushanrajput12362@gmail.com',
                        [e]
                    )
            new_user.save()
            return redirect('login')
    return render(req, 'register.html')

def admindash(req):                                            #For adminDashboard
    if not req.session.get("admin"):
        return redirect("login")
    return render(req, "admindash.html")


def dashboard(req):                                            #For Dashboard Switching
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

def logout(req):                                        #FOr Logout Logics 
    req.session.flush()
    return redirect("login")

def forgetpass(req):                                    #For Forget password method 
    if req.method == 'POST':
        e = req.POST.get('Email')
        # print('email:', e)
        req.session['email']=e

        otp = random.randint(1111, 9999)
        req.session['classotp'] =otp
        send_mail(
            'OTP Verification for Forget password',
            f'Generate OTP for django app is {otp}',
            'roushanrajput12362@gmail.com',
            [e]
        )
        # print('otp send successfully!!!')
        return render(req, 'verifyotp.html')
    return render(req, 'forgetpass.html')


def passwordreset(req):                                    #For Resetting password method
    return render(req, 'passwordreset.html')

def verifyotp(req):                                    #For Verifying OTP method 
    if req.method == "POST":
        user_otp = int(req.POST.get("otp"))
        sent_otp = int(req.session.get("classotp"))
        print("User OTP:", repr(user_otp), type(user_otp))
        print("Sent OTP:", repr(sent_otp), type(sent_otp))
        print("Equal:", user_otp == sent_otp)
        if sent_otp is None:
            return render(req, "verifyotp.html", {
                "error": "OTP expired. Please request a new OTP."
            })
        if user_otp == sent_otp:
            print("OTP verified successfully!")
            return redirect('passwordreset')
        else:
            print("Invalid OTP")
            

def passwordreset(req):
    email = req.session.get("reset_email")
    if email is None:
        return redirect("forgetpass")
    if req.method == "POST":
        new_password = req.POST.get("new_password")
        confirm_password = req.POST.get("confirm_password")
        if new_password == confirm_password:
            user = User.objects.get(useremail=email)
            user.userpassword = new_password
            user.userconfirmpassword = confirm_password
            user.save()
            # Session clear kar do
            req.session.pop("otp", None)
            req.session.pop("reset_email", None)
            return redirect("login")
        else:
            return render(req, "password_reset.html", {
                "error": "Passwords do not match"
            })
    return render(req, "passwordreset.html")


def addpro(req):                                        #For Adding Product Logics 
    if not req.session.get("admin"):
        return redirect("login")

    if req.method == "POST":
        productname = req.POST.get("productname")
        productdescription = req.POST.get("productdescription")
        productprice = req.POST.get("productprice")
        productimage = req.FILES.get("productimage")

        new_product = Product(
            productname=productname,
            productdescription=productdescription,
            productprice=productprice,
            productimage=productimage
        )
        send_mail(
            'Product Added Successfully',
            f'Hello Admin, the product "{productname}" has been added successfully!',
            'roushanrajput12362@gmail.com',
            ['admin@gmail.com']
        )

        new_product.save()
        
        return redirect("allpro")

    return render(
        req,
        "addpro.html"
    )



def editpro(req, product_id):                              #For Editing product details logics 
    if not req.session.get("admin"):
        return redirect("login")
    product = Product.objects.get(id=product_id)
    if req.method == "POST":
        product.productname = req.POST.get("productname")
        product.productdescription = req.POST.get("productdescription")
        product.productprice = req.POST.get("productprice")

        if req.FILES.get("productimage"):
            product.productimage = req.FILES.get("productimage")
        product.save()
        return redirect("allpro")
    
    return render(
        req,
        "addpro.html",
        {
            "product": product
        }
    )



def allpro(req):                                           #For showing all products logics 
    products = Product.objects.all()

    is_admin = req.session.get("admin", False)

    user_id = req.session.get("user_id")

    if not is_admin and not user_id:
        return redirect("login")
    return render(
        req,
        "allpro.html",
        {
            "products": products,
            "is_admin": is_admin
        }
    )



def deletepro(req, product_id):                        #For  Delecting product logics
    if not req.session.get("admin"):
        return redirect("login")
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('allpro')