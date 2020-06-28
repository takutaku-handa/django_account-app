import io

import matplotlib.pyplot as plt
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
for i in range(9, 313):
    x = sheet["B" + str(i)].value
    lists_food.append(x)

lists_0 = []
for i in range(9, 62):
    x = sheet["B" + str(i)].value
    lists_0.append(x)
for i in range(281, 313):
    x = sheet["B" + str(i)].value
    lists_0.append(x)

lists_1 = []
for i in range(83, 192):
    x = sheet["B" + str(i)].value
    lists_1.append(x)

lists_2 = []
for i in range(62, 83):
    x = sheet["B" + str(i)].value
    lists_2.append(x)
for i in range(198, 281):
    x = sheet["B" + str(i)].value
    lists_2.append(x)

# リスト集
cell = (
    "C", "D", "E", "F", "G", "H", "I", "J", "K", "W", "X", "Z", "AA", "Y", "AD", "R", "AB", "AC", "L", "M", "N", "O",
    "P",
    "Q", "S", "T", "U", "V", "AE")
xxx = {"エネルギー": "kcal", "たんぱく質": "g", "食物繊維": "g",
       "ナトリウム": "mg", "カリウム": "mg", "カルシウム": "mg", "マグネシウム": "mg", "リン": "mg", "鉄": "mg",
       "ビタミンＢ１": "mg", "ビタミンＢ２": "mg", "ビタミンＢ６": "mg", "ビタミンＢ１２": "μg",
       "ナイアシン": "mg", "ビタミンＣ": "mg", "ビタミンＤ": "μg", "葉酸": "μg", "パントテン酸": "mg",
       "ビタミンＡ": "μg", "ビタミンＥ": "mg", "食塩相当量": "g"
       }
nut = [2650, 60, 20, 3149, 2500, 650, 340, 1000, 7, 1.4, 1.6, 1.4, 2.4, 15, 100, 5.5, 240, 5, 850, 6.5, 8.0]
eiy = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, ]
hyo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
par = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
par_x = []
par_y = []
par_z = []

ranran = []
for i in range(0, 304):
    ranran.append(i)

hyoujiweight = []
checkhyouji = []


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


def kosuu(num, q):
    if q == '個':
        r = sheet["AG" + str(num + 9)].value
        if type(r) == type(None):
            r = 0
    elif q == '枚':
        r = sheet["AH" + str(num + 9)].value
        if type(r) == type(None):
            r = 0
    elif q == '玉':
        r = sheet["AI" + str(num + 9)].value
        if type(r) == type(None):
            r = 0
    elif q == '合':
        r = sheet["AJ" + str(num + 9)].value
        if type(r) == type(None):
            r = 0
    elif q == '尾':
        r = sheet["AK" + str(num + 9)].value
        if type(r) == type(None):
            r = 0
    elif q == '切':
        r = sheet["AL" + str(num + 9)].value
        if type(r) == type(None):
            r = 0
    elif q == 'cc':
        r = sheet["AM" + str(num + 9)].value
        if type(r) == type(None):
            r = 0
    else:
        r = 1

    return r


def out(f, w, q):
    try:
        num = lists_food.index(f)
    except ValueError:
        if f == "":
            num = 305
        else:
            num = 304
    else:
        num = int(num)

    try:
        inn = float(w)
    except ValueError:
        inn = 0
    else:
        pass

    r = kosuu(num, q)
    if num == 305:
        if inn != 0:
            pass
    elif num == 304:
        hyoujiweight.append(inn)
        checkhyouji.append(inn)
    elif inn == 0:
        hyoujiweight.append("???")
        checkhyouji.append("?")
    elif r == 0:
        hyoujiweight.append("(無効な単位)")
        if type(w) == type("1"):
            checkhyouji.append(w)
        elif type(w) == type("2.4"):
            checkhyouji.append(inn)
    else:
        g = round(inn * r, 1)
        hyoujiweight.append(g)
        if type(w) == type("1"):
            checkhyouji.append(w)
        elif type(w) == type("2.4"):
            checkhyouji.append(inn)

    # エネルギーからパントテン酸
    for n in range(0, 18):
        add(n, youso(n, num), inn * r)

    # ビタミンＡ
    for j in range(18, 24):
        add(18, youso(j, num), inn * r)

    # ビタミンE
    for j in range(24, 28):
        add(19, youso(j, num), inn * r)

    # 食塩相当量
    add(20, youso(28, num), inn * r)


def out_out(ff, ww, qq):
    hyoujiweight.clear()
    checkhyouji.clear()
    for i in range(0, 21):
        eiy[i] = 0.0
        hyo[i] = 0.0
        par[i] = 0.0
    for j in range(0, 20):
        f = ff[j]
        w = ww[j]
        q = qq[j]
        out(f, w, q)
    for p in range(0, 21):
        hyouji(p)
    for i in range(0, 21):
        par[i] = round(par[i], 1)
        hyo[i] = round(hyo[i], 1)


hello = ["ようこそ", "食品名と量を入力してください"]


@login_required
def indexview(request):
    user = request.user.id
    p = Profile.objects.get(user=user)
    if p.checkryo == None:
        p.checkryo = ["g", "個"]
    for i in range(0, 20):
        p.checkryo.append("g")
    if p.checkedfood == None:
        p.checkedfood = ["ぶた　ばら", "じゃがいも"]
    if p.checkweight == None:
        p.checkweight = ["200", "1.5"]
        hello[0] = "はじめまして"
        hello[1] = "例にならい入力して栄養価を計算してみましょう。"
    else:
        hello[0] = "ようこそ"
        hello[1] = "食品名と量を入力してください"
    p.save()
    templates = loader.get_template("accounts/index.html")
    contexts = {"hello": hello}
    return HttpResponse(templates.render(contexts, request))


def list_indexview(request):
    hello[1] = "リストから追加出来たら量を入力しましょう"
    user = request.user.id
    p = Profile.objects.get(user=user)
    templates = loader.get_template("accounts/index.html")
    checked_food = request.POST.getlist("checkbox")
    for i in checked_food:
        for j in range(0, 20):
            try:
                o = p.checkedfood[j]
            except IndexError:
                p.checkedfood.append(i)
            else:
                if o == " ":
                    p.checkedfood[j] = i
                    break
    for i in range(0, 20):
        p.checkryo.append("g")

    contexts = {"hello": hello}
    p.save()
    return HttpResponse(templates.render(contexts, request))


def reset_view(request):
    hello[1] = "食品名と量を入力してください"
    user = request.user.id
    p = Profile.objects.get(user=user)
    templat = loader.get_template("accounts/index.html")
    p.checkedfood = []
    p.checkweight = []
    p.foodname = []
    p.foodweight = []
    p.checkryo = []
    for i in range(0, 21):
        p.checkryo.append("g")
    contex = {"hello": hello}
    p.save()
    return HttpResponse(templat.render(contex, request))


def listview(request):
    user = request.user.id
    p = Profile.objects.get(user=user)
    p.checkedfood = []
    p.checkweight = []
    p.checkryo = []
    foodfood = request.POST.getlist("food")
    weightweight = request.POST.getlist("weight")
    ryoryo = request.POST.getlist("ryo")

    n = []
    for uh in foodfood:
        if uh == "":
            n.append(" ")
        else:
            n.append(uh)

    l = []
    for uw in weightweight:
        if uw == "":
            l.append(" ")
        else:
            l.append(uw)

    p.checkedfood = n
    p.checkweight = l
    p.checkryo = ryoryo
    template = loader.get_template("accounts/list.html")
    context = {"list": lists_food,
               "lists_0": lists_0,
               "lists_1": lists_1,
               "lists_2": lists_2,
               "range": ranran,
               "food": foodfood,
               }
    p.save()
    return HttpResponse(template.render(context, request))


def outview(request):
    user = request.user.id
    p = Profile.objects.get(user=user)
    templatess = loader.get_template("accounts/out.html")
    contextss = {}
    p.save()
    return HttpResponse(templatess.render(contextss, request))


def img_plot():
    x = []
    for i in range(1, 22):
        x.append(i * 4.8)
    fig = plt.figure(figsize=(5, 14.7))
    ax = fig.add_subplot(111)
    plt.barh(x, par_x, color="crimson", height=2.3)
    plt.barh(x, par_y, left=par_x, color="white", height=2.3)
    plt.barh(x, par_z, left=par_x, color="limegreen", height=2.3)
    plt.vlines([100], ymax=106, ymin=0.5, linestyles="dashed")
    plt.ylim(3, 104)

    www = []
    uuu = []
    for i in range(1, 22):
        www.append(i * 4.8 - 0.8)
    for u in reversed(par):
        uuu.append(str(u) + "%")
    for j in range(0, 21):
        ax.text(3, www[j], uuu[j], size=16, color='black', weight="bold")
    ax.tick_params(top=True, bottom=True, labeltop=True)
    ax = plt.gca()
    ax.axes.yaxis.set_visible(False)
    ax.spines['right'].set_visible(False)


# svgへの変換
def pltToSvg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s


def get_svg(request):
    img_plot()  # create the plot
    svg = pltToSvg()  # convert plot to SVG
    plt.cla()  # clean up plt so it can be re-used
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response


def outputview(request):
    user = request.user.id
    p = Profile.objects.get(user=user)
    food_input = request.POST.getlist("food")
    weight_input = request.POST.getlist("weight")
    ryo_input = request.POST.getlist("ryo")
    p.checkedfood = []
    p.checkweight = []
    p.foodname = []
    p.foodweight = []
    p.checkryo = []
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

    for i in weight_input:
        if i == "":
            pass
        try:
            inn = int(i)
        except ValueError:
            if i == "":
                pass
            else:
                p.foodweight.append("???")
        else:
            p.foodweight.append(inn)
    for i in range(0, len(p.foodname)):
        p.checkryo.append(ryo_input[i])

    p.foodweight = hyoujiweight
    p.checkweight = checkhyouji

    out_out(food_input, weight_input, ryo_input)

    oooo = ["s"]
    try:
        type(p.foodname[0]) == type(None)
    except IndexError:
        oooo.append("hidden")
    else:
        if "???" in p.foodname or "???" in p.foodweight:
            oooo.append("hidden")
    par_x.clear()
    par_y.clear()
    par_z.clear()
    for i in reversed(par):
        if i <= 100:
            par_x.append(round(i, 1))
            par_y.append(round(100 - i, 1))
            par_z.append(0)
        else:
            par_x.append(0)
            par_y.append(0)
            par_z.append(round(i, 1))
    template = loader.get_template("accounts/output.html")
    ran = ["No"]
    for i in range(1, len(hyoujiweight)+1):
        ran.append(i)
    context = {"range": ran,
               "hyouji": hyoujiweight,
               "hidden": oooo[-1],
               "hyo": hyo,
               "par": par,
               "name": xxx,
               "tanni": xxx.values(),
               }

    p.save()
    return HttpResponse(template.render(context, request))


class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"
