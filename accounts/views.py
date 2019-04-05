from django.shortcuts import render,redirect,Http404, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout as auth_logout, update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (CreateView,FormView,
                                    RedirectView,TemplateView,
                                        UpdateView,ListView,
                                                    DetailView)
from .forms import *
from tournament.models import Tournament
from .models import UserModel, PlayerModel


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'Registration/login.html'
    success_url = '/'

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/')
                    else:
                        return HttpResponse('Inactive user')
            else:
                return render(request, self.template_name,{'error_message':'Login Failed! Enter the username and password correctly','form':LoginForm})
            return render(request, 'index.html')
        else:
            return render(request, self.template_name, {'form':form})


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class Registration(CreateView):
    user_form_class = UserRegistrationForm
    player_form_class = PlayerRegistrationForm
    club_form_class = ClubRegistrationForm
    template_name = 'Registration/general_registration.html'
    # print("Registration Create view called")

    def get(self, request):
        player_form = self.player_form_class
        user_form = self.user_form_class
        return render(request, self.template_name, {'player_form': player_form,
                                                    'user_form': user_form,
                                                    'c': 'Player Registration: '})

    def post(self, request):
        user_form = self.user_form_class(request.POST)
        player_form = self.player_form_class(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            username = request.POST['username']
            password = user_form['password1']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            is_player = True
            user_type = '1'
            date_of_birth = request.POST['initial-date_of_birth']
            nationality = request.POST['nationality']
            gender = request.POST['gender']
            profile_pic = request.POST['profile_pic']
            marital_status = request.POST['marital_status']
            gameFrequency = request.POST['gameFrequency']
            address = request.POST['address']
            user.save()
            player = player_form.save(commit=False)
            player.user = user
            player.save()
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.active:
                    login(request, user)
            return redirect('/')
        return render(request, self.template_name, {'player_form': player_form,
                                                    'user_form': user_form,
                                                    'c': 'Player Registration'})


# player registration
class PlayerRegistrationView(CreateView):
    player_form_class = PlayerRegistrationForm
    user_form_class = UserRegistrationForm
    print("PlayerRegistration Create view called")
    template_name = 'Registration/player_registration.html'

    def get(self, request):
        player_form = self.player_form_class(None)
        user_form = self.user_form_class
        return render(request, self.template_name, {'player_form': player_form,
                                                    'user_form': user_form,
                                                    'c': 'Player Registration: '})

    def post(self, request):
        user_form = self.user_form_class(request.POST)
        player_form = self.player_form_class(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            username = request.POST['username']
            password = user_form.cleaned_data.get('password1')
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            user.is_player = True
            user.user_type = '1'
            date_of_birth = request.POST['date_of_birth']
            nationality = request.POST['nationality']
            gender = request.POST['gender']
            profile_pic = request.POST['profile_pic']
            marital_status = request.POST['marital_status']
            gameFrequency = request.POST['gameFrequency']
            address = request.POST['address']
            user.save()
            player = player_form.save(commit=False)
            player.user = user
            player.save()
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.active:
                    login(request, user)
            return redirect('/')
        return render(request, self.template_name, {'player_form': player_form,
                                                    'user_form': user_form,
                                                    'c': 'Player Registration'})


class ClubRegistrationView(CreateView):
    club_form_class = ClubRegistrationForm
    user_form_class = UserRegistrationForm
    # user_form_class = UserAdminCreationForm
    template_name = 'Registration/player_registration.html'
    print("club Registration Create view called")
    heading = "Club Registration"

    def get(self, request):
        club_form = self.club_form_class(None)
        user_form = self.user_form_class
        context = {'player_form': club_form,
                   'user_form': user_form,
                   'c': 'Club Registration'}
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = self.user_form_class(request.POST)
        club_form = self.club_form_class(request.POST)
        username = request.POST['username']
        username = request.POST['username']
        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data['password1']
            username = request.POST['username']
            phone_number = request.POST['phone_number']
            user.is_club_auth = True
            user.is_player = False
            user.user_type = '2'
            club_starting_date = request.POST['club_starting_date']
            number_of_tables = request.POST['number_of_tables']
            profile_pic = request.POST['profile_pic']
            address = request.POST['address']
            user.save()
            player = club_form.save(commit=False)
            player.user = user
            player.save()
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.active:
                    login(request, user)
            return redirect('/')

        return render(request, self.template_name, {'player_form': club_form,
                                                    'user_form': user_form,
                                                    'c': 'Club Registration'})


class HomeView(TemplateView):
    user = get_user_model()

    def get_template_names(self):

        print(self.request.user)
        if str(self.request.user) != "AnonymousUser":
            print(self.request.user.user_type)
            if str(self.request.user.user_type) == '1':
                self.request.template_name = 'player/index.html'
            elif str(self.request.user.user_type) == '2':
                self.request.template_name = 'club/index.html'
            elif self.request.user.user_type == '3':
                self.request.template_name = 'admin/index.html'
            elif self.request.user.user_type == '4':
                self.request.template_name = 'customadmin/index.html'
            else:
                self.request.template_name = 'user_not_found.html'
        else:
            self.request.template_name = 'index.html'

        return self.request.template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Tournament.objects.all()
        if str(self.request.user) != "AnonymousUser":
            userobj = UserModel.objects.filter(username=str(self.request.user))
            playerobj = PlayerModel.objects.filter(user=self.request.user)
            context = {"q": qs,
                       "userobj": userobj,
                       "playerobj": playerobj}

        else:
            context = {"q": qs}

        return context


class ProfileDetail(DetailView):
    player_form_class = PlayerRegistrationForm
    user_form_class = UserRegistrationForm
    template_name = 'player/player_profile.html'
    model = UserModel
    slug_field = 'slug'
    # slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        user_form = self.user_form_class(request.POST)
        player_form = self.player_form_class(request.POST)
        self.object = self.get_object()
        context = {'playerobj': player_form,
                   'userobj': user_form,
                   'c': 'Player Profile'}
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Tournament.objects.all()
        if str(self.request.user) != "AnonymousUser":
            userobj = UserModel.objects.filter(slug=str(self.request.user))
            playerobj = PlayerModel.objects.filter(user=self.request.user)
            context = {"q": qs,
                       "userobj": userobj,
                       "playerobj": playerobj}

        else:
            context = {"q": qs}

        return context


# class ProfileUpdateView(UpdateView):
#     model = PlayerModel
#     form_class = UserRegistrationForm
#     second_form_class = PlayerRegistrationForm
#     template_name = 'player/player_profile_edit.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProfileUpdateView, self).get_context_data(**kwargs)
#         # context['active_client'] = True
#         if 'form' not in context:
#             # context['form'] = self.form_class(self.request.GET)
#             context['form'] = self.form_class(self.request.GET, instance=self.request.user)
#         if 'form2' not in context:
#             print("Working"+ str(self.request.user.profile))
#             # self.second_form_class = self.second_form_class(self.request.GET, instance=self.request.user.profile)
#             playerobj = PlayerModel.objects.get(user=self.request.user)
#             context['form2'] = self.second_form_class(self.request.GET, instance=playerobj)
#         # context['active_client'] = True
#         return context
#
#     def get(self, request, *args, **kwargs):
#         super(ProfileUpdateView, self).get(request, *args, **kwargs)
#         form = self.form_class
#         form2 = self.second_form_class
#         return self.render_to_response(self.get_context_data(
#             object=self.object, form=form, form2=form2))

def update_profile(request, pk=None):
    qs = get_object_or_404(PlayerModel, pk=pk)
    form = PlayerRegistrationForm(request.POST or None, instance=qs)
    context = {"form": form, "query": qs}

    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect("/ accounts/")

    template = 'player/player_profile_edit.html'
    return render(request, template, context)


class ProfileUpdateView(UpdateView):
    model = UserModel
    second_model = PlayerModel
    template_name = 'player/player_profile_edit.html'
    form_class = UserProfileUpdate
    second_form_class = PlayerRegistrationForm
    success_url = '../'

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        userobj = self.model.objects.get(pk=pk)
        playerobj = self.second_model.objects.get(user=pk)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=playerobj)
        context['pk'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_sitiocontratado = kwargs['pk']
        sitiocontratado = self.model.objects.get(id=id_sitiocontratado)
        sitioproyecto = self.second_model.objects.get(user=id_sitiocontratado)
        form = self.form_class(request.POST, instance=sitiocontratado)
        form2 = self.second_form_class(request.POST, instance=sitioproyecto)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))
    # player_form_class = PlayerRegistrationForm
    # user_form_class = UserRegistrationForm
    # model = UserModel
    # template_name = 'player/player_profile_edit.html'
    # slug_field = 'slug'
    #
    # def get(self, request, *args, **kwargs):
    #     player_form = self.player_form_class(request.POST)
    #     user_form = self.user_form_class(request.POST)
    #     # return render(request, self.template_name, {'playerobj': player_form,
    #     #                                             'userobj': user_form,
    #     #                                             'c': 'Player Registration: '})
    #     self.object = self.get_object()
    #     context = {'playerobj': player_form,
    #                'userobj': user_form,
    #                'c': 'Player Profile'}
    #     context = self.get_context_data(object=self.object)
    #     return self.render_to_response(self.get_context_data())
    #
    # def post(self, request, slug):
    #     user_form = self.user_form_class(request.POST)
    #     player_form = self.player_form_class(request.POST)
    #     print(str(self.request.user.slug) + " com on")
    #     self.slug_field = self.request.user.slug
    #     return render(request, self.template_name, {'playerobj': player_form,
    #                                                 'userobj': user_form,
    #                                                 'c': 'Player Registration: '})
    #
    # # def get_context_data(self, **kwargs):
    # #     context = super().get_context_data(**kwargs)
    # #     qs = Tournament.objects.all()
    # #     if str(self.request.user) != "AnonymousUser":
    # #         userobj = UserModel.objects.filter(slug=str(self.request.user))
    # #         playerobj = PlayerModel.objects.filter(user=self.request.user)
    # #         context = {"q": qs,
    # #                    "userobj": userobj,
    # #                    "playerobj": playerobj}
    # #
    # #     else:
    # #         context = {"q": qs}
    # #
    # #     return context
    # def get_context_data(self, **kwargs):
    #     context = super(ProfileUpdate, self).get_context_data(**kwargs)
    #     context['userobj'] = UserModel.objects.filter(slug=str(self.request.user))  # whatever you would like
    #     context['playerobj'] = PlayerModel.objects.filter(user=self.request.user)  # whatever you would like
    #     return context
    # # def get_context_data(self, **kwargs):
    # #     """Insert the form into the context dict."""
    # #     if 'form' not in kwargs:
    # #         kwargs['userobj'] = self.user_form_class
    # #         kwargs['playerobj'] = self.player_form_class
    # #     return super().get_context_data(**kwargs)
    #
    # def get_slug_field(self):
    #     return self.slug


