import openpyxl
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms
from .models import Profile


class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts/login.html"


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/create.html"
    success_url = reverse_lazy("login")


# excelシートの読み込み
book = openpyxl.load_workbook("accounts/FOOD.xlsx")
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
eiy = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, ]
hyo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
par = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
ran = ("(ex)", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,)



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
    p = 100 * float(eiy[x]) / e
    par[x] += round(p, 1)
    hyo[x] += round(eiy[x], 1)

"""
def reset():
    for i in range(0, 21):
        eiy[i] = 0.0
        hyo[i] = 0.0
        par[i] = 0.0
    foodname.clear()
    foodweight.clear()
"""

def out(f, w):
    try:
        num = lists_food.index(f)
    except ValueError:
        num = -8
    else:
        num = int(num)

    try:
        inn = int(w)
    except ValueError:
        inn = 0
    else:
        pass

    # エネルギーからパントテン酸
    for n in range(0, 18):
        add(n, youso(n, num), inn)

        # ビタミンＡ
    for j in range(18, 24):
        add(18, youso(j, num), inn)

    # ビタミンE
    for j in range(24, 28):
        add(19, youso(j, num), inn)

    # 食塩相当量
    add(20, youso(28, num), inn)


def out_out(ff, ww):
    for i in range(0, 21):
        eiy[i] = 0.0
        hyo[i] = 0.0
        par[i] = 0.0
    for j in range(0, 20):
        f = ff[j]
        w = ww[j]
        out(f, w)
    for p in range(0, 21):
        hyouji(p)
    for i in range(0, 21):
        par[i] = round(par[i], 1)
        hyo[i] = round(hyo[i], 1)


@login_required
def indexview(request):
    templates = loader.get_template("index.html")
    contexts = {}
    return HttpResponse(templates.render(contexts, request))


def list_indexview(request):
    user = request.user.id
    p = Profile.objects.get(user=user)
    templates = loader.get_template("index.html")
    checked_food = request.POST.getlist("checkbox")
    checklist = [i for i in p.checkedfood if i != " "]
    for d in checked_food:
        checklist.append(d)
    p.checkedfood = checklist
    """
    for r in range(0, 20):
        checkedfood.append("")
    """
    contexts = {}
    p.save()
    return HttpResponse(templates.render(contexts, request))


def reset_view(request):
    user = request.user.id
    p = Profile.objects.get(user=user)
    templat = loader.get_template("index.html")
    p.checkedfood = ["食品"]
    p.checkweight = ["量"]
    p.foodname = ["食品"]
    p.foodweight = ["量"]
    """
    for i in range(0, 20):
        checkedfood.append("")
    """
    contex = {}
    p.save()
    return HttpResponse(templat.render(contex, request))


def listview(request):
    user = request.user.id
    p = Profile.objects.get(user=user)
    p.checkedfood = ["食品"]
    p.checkweight = ["量"]
    foodfood = request.POST.getlist("food")
    weightweight = request.POST.getlist("weight")
    for uh in foodfood:
        if uh == "":
            pass
            """
            p.checkedfood.append(" ")
            """
        else:
            p.checkedfood.append(uh)
    """
    for ug in range(0, 20):
        p.checkedfood.append("")
    """
    for uw in weightweight:
        if uw == "":
            pass
            """
            p.checkweight.append(" ")
            """
        else:
            p.checkweight.append(uw)
    """
    for uq in range(0, 20):
        p.checkweight.append("")
    """
    template = loader.get_template("list.html")
    context = {"list": lists_food}
    p.save()
    return HttpResponse(template.render(context, request))


def outview(request):
    user = request.user.id
    p = Profile.objects.get(user=user)
    templatess = loader.get_template("out.html")
    contextss = {}
    p.save()
    return HttpResponse(templatess.render(contextss, request))


def outputview(request):
    user = request.user.id
    p = Profile.objects.get(user=user)
    food_input = request.POST.getlist("food")
    p.checkedfood = ["食品"]
    p.checkweight = ["量"]
    p.foodname = ["食品"]
    p.foodweight = ["量"]
    for i in food_input:
        try:
            num = lists_food.index(i)
        except ValueError:
            if i == "":
                pass
            else:
                p.foodname.append("???")
                p.checkedfood.append(i)
        else:
            p.checkedfood.append(i)
            ii = i.replace("\u3000", " ")
            p.foodname.append(ii)
    weight_input = request.POST.getlist("weight")
    for i in weight_input:
        try:
            inn = int(i)
        except ValueError:
            if i == "":
                pass
            else:
                p.foodweight.append("???")
                p.checkweight.append(i)
        else:
            p.checkweight.append(i)
            p.foodweight.append(i)
    out_out(food_input, weight_input)
    template = loader.get_template("output.html")
    context = {"range": ran,
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
    p.save()
    return HttpResponse(template.render(context, request))


class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"
