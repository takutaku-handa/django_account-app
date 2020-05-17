import openpyxl
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms


class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts/login.html"


class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/create.html"
    success_url = reverse_lazy("login")


# excelシートの読み込み
book = openpyxl.load_workbook("accounts\FOOD.xlsx")
sheet = book["本表"]

# 食べ物の名前のリストを作り、番号を返す
lists_food = []
for i in range(9, 319):
    x = sheet["B" + str(i)].value
    lists_food.append(x)

# リスト集
cell = (
    "C", "D", "E", "F", "G", "H", "I", "J", "K", "W", "X", "Z", "AA", "Y", "AD", "R", "AB", "AC", "L", "M", "N", "O",
    "P",
    "Q", "S", "T", "U", "V", "AE")
nut = [2650, 60, 20, 3149, 2500, 650, 340, 1000, 7, 1.4, 1.6, 1.4, 2.4, 15, 100, 5.5, 240, 5, 850, 6.5, 8.0]
eiy = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
hyo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0]
par = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0]
list_contents = []


# 関数集
def youso(x, y):
    return sheet[cell[x] + str(y + 9)].value


def add(x, y, inn):
    if type(y) == type(None):
        pass
    elif type(y) == type("ji"):
        pass
    else:  # セルの値がintまたはfloatのときだけ計算する（でないとエラーになる）
        eiy[x] += round(float(y) * inn * 0.01, 1)


def hyouji(x):
    e = nut[x]
    p = float(eiy[x]) / e * 100
    p = round(p, 1)
    hy = str(round(eiy[x], 1))
    parcent = str(p)
    hyo[x] = hy
    par[x] = parcent


# スタート
def out(f, w):
    m = lists_food.index(f)
    inn = int(w)

    # エネルギーからパントテン酸
    for n in range(0, 18):
        add(n, youso(n, m), inn)
        hyouji(n)

        # ビタミンＡ
    for j in range(18, 24):
        add(18, youso(j, m), inn)
    hyouji(18)

    # ビタミンE
    for j in range(24, 28):
        add(19, youso(j, m), inn)
    hyouji(19)

    # 食塩相当量
    add(20, youso(28, m), inn)
    hyouji(20)


@login_required
def indexview(request):
    return render(request, 'index.html')


def outputview(request):
    food_input = request.POST["food"]
    weight_input = request.POST["weight"]
    out(food_input, weight_input)
    template = loader.get_template("output.html")
    v = food_input.replace('\u3000', ' ')
    vv = " " + v + " x " + weight_input + "g "
    list_contents.append(vv)
    context = {"food": food_input,
               "weight": weight_input,
               "list_contents": list_contents,
               "h0": hyo[0],
               "h1": hyo[1],
               "h2": hyo[2],
               "h3": hyo[3],
               "h4": hyo[4],
               "h5": hyo[5],
               "h6": hyo[6],
               "h7": hyo[7],
               "h8": hyo[8],
               "h9": hyo[9],
               "h10": hyo[10],
               "h11": hyo[11],
               "h12": hyo[12],
               "h13": hyo[13],
               "h14": hyo[14],
               "h15": hyo[15],
               "h16": hyo[16],
               "h17": hyo[17],
               "h18": hyo[18],
               "h19": hyo[19],
               "h20": hyo[20],
               "p0": par[0],
               "p1": par[1],
               "p2": par[2],
               "p3": par[3],
               "p4": par[4],
               "p5": par[5],
               "p6": par[6],
               "p7": par[7],
               "p8": par[8],
               "p9": par[9],
               "p10": par[10],
               "p11": par[11],
               "p12": par[12],
               "p13": par[13],
               "p14": par[14],
               "p15": par[15],
               "p16": par[16],
               "p17": par[17],
               "p18": par[18],
               "p19": par[19],
               "p20": par[20],
               }
    return HttpResponse(template.render(context, request))
