import datetime
import io
import itertools
import re

import matplotlib.pyplot as plt
from accounts import models, views
from accounts.views import hyouji, out
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView, DetailView, TemplateView

from . import mixins
from .forms import RecipeForm, CalenderForm
from .models import MyCalender
from .models import Recipe

"""start"""
par_x = []
par_y = []
par_z = []


def img_plot():
    x = []
    for i in range(1, 22):
        x.append(i * 4.8)
    fig = plt.figure(figsize=(7, 6.1))
    ax = fig.add_subplot(111)
    plt.barh(x, par_x, color="crimson", height=3)
    plt.barh(x, par_y, left=par_x, color="white", height=3)
    plt.barh(x, par_z, left=par_x, color="limegreen", height=3)
    plt.vlines([100], ymax=106, ymin=0.5, linestyles="dashed")
    plt.ylim(3, 104)

    #www = []
    #uuu = []
    #for i in range(1, 22):
        #www.append(i * 4.8 - 0.8)
    #for u in reversed(par):
        #uuu.append(str(u) + "%")
    #for j in range(0, 21):
        #ax.text(3, www[j], uuu[j], size=10, color='black', weight="bold")
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


"""stop"""


class WeekCalendar(mixins.WeekCalendarMixin, TemplateView):
    template_name = "calender/top.html"

    def get_context_data(self, **kwargs):
        self.setup_calendar()
        days = self.get_week_days()

        l = list(Recipe.objects.filter(user=self.request.user.id).values_list('name', flat=True))

        d = models.Profile.objects.get(user=self.request.user)
        d.day = datetime.date(2020, 1, 1)
        d.save()

        calendar_data = {
            'now': datetime.date.today(),
            'week_days': days,
            'week_previous': days[0] - datetime.timedelta(days=7),
            'week_next': days[0] + datetime.timedelta(days=7),
            'week_names': self.get_week_names(),
            'week_first': days[0],
            'mon': days[1],
            'tue': days[2],
            'wed': days[3],
            'tur': days[4],
            'fri': days[5],
            'week_last': days[-1],
            "Recipe": Recipe.objects.filter(Q(user=self.request.user.id) | Q(pub=True)),
            "list": l,
            "d": datetime.date.today(),
        }
        context = super().get_context_data(**kwargs)
        context.update(calendar_data)
        list_xxx = []
        for i in range(0, 7):
            list_x = []
            for j in range(1, 5):
                list_y = []
                asa = list(
                    MyCalender.objects.filter(Q(user=self.request.user.id) & Q(date=days[i]) & Q(time=j)).values_list(
                        'name', flat=True))
                for pk in asa:
                    name = list(Recipe.objects.filter(pk=pk).values_list('name', flat=True))
                    n = name[0]
                    list_y.append(n)
                list_x.append(list_y)
            list_xxx.append(list_x)
        last_list_zero = []
        for j in range(0, 7):
            last_list_zero.append(list_xxx[j][0])
        last_list_one = []
        for j in range(0, 7):
            last_list_one.append(list_xxx[j][1])
        last_list_two = []
        for j in range(0, 7):
            last_list_two.append(list_xxx[j][2])
        last_list_three = []
        for j in range(0, 7):
            last_list_three.append(list_xxx[j][3])

        context["food"] = {"朝": last_list_zero, "昼": last_list_one, "夜": last_list_two, "間": last_list_three}
        return context


"""ここから栄養計算の準備"""
lists_food = views.lists_food
cell = views.cell
xxx = views.xxx
nut = views.nut
hyo = views.hyo
eiy = views.eiy
par = views.par
hyoujiweight = views.hyoujiweight
checkhyouji = views.checkhyouji


class ChangeDay(TemplateView, mixins.WeekCalendarMixin):
    template_name = "calender/change.html"

    def get_context_data(self, **kwargs):
        self.setup_calendar()
        days = self.get_week_days()

        day = self.request.GET.get('day')
        if day:
            model_x = models.Profile.objects.get(user=self.request.user)

            day = str(day)
            tdatetime = datetime.datetime.strptime(day, '%Y年%m月%d日')
            tdate = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)

            if tdate == model_x.day:
                model_x.day = datetime.date(2020, 1, 1)
                model_x.save()
                tt = "dame"
            else:
                model_x.day = tdate
                model_x.save()
                tt = "ok"
        else:
            tt = "ok"

        d = list(models.Profile.objects.filter(user=self.request.user).values_list("day"))
        d = d[0]
        d = d[0]

        f_list = []
        r_list = []
        for i in range(1, 5):
            f_list.append(list(MyCalender.objects.filter(Q(date=d) & Q(time=i)).values_list("name", flat=True)))
            r_list.append(list(MyCalender.objects.filter(Q(date=d) & Q(time=i)).values_list("ryo", flat=True)))

        l = list(Recipe.objects.filter(user=self.request.user.id).values_list('name', flat=True))
        r = list(Recipe.objects.filter(pub=True).values_list('name', flat=True))

        """start"""
        list_foods = []
        foods_list = list(MyCalender.objects.filter(date=d).values_list("name", flat=True))
        ryo_list = list(MyCalender.objects.filter(date=d).values_list("ryo", flat=True))

        for f in foods_list:
            name = list(Recipe.objects.filter(pk=int(f)).values_list('name'))
            name = name[0]
            name = name[0]
            list_foods.append(name)

        hyoujiweight.clear()
        checkhyouji.clear()
        for i in range(0, 21):
            eiy[i] = 0.0
            hyo[i] = 0.0
            par[i] = 0.0

        for i in range(0, len(list_foods)):
            fo = list_foods[i]
            ry = ryo_list[i]
            ing = Recipe.objects.get(name=fo).ingredient
            wei = Recipe.objects.get(name=fo).weight

            for ii in range(0, len(ing)):
                out(ing[ii], float(wei[ii]) * float(ry), "g")

        for p in range(0, 21):
            hyouji(p)
        for i in range(0, 21):
            par[i] = round(par[i], 1)
            hyo[i] = round(hyo[i], 1)

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

        all = 0
        for j in range(0, 21):
            if par[j] <= 100:
                jamp = (100 - float(par[j])) * 10
            else:
                jamp = float(par[j]) - 100
            all += jamp
        heikin = all / 21
        if heikin <= 25:
            hto = "S"
        elif heikin <= 50:
            hto = "A"
        elif heikin <= 150:
            hto = "B"
        elif heikin <= 300:
            hto = "C"
        elif heikin <= 500:
            hto = "D"
        elif heikin <= 800:
            hto = "E"
        else:
            hto = "F"
        """stop"""

        calendar_data = {
            'now': datetime.date.today(),
            'week_days': days,
            'week_previous': days[0] - datetime.timedelta(days=7),
            'week_next': days[0] + datetime.timedelta(days=7),
            'week_names': self.get_week_names(),
            'week_first': days[0],
            'mon': days[1],
            'tue': days[2],
            'wed': days[3],
            'tur': days[4],
            'fri': days[5],
            'week_last': days[-1],
            'd': d,
            "Recipe": Recipe.objects.filter(Q(user=self.request.user.id) | Q(pub=True)),
            "MyCalender": MyCalender.objects.filter(Q(user=self.request.user.id) & Q(date=d)),
            "foods_list": f_list,
            "ryo_list": r_list,
            "list": l,
            "rist": r,
            "tt": tt,
            "par": par,
            "eiyo": views.xxx,
            "h": hto,
        }

        context = super().get_context_data(**kwargs)
        context.update(calendar_data)

        list_xxx = []
        for i in range(0, 7):
            list_x = []
            for j in range(1, 5):
                list_y = []
                asa = list(
                    MyCalender.objects.filter(Q(user=self.request.user.id) & Q(date=days[i]) & Q(time=j)).values_list(
                        'name', flat=True))
                for pk in asa:
                    name = list(Recipe.objects.filter(pk=pk).values_list('name', flat=True))
                    n = name[0]
                    list_y.append(n)
                list_x.append(list_y)
            list_xxx.append(list_x)
        last_list_zero = []
        for j in range(0, 7):
            last_list_zero.append(list_xxx[j][0])
        last_list_one = []
        for j in range(0, 7):
            last_list_one.append(list_xxx[j][1])
        last_list_two = []
        for j in range(0, 7):
            last_list_two.append(list_xxx[j][2])
        last_list_three = []
        for j in range(0, 7):
            last_list_three.append(list_xxx[j][3])

        context["food"] = {"朝": last_list_zero, "昼": last_list_one, "夜": last_list_two, "間": last_list_three}
        return context


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe/list.html'


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe/detail.html'
    fields = ["user", 'name', 'ingredient', 'weight', 'hyojiweight', 'hyojiryo']


class MyCalenderDetailView(DetailView):
    model = MyCalender
    template_name = 'calender/detail.html'
    fields = ['date', 'time', 'name', 'ryo']


def newrecipe(request):
    l1 = list(models.Profile.objects.filter(user=request.user.id).values_list('checkedfood', flat=True))
    l2 = list(models.Profile.objects.filter(user=request.user.id).values_list('foodweight', flat=True))
    l3 = list(models.Profile.objects.filter(user=request.user.id).values_list('checkweight', flat=True))
    l4 = list(models.Profile.objects.filter(user=request.user.id).values_list('checkryo', flat=True))

    initial = {
        'user': request.user.id,
        'ingredient': l1[0],
        'weight': l2[0],
        'hyojiweight': l3[0],
        'hyojiryo': l4[0],
    }
    content = {"message": '料理名：',
               "form": None,
               "checkedfood": models.Profile.objects.filter(user=request.user.id).values_list('checkedfood', flat=True),
               "foodweight": models.Profile.objects.filter(user=request.user.id).values_list('foodweight', flat=True),
               "checkweight": models.Profile.objects.filter(user=request.user.id).values_list('checkweight', flat=True),
               "chekryo": models.Profile.objects.filter(user=request.user.id).values_list('checkryo', flat=True),
               }
    form = RecipeForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('recipe_list')
        else:
            content["message"] = "<<その料理名はすでに登録されています>>"
            content["form"] = form
    else:
        content["form"] = form

    return render(request, 'recipe/create.html', content)


def newcalender(request):
    day = request.POST.get('day')
    day = str(day)

    tdatetime = datetime.datetime.strptime(day, '%Y年%m月%d日')
    tdate = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)

    d = list(models.Profile.objects.filter(user=request.user).values_list("day"))
    d = d[0]
    d = d[0]

    l = list(Recipe.objects.filter(user=request.user.id).values_list('name', flat=True))
    content = {
        "list": l,
        "day": day}

    foodname = request.POST.get('name')
    ryo = request.POST.get('ryo')
    if not ryo:
        ryo = 1.0

    if not foodname:
        return redirect("week")
    else:
        if request.method == "POST":
            ttime = request.POST.get('time')
            ttime = int(ttime)
            r = Recipe.objects.get(name=foodname)
            r.save()
            MyCalender.objects.create(user=request.user, date=tdate, time=ttime, name=r, ryo=ryo)

            ii = list(re.split('年|月|日', day))
            url = "../change/" + ii[0] + "/" + ii[1] + "/" + ii[2]

            return redirect(url)

        return render(request, 'calender/create.html', content)


class RecipeDelete(DeleteView):
    model = Recipe
    template_name = 'recipe/delete.html'
    success_url = reverse_lazy('recipe_list')

def deletecalender(request):
    if request.method == "POST":
        pk = request.POST.get('pk')
        MyCalender.objects.filter(pk=pk).delete()
        day = request.POST.get('day')
        if day:
            day = str(day)
            ii = list(re.split('年|月|日', day))
            url = "../../change/" + ii[0] + "/" + ii[1] + "/" + ii[2]
            return redirect(url)
        else:
            return redirect("../week/")
    content = {}
    return render(request, 'calender/create.html', content)


class RecipeUpdateView(UpdateView):
    model = Recipe
    template_name = 'recipe/update.html'
    fields = ['pub', 'name', 'ingredient', 'weight', 'hyojiweight', 'hyojiryo', 'recipe']
    success_url = reverse_lazy('recipe_list')


class MyCalenderUpdateView(TemplateView):
    template_name = 'calender/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        mod = MyCalender.objects.get(pk=int(pk))
        context["mod"] = mod
        context["l"] = list(Recipe.objects.filter(user=self.request.user.id).values_list('name', flat=True))
        context["r"] = list(Recipe.objects.filter(pub=True).values_list('name', flat=True))
        initial = {"date": mod.date}
        context["form"] = CalenderForm(initial=initial)
        return context


def changecalender(request):
    date_year = request.POST.get('date_year')
    date_month = request.POST.get('date_month')
    date_day = request.POST.get('date_day')

    day = str(date_year) + "年" + str(date_month) + "月" + str(date_day) + "日"

    tdatetime = datetime.datetime.strptime(day, '%Y年%m月%d日')
    tdate = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)


    l = list(Recipe.objects.filter(user=request.user.id).values_list('name', flat=True))
    content = {}

    foodname = request.POST.get('name')
    ryo = request.POST.get('ryo')
    if not ryo:
        ryo = 1.0

    if not foodname:
        return redirect("week")
    else:
        if request.method == "POST":
            ttime = request.POST.get('time')
            ttime = int(ttime)
            r = Recipe.objects.get(name=foodname)
            r.save()
            pk = request.POST.get('pk')
            m = MyCalender.objects.get(pk=pk)
            m.date = tdate
            m.time = ttime
            m.name = r
            m.ryo = ryo
            m.save()

            ii = list(re.split('年|月|日', day))
            url = "../change/" + ii[0] + "/" + ii[1] + "/" + ii[2]

            return redirect(url)

        return render(request, 'calender/create.html', content)


def hyoji(dic_f, dic_r, list_i):
    dic_hyoji = {}
    for n in range(1, len(list_i) + 1):
        for conb in itertools.combinations(list_i, n):
            dic_x = {}
            dic_x.update(dic_f)
            for m in list(conb):
                f = dic_r[m]
                for n, w in f.items():
                    if n in dic_x:
                        dic_x[n] += float(w)
                    else:
                        dic_x[n] = float(w)
            l = []
            for x in dic_x.values():
                if float(x) < 0:
                    l.append("a")
            p = len(l)
            # p = sum(x < 0 for x in dic_x.values())
            if p == 0:
                dic_xx = {}
                for h, p in dic_x.items():
                    if float(p) > 0:
                        dic_xx[h] = p
                dic_hyoji[conb] = dic_xx

        if dic_hyoji != {}:
            break

    return dic_hyoji


@login_required()
def myshohiview(request):
    foods = request.POST.getlist('food')
    list_foods = []
    for i in foods:
        if i != "":
            list_foods.append(i)
    weights = request.POST.getlist('weight')
    list_weights = []
    for i in weights:
        if i != "":
            list_weights.append(-1 * float(i))

    dic_shokuzai = dict(zip(list_foods, list_weights))

    recipes = {}
    user = request.user.id
    p1 = Recipe.objects.filter(user=user).values_list('name', flat=True)
    p2 = Recipe.objects.filter(user=user).values_list('ingredient', flat=True)
    p3 = Recipe.objects.filter(user=user).values_list('weight', flat=True)
    p1 = list(p1)
    p2 = list(p2)
    p3 = list(p3)
    for i in range(0, len(p1)):
        p_2 = p2[i]
        p_3 = p3[i]
        dic_y = {}
        for j in range(0, len(p_2)):
            dic_y[p_2[j]] = p_3[j]

        recipes[p1[i]] = dic_y

    list_index = []
    for i in list(dic_shokuzai.keys()):
        for q, j in recipes.items():
            if i in j and q not in list_index:
                list_index.append(q)

    hyo = hyoji(dic_shokuzai, recipes, list_index)

    context = {"list": recipes,
               "foods": foods,
               "weights": weights,
               "dic_shokuzai": dic_shokuzai,
               "list_foods": list_foods,
               "list_weights": list_weights,
               "h": hyo,
               "Recipe": Recipe.objects.filter(user=user),
               "Recipe2": Recipe.objects.filter(pub=True),
               "name": Recipe.objects.filter(user=user).values_list('name', flat=True),
               "pk": Recipe.objects.filter(user=user).values_list('pk', flat=True),
               }
    template = loader.get_template("recipe/shohi2.html")
    return HttpResponse(template.render(context, request))


@login_required()
def allshohiview(request):
    foods = request.POST.getlist('food')
    list_foods = []
    for i in foods:
        if i != "":
            list_foods.append(i)
    weights = request.POST.getlist('weight')
    list_weights = []
    for i in weights:
        if i != "":
            list_weights.append(-1 * float(i))

    dic_shokuzai = dict(zip(list_foods, list_weights))

    recipes = {}
    user = request.user.id
    p1 = Recipe.objects.filter(Q(user=user) | Q(pub=True)).values_list('name', flat=True)
    p2 = Recipe.objects.filter(Q(user=user) | Q(pub=True)).values_list('ingredient', flat=True)
    p3 = Recipe.objects.filter(Q(user=user) | Q(pub=True)).values_list('weight', flat=True)
    p1 = list(p1)
    p2 = list(p2)
    p3 = list(p3)
    for i in range(0, len(p1)):
        p_2 = p2[i]
        p_3 = p3[i]
        dic_y = {}
        for j in range(0, len(p_2)):
            dic_y[p_2[j]] = p_3[j]

        recipes[p1[i]] = dic_y

    list_index = []
    for i in list(dic_shokuzai.keys()):
        for q, j in recipes.items():
            if i in j and q not in list_index:
                list_index.append(q)

    hyo = hyoji(dic_shokuzai, recipes, list_index)

    context = {"list": recipes,
               "h": hyo,
               "Recipe": Recipe.objects.filter(user=user),
               "Recipe2": Recipe.objects.filter(pub=True),
               "Recipe0": Recipe.objects.filter(Q(user=user) | Q(pub=True)),
               "name": Recipe.objects.filter(user=user).values_list('name', flat=True),
               "pk": Recipe.objects.filter(user=user).values_list('pk', flat=True),
               "dic_s": dic_shokuzai,
               }
    template = loader.get_template("recipe/shohi.html")
    return HttpResponse(template.render(context, request))


def recipeview(request):
    template = loader.get_template('recipe/recipe.html')
    context = {}
    return HttpResponse(template.render(context, request))
