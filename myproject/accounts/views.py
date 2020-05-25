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
book = openpyxl.load_workbook("accounts/templates/accounts/FOOD.xlsx")
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



"""
lists_r = []
for i in range(9, 313):
    x = sheet["AN" + str(i)].value
    if type(x) == type(None):
        lists_r.append("?")
    else:
     lists_r.append(x)

lists_p = []
for i in range(9, 313):
    x = sheet["AO" + str(i)].value
    if type(x) == type(None):
        lists_p.append("個")
    else:
        lists_p.append(x)
"""
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

ranran = []
for i in range(0, 304):
    ranran.append(i)

hyoujiweight = []


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
    if q == "個":
        r = sheet["AG" + str(num + 9)].value
        if type(r) == type(None):
            r = 0
    elif q == "枚":
        r = sheet["AH" + str(num + 9)].value
        if type(r) == type(None):
            r = 0
    elif q == "玉":
        r = sheet["AI" + str(num + 9)].value
        if type(r) == type(None):
            r = 0
    elif q == "合":
        r = sheet["AJ" + str(num + 9)].value
        if type(r) == type(None):
            r = 0
    elif q == "尾":
        r = sheet["AK" + str(num + 9)].value
        if type(r) == type(None):
            r = 0
    elif q == "切":
        r = sheet["AL" + str(num + 9)].value
        if type(r) == type(None):
            r = 0
    elif q == "cc":
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
    if num == 304:
        hyoujiweight.append("")
    elif inn == 0:
        hyoujiweight.append("???g")
    elif r == 0:
        hyoujiweight.append("(無効な単位)")
    else:
        g = round(inn * r, 1)
        gg = str(g) + "g"
        hyoujiweight.append(gg)

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
    hyoujiweight.append("(量)")
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
        p.checkryo = ["単位", "g", "個"]
        for i in range(0, 18):
            p.checkryo.append("g")
    if p.checkedfood == None:
        p.checkedfood = ["食品", "ぶた　ばら", "じゃがいも"]
    if p.checkweight == None:
        p.checkweight = ["量", "200", "1.5"]
        hello[0] = "はじめまして"
        hello[1] = "例にならい入力して栄養価を計算してみましょう。"
    else:
        hello[1] = "食品名と量を入力してください"
    p.save()
    templates = loader.get_template("index.html")
    contexts = {"hello": hello}
    return HttpResponse(templates.render(contexts, request))


def list_indexview(request):
    hello[1] = "リストから追加出来たら量を入力しましょう"
    user = request.user.id
    p = Profile.objects.get(user=user)
    templates = loader.get_template("index.html")
    checked_food = request.POST.getlist("checkbox")
    checklist = [i for i in p.checkedfood if i != " "]
    for d in checked_food:
        checklist.append(d)
    p.checkedfood = checklist

    contexts = {"hello": hello}
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
    p.checkryo = ["単位"]
    for i in range(0, 20):
        p.checkryo.append("g")
    contex = {"hello": hello}
    p.save()
    return HttpResponse(templat.render(contex, request))


def listview(request):
    user = request.user.id
    p = Profile.objects.get(user=user)
    p.checkedfood = ["食品"]
    p.checkweight = ["量"]
    p.checkryo = ["単位"]
    foodfood = request.POST.getlist("food")
    weightweight = request.POST.getlist("weight")
    ryoryo = request.POST.getlist("ryo")
    for uh in foodfood:
        if uh == "":
            pass
        else:
            p.checkedfood.append(uh)
    for uw in weightweight:
        if uw == "":
            pass
        else:
            p.checkweight.append(uw)
    for i in ryoryo:
        p.checkryo.append(i)
    template = loader.get_template("list.html")
    context = {"list": lists_food,
               "lists_0": lists_0,
               "lists_1": lists_1,
               "lists_2": lists_2,
               "range": ranran,
               }
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
    weight_input = request.POST.getlist("weight")
    ryo_input = request.POST.getlist("ryo")
    p.checkedfood = ["食品"]
    p.checkweight = ["量"]
    p.foodname = ["食品"]
    p.foodweight = ["量"]
    p.checkryo = ["単位"]
    for i in food_input:
        try:
            num = lists_food.index(i)
        except ValueError:
            if i == "":
                p.foodname.append(" ")
                p.checkedfood.append((" "))
            else:
                p.foodname.append("???")
                p.checkedfood.append(i)
        else:
            p.checkedfood.append(i)
            ii = i.replace("\u3000", " ")
            p.foodname.append(ii)

    for i in weight_input:
        if i == "":
            p.foodweight.append(" ")
            p.checkweight.append(" ")
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

    for i in ryo_input:
        if i == "":
            pass
        else:
            p.checkryo.append(i)

    out_out(food_input, weight_input, ryo_input)
    template = loader.get_template("output.html")
    context = {"range": ran,
               "food": food_input,
               "weight": weight_input,
               "ryo": ryo_input,
               "hyouji": hyoujiweight,
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
