from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    last_name = models.CharField(max_length=50, blank=False, null=True, default='')
    first_name = models.CharField(max_length=50, blank=False, null=True, default='')
    address = models.CharField(max_length=100, blank=False, null=True, default='-')
    city = models.CharField(max_length=50, blank=False, null=True, default='-')
    state = models.CharField(max_length=50, blank=False, null=True, default='-')
    zip = models.CharField(max_length=50, blank=True, null=True, default='00000')
    email = models.EmailField(max_length=100, default=' ')
    phone = models.CharField(max_length=50, default='(402)000-0000')
    referee_id = models.CharField(max_length= 10, blank=False, default='-')
    team_id = models.CharField(max_length=10, blank=False, default='-')

    def __str__(self):
        return str(self.first_name)

class Referee(models.Model):
    referee_ID = models.CharField(primary_key=True, max_length= 10, blank=False, null=False, default=' ')
    username = models.CharField(max_length=50, default=' ')
    last_name = models.CharField(max_length=50, blank=False, null=True, default='')
    first_name = models.CharField(max_length=50, blank=False, null=True, default='')
    address = models.CharField(max_length=100, blank=False, null=True, default='')
    city = models.CharField(max_length=50, blank=False, null=True, default='')
    state = models.CharField(max_length=50, blank=False, null=True, default='')
    zip = models.CharField(max_length=50, blank=True, null=True, default='00000')
    email = models.EmailField(max_length=100, default=' ')
    phone = models.CharField(max_length=50, default='(402)000-0000')

    def __str__(self):
        return str(self.first_name)

class School(models.Model):
    school_ID = models.CharField(primary_key=True, max_length= 10, blank=False, null=False, default=' ')
    school_name = models.CharField(max_length=50, blank=False, null=True, default='')
    school_street_address = models.CharField(max_length=100, blank=False, null=True, default='')
    school_city = models.CharField(max_length=50, blank=False, null=True, default='')
    school_state = models.CharField(max_length=50, blank=False, null=True, default='')
    school_zip = models.CharField(max_length=50, blank=True, null=True, default='00000')

    def __str__(self):
        return str(self.school_name)

class Team(models.Model):
    team_ID = models.CharField(primary_key=True, max_length= 10, blank=False, null=False, default=' ')
    team_name = models.CharField(max_length=50, blank=False, null=True, default='')
    team_coach = models.CharField(max_length=50, blank=False, null=True, default='')
    team_coach_email = models.EmailField(max_length=100, default=' ')
    team_coach_contact = models.CharField(max_length=50, default='(402)000-0000')
    school_ID = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school')

    def __str__(self):
        return str(self.team_name)

class Player(models.Model):
    player_ID = models.CharField(primary_key=True, max_length=10, blank=False, null=False, default=' ')
    player_last_name = models.CharField(max_length=50, blank=False, null=True, default='')
    player_first_name = models.CharField(max_length=50, blank=False, null=True, default='')
    player_address = models.CharField(max_length=100, blank=False, null=True, default='')
    player_city = models.CharField(max_length=50, blank=False, null=True, default='')
    player_state = models.CharField(max_length=50, blank=False, null=True, default='')
    player_zip = models.CharField(max_length=50, blank=True, null=True, default='00000')
    player_email = models.EmailField(max_length=100, default=' ')
    player_phone = models.CharField(max_length=50, default='(402)000-0000')
    eligibility_status = models.BooleanField(default=True)
    player_school_ID = models.ForeignKey(School, on_delete=models.CASCADE, related_name='School')
    player_team_ID = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='Team')
    player_yellowcards = models.IntegerField(blank=False, default=0)
    player_redcards = models.IntegerField(blank=False, default=0)

    def __str__(self):
        return str(self.player_first_name)

class Tournament(models.Model):
    tournament_ID = models.CharField(primary_key=True, max_length=10, blank=False, null=False, default=' ')
    tournament_name = models.CharField(max_length=50, blank=False, null=True, default='')

    def __str__(self):
        return str(self.tournament_name)

class Field(models.Model):
    field_ID = models.CharField(primary_key=True, max_length=10, blank=False, null=False, default=' ')
    field_name = models.CharField(max_length=50, blank=False, null=True, default='')
    field_address = models.CharField(max_length=100, blank=False, null=True, default='')
    field_city = models.CharField(max_length=50, blank=False, null=True, default='')
    field_state = models.CharField(max_length=50, blank=False, null=True, default='')
    field_zip = models.CharField(max_length=50, blank=True, null=True, default='00000')
    field_owner_org = models.CharField(max_length=50, blank=True, null=True, default=' ')
    field_contact_name = models.CharField(max_length=50, blank=False, null=True, default='')
    field_contact_email = models.EmailField(max_length=100, default=' ')
    field_contact_phone = models.CharField(max_length=50, default='(402)000-0000')
    field_notes = models.CharField(max_length=50, blank=True, null=True, default=' ')

    def __str__(self):
        return str(self.field_name)



class Match(models.Model):
    match_ID = models.CharField(primary_key=True, max_length=10, blank=False, null=False, default=' ')
    home_team_ID = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='Home_Team')
    guest_team_ID = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='Guest_Team')
    time = models.TimeField(auto_now=False)
    date = models.DateField(auto_now=False)
    match_tournament_ID = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='Tournament', default='')
    match_referee_ID = models.ForeignKey(Referee, on_delete=models.CASCADE, related_name='Referee', default='')
    home_team_score = models.CharField(max_length=50, default='0')
    guest_team_score = models.CharField(max_length=50, default='0')
    field_name = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='field', default='')
    referee_comment = models.CharField(max_length=200, default='N/A')
    match_detail = models.TextField(max_length=500, blank=True, default='N/A')



    def __str__(self):
        return str(self.match_ID)

class Score(models.Model):
    score_ID = models.CharField(primary_key=True, max_length=10, blank=False, null=False, default=' ')
    home_team_score = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='home_score', default='')
    guest_team_score = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='guest_score', default='')
    email = models.EmailField(max_length=100, default=' ')
    referee_comment = models.CharField(max_length=200, default='N/A')
    match_detail = models.TextField(max_length=500, blank=True, default='N/A')

    def __str__(self):
        return str(self.score_ID)
