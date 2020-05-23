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
ran = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,)

foodname = []
foodweight = []
checkedfood = []
checkweight = []



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


def reset():
    for i in range(0, 21):
        eiy[i] = 0.0
        hyo[i] = 0.0
        par[i] = 0.0
        foodname.clear()
        foodweight.clear()


"""
def delete():
    for t in foodname:
        if t == "":
            del foodname[t]
"""


# スタート
def out(f, w):
    try:
        num = lists_food.index(f)
        num = int(num)
    except ValueError:
        num = -8
        if f == "":
            foodname.append("")
        else:
            foodname.append("???")
    else:
        f = f.replace("\u3000", " ")
        foodname.append(f)

    try:
        inn = int(w)
    except ValueError:
        inn = 0
        if w == "":
            foodweight.append(w)
        else:
            iinn = "???"
            foodweight.append(iinn)
    else:
        foodweight.append(inn)

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
    reset()
    for j in range(0, 20):
        f = ff[j]
        w = ww[j]
        out(f, w)
    for p in range(0, 21):
        hyouji(p)
    for i in range(0, 21):
        par[i] = round(par[i], 1)
        hyo[i] = round(hyo[i], 1)
    """
    delete()
    """


@login_required
def indexview(request):
    templates = loader.get_template("index.html")
    contexts = {"checkedfood": checkedfood,
                "checkweight": checkweight}
    return HttpResponse(templates.render(contexts, request))


def list_indexview(request):
    templates = loader.get_template("index.html")
    checked_food = request.POST.getlist("checkbox")
    checklist = [i for i in checkedfood if i != ""]
    for d in checked_food:
        checklist.append(d)
    for r in range(0, 20):
        checkedfood.append("")
    contexts = {"checkedfood": checklist,
                "checkweight": checkweight,
                }
    return HttpResponse(templates.render(contexts, request))


def reset_view(request):
    templat = loader.get_template("index.html")
    checkedfood.clear()
    for i in range(0, 20):
        checkedfood.append("")
    contex = {"checkedfood": checkedfood, }
    return HttpResponse(templat.render(contex, request))


def listview(request):
    checkedfood.clear()
    checkweight.clear()
    foodfood = request.POST.getlist("food")
    weightweight = request.POST.getlist("weight")
    for uh in foodfood:
        checkedfood.append(uh)
    for ug in range(0, 20):
        checkedfood.append("")
    for uw in weightweight:
        checkweight.append(uw)
    for uq in range(0, 20):
        checkweight.append("")
    template = loader.get_template("list.html")
    context = {"list": lists_food}
    return HttpResponse(template.render(context, request))


def outview(request):
    checkweight.clear()
    templatess = loader.get_template("out.html")
    contextss = {}
    return HttpResponse(templatess.render(contextss, request))


def outputview(request):
    food_input = request.POST.getlist("food")
    checkedfood.clear()
    for i in food_input:
        checkedfood.append(i)
    weight_input = request.POST.getlist("weight")
    checkweight.clear()
    for i in weight_input:
        checkweight.append(i)
    out_out(food_input, weight_input)
    template = loader.get_template("output.html")
    context = {"name": foodname,
               "weight": foodweight,
               "range": ran,
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


class MyLogoutView(LoginRequiredMixin, LogoutView):
    checkweight.clear()
    template_name = "accounts/logout.html"
