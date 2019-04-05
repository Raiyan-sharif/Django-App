from django.shortcuts import render, get_object_or_404
from .forms import TournamentForm
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, FormView
from accounts.models import UserModel,PlayerModel
from .models import Tournament


def create_tournament(request):
    form = TournamentForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # some more stuf could be done here
        obj.save()
        # messages.success(request,"Player Created")
        return HttpResponseRedirect("../{num}".format(num=obj.pk))

    template = "tournament/tournament_creating.html"
    context = {"form": form}
    return render(request, template, context)


def detail_of_tournament(request, pk):
    qs = get_object_or_404(Tournament, pk=pk)
    print(qs)
    template = "tournament/tournament_details.html"
    context = {"query": qs}

    return render(request, template, context)


def update_tournament(request, pk=None):
    qs = get_object_or_404(Tournament, pk=pk)
    form = TournamentForm(request.POST or None, instance=qs)
    context = {"form": form, "query": qs}

    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect("../")

    template = "tournament/tournament_update.html"
    return render(request, template, context)


def delete_tournament(request, pk=None):
    qs = get_object_or_404(Tournament, pk=pk)
    print(request.method)
    if request.method == 'POST':
        qs.delete()
        print("deleted")
        return HttpResponseRedirect("../../")
    template = "tournament/delete_tournament.html"
    context = {"query": qs}

    return render(request, template, context)


def list_of_tournament(request):
    search_obj = request.GET.get("q", None)

    qs = Tournament.objects.all()
    if search_obj is not None:
        qs = qs.filter(tornament_name__icontains=search_obj)
    print(qs)
    template = "tournament/tournament_list.html"
    context = {"query": qs}
    return render(request, template, context)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Tournament.objects.all()
        context = {"q": qs}

        return context


class UpcomingTournament(TemplateView):
    template_name = 'tournament/upcomming_tournament.html'

    def get(self, request, *args, **kwargs):
        self.request = request
        context = self.get_context_data(**kwargs)
        print("any")
        print(request.GET['tournament'])
        qs = Tournament.objects.all()

        if 'upcoming_tournament' in request.path:
            context = {"btn": request.GET['tournament'], "q": qs}
            print(request.path)
        elif 'ongoing_tournament' in request.path:
            context = {"btn": request.GET['tournament'], "q": qs}

        elif 'edit' in request.path:
            context = {"btn": request.GET['tournament'], "q": qs}

        elif 'tournament_history' in request.path:
            context = {"btn": request.GET['tournament'], "q": qs}

        elif 'new_game' in request.path:
            if str(self.request.user) != "AnonymousUser":
                userobj = UserModel.objects.filter(username=str(self.request.user))
                print(userobj)
                playerobj = PlayerModel.objects.filter(user=self.request.user)
                context = {"q": qs,
                           "btn": request.GET['tournament'],
                           "userobj": userobj,
                           "playerobj": playerobj}

        else:
            context = {"q": qs}

        return self.render_to_response(context)

    def get_template_names(self):

        print(self.request.user)
        if str(self.request.user) != "AnonymousUser" and str(self.request.user.user_type) == '1':
            print(self.request.user.user_type)
            if 'new_game' in self.request.path:
                self.request.template_name = 'player/newgame.html'
                print("ok")
            else:
                self.request.template_name = 'tournament/upcomming_tournament.html'
        else:
            self.request.template_name = 'index.html'

        return self.request.template_name


