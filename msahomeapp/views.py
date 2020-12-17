from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.template.loader import render_to_string
from .forms import *
from .models import *
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# import weasyprint
from io import BytesIO


def is_Referee(username):
    return Referee.objects.filter(username=username).exists()


# Create your views here.
def SignUpView(request):
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        referee_id = form.cleaned_data.get('referee_id')
        username = form.cleaned_data.get('username')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        address = form.cleaned_data.get('address')
        city = form.cleaned_data.get('city')
        state = form.cleaned_data.get('state')
        zip = form.cleaned_data.get('zip')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        password1 = form.cleaned_data.get('password1')
        Referee.objects.create(referee_ID=referee_id, username=username, email=email, first_name=first_name,
                               last_name=last_name,
                               address=address, city=city, state=state, zip=zip, phone=phone)
        CustomUser.objects.create_user(referee_id=referee_id, username=username, email=email, first_name=first_name,
                                       last_name=last_name,
                                       address=address, city=city, state=state, zip=zip, phone=phone,
                                       password=password1)

        return redirect('login')
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


@login_required()
def referee_landing(request):
    username = Referee.username
    return render(request, "msahome/referee_landing.html", {'username': username})


@login_required()
def coach_landing(request):
    username = CustomUser.username
    return render(request, "msahome/coach_landing.html", {'username': username})


@login_required
def login_landing(request):
    current_user = request.user
    if current_user.is_staff:
        return coach_landing(request)
    elif is_Referee(current_user):
        return referee_landing(request)
    else:
        return render(request, "msahome/referee_landing.html")


def home(request):
    return render(request, 'msahome/home.html',
                  {'home': home})


def about_us(request):
    return render(request, 'msahome/about_us.html',
                  {'about_us': about_us})


def contact_us(request):
    return render(request, 'msahome/contact_us.html',
                  {'contact_us': contact_us})


@login_required
def matches_new(request):
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            matches = form.save(commit=False)
            matches.save()
            matches = Match.objects.filter()
            return render(request, 'msahome/matches_list.html',
                          {'matches': matches})
    else:
        form = MatchForm()
        # print("Else")
    return render(request, 'msahome/matches_new.html', {'form': form})


def matches_list(request, pk):
    match_list = Match.objects.filter(match_tournament_ID=pk)
    page = request.GET.get('page', 1)

    paginator = Paginator(match_list, 5)
    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    return render(request, 'msahome/matches_list.html', {'matches': matches})


@login_required
def referee_matches_list(request):
    match_referee_ID = request.user.referee_id
    match_list = Match.objects.filter(match_referee_ID=match_referee_ID)
    page = request.GET.get('page', 1)

    paginator = Paginator(match_list, 5)
    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    return render(request, 'msahome/referee_matches_list.html', {'matches': matches})


@login_required
def referee_matches_edit(request, pk):
    matches = get_object_or_404(Match, pk=pk)
    if request.method == "POST":
        form = MatchForm(request.POST, instance=matches)
        if form.is_valid():
            matches = form.save()
            matches.save()
            matches = Match.objects.filter()
            return render(request, 'msahome/referee_matches_list.html', {'matches': matches})
    else:
        # print("else")
        form = MatchForm(instance=matches)
    return render(request, 'msahome/referee_matches_edit.html', {'form': form})


@login_required
def referee_matches_delete(request, pk):
    matches = get_object_or_404(Match, pk=pk)
    matches.delete()
    return redirect('referee_matches_list')


@login_required
def players_new(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            players = form.save(commit=False)
            players.save()
            players = Player.objects.filter()
            return render(request, 'msahome/players_list.html',
                          {'players': players})
    else:
        form = PlayerForm()
        # print("Else")
    return render(request, 'msahome/players_new.html', {'form': form})


def players_list(request):
    players_list = Player.objects.filter()
    page = request.GET.get('page', 1)

    paginator = Paginator(players_list, 5)
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)
    return render(request, 'msahome/players_list.html', {'players': players})


@login_required
def players_edit(request, pk):
    players = get_object_or_404(Player, pk=pk)
    if request.method == "POST":
        form = PlayerForm(request.POST, instance=players)
        if form.is_valid():
            players = form.save()
            players.save()
            players = Player.objects.filter()
            return render(request, 'msahome/players_list.html', {'players': players})
    else:
        # print("else")
        form = PlayerForm(instance=players)
    return render(request, 'msahome/players_edit.html', {'form': form})


@login_required
def players_delete(request, pk):
    players = get_object_or_404(Player, pk=pk)
    players.delete()
    return redirect('players_list')


@login_required
def coach_players_new(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            players = form.save(commit=False)
            players.save()
            players = Player.objects.filter()
            return render(request, 'msahome/coach_players_list.html',
                          {'players': players})
    else:
        form = PlayerForm()
        # print("Else")
    return render(request, 'msahome/coach_players_new.html', {'form': form})


@login_required
def coach_players_list(request):
    players_team_ID = request.user.team_id
    players_list = Player.objects.filter(player_team_ID=players_team_ID)
    page = request.GET.get('page', 1)

    paginator = Paginator(players_list, 5)
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)
    return render(request, 'msahome/coach_players_list.html', {'players': players})


@login_required
def coach_players_edit(request, pk):
    players = get_object_or_404(Player, pk=pk)
    if request.method == "POST":
        form = PlayerForm(request.POST, instance=players)
        if form.is_valid():
            players = form.save()
            players.save()
            players = Player.objects.filter()
            return render(request, 'msahome/players_list.html', {'players': players})
    else:
        # print("else")
        form = PlayerForm(instance=players)
    return render(request, 'msahome/coach_players_edit.html', {'form': form})


@login_required
def coach_players_delete(request, pk):
    players = get_object_or_404(Player, pk=pk)
    players.delete()
    return redirect('coach_players_list')


@login_required
def team_summary(request):
    team_ID = request.user.team_id
    home_matches = Match.objects.filter(home_team_ID=team_ID)
    guest_matches = Match.objects.filter(guest_team_ID=team_ID)
    return render(request, 'msahome/coach_team_summary.html',
                  {'home_matches': home_matches, 'guest_matches': guest_matches})


def tournaments_list(request):
    tournaments_list = Tournament.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(tournaments_list, 5)
    try:
        tournaments = paginator.page(page)
    except PageNotAnInteger:
        tournaments = paginator.page(1)
    except EmptyPage:
        tournaments = paginator.page(paginator.num_pages)
    return render(request, 'msahome/tournaments.html',
                  {'tournaments': tournaments})


def teams_list(request, pk):
    teams = Team.objects.filter(school_ID=pk)
    return render(request, 'msahome/teams_list.html', {'teams': teams})


def schools_list(request):
    schools_list = School.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(schools_list, 5)
    try:
        schools = paginator.page(page)
    except PageNotAnInteger:
        schools = paginator.page(1)
    except EmptyPage:
        schools = paginator.page(paginator.num_pages)
    return render(request, 'msahome/schools_list.html',
                  {'schools': schools})


def players_list(request, pk):
    players_list = Player.objects.filter(player_team_ID=pk)
    page = request.GET.get('page', 1)

    paginator = Paginator(players_list, 5)
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)
    return render(request, 'msahome/players_list.html', {'players': players})


def about_us(request):
    return render(request, 'msahome/about_us.html', {'soccer': about_us})


def scores_report(request, match_ID):
    match = get_object_or_404(Match, match_ID=match_ID)
    if request.method == "POST":
        form = ScoresForm(request.POST, instance=match)
        if form.is_valid():
            subject = 'Your Match Information'
            from_email = 'ychongdjangotest@gmail.com'
            to_email = form.cleaned_data['email']
            message = 'Please, find attached the match information.'
            email = EmailMultiAlternatives(subject, message, from_email, [to_email])
            # generate PDF
            html = render_to_string('msahome/pdf.html', {'match': match})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/admin/css/base.css')]
            weasyprint.HTML(string=html).write_pdf(out,
                                                   stylesheets=stylesheets)
            email.attach(f'match_{match.match_ID}.pdf', out.getvalue(), 'application/pdf')
            email.send()
            return redirect('successView')

    else:
        form = ScoresForm(instance=match)
    return render(request, 'msahome/scores_report.html', {'form': form})


def successView(request):
    return render(request, 'msahome/successView.html',
                  {'successView': successView})


# def tournamentslist(request, pk):
# match = Match.objects.filter(match_tournament_ID=pk)
# return render(request, 'msahome/tournamentslist.html',
#               {'tournamentslist': match})


def admin_match_pdf(request, match_ID):
    match = get_object_or_404(Match, match_ID=match_ID)
    html = render_to_string('msahome/pdf.html',
                            {'match': match})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=match_{match.match_ID}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT + '/admin/css/base.css')])
    return response
