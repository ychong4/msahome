from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *
from django.http import HttpResponse
import csv
import datetime

def export_to_csv(modeladmin, request, queryset):
   opts = modeladmin.model._meta
   content_disposition = 'attachment; filename={opts.verbose_name}.csv'
   response = HttpResponse(content_type='text/csv')
   response['Content-Disposition'] = content_disposition
   writer = csv.writer(response)
   fields = [field for field in opts.get_fields() if not \
      field.many_to_many and not field.one_to_many]
   # Write a first row with header information
   writer.writerow([field.verbose_name for field in fields])
   # Write data rows
   for obj in queryset:
      data_row = []
      for field in fields:
         value = getattr(obj, field.name)
         if isinstance(value, datetime.datetime):
            value = value.strftime('%d/%m/%Y')
         data_row.append(value)
      writer.writerow(data_row)
   return response


export_to_csv.short_description = 'Export to CSV'

class CustomUserAdmin(UserAdmin):
   model = CustomUser
   add_form = CustomUserCreationForm
   form = CustomUserChangeForm
   list_display = ['username','last_name', 'first_name', 'address', 'city', 'state', 'zip', 'email', 'phone', 'team_id', 'referee_id']
   list_filter = ['username','last_name', 'first_name', 'address', 'city', 'state', 'zip', 'email', 'phone']
   list_editable = ['address', 'city', 'state', 'zip', 'phone', 'team_id', 'referee_id']
   search_fields = ['username','last_name', 'first_name', 'address', 'city', 'state', 'zip', 'email', 'phone']

class RefereeAdmin(admin.ModelAdmin):
   list_display = ['referee_ID', 'last_name', 'first_name', 'address', 'city', 'state', 'zip', 'email', 'phone']
   list_filter = ['referee_ID', 'last_name', 'first_name', 'address', 'city', 'state', 'zip', 'email', 'phone']
   search_fields = ['referee_ID', 'last_name', 'first_name', 'address', 'city', 'state', 'zip', 'email', 'phone']

class SchoolAdmin(admin.ModelAdmin):
   list_display = ['school_ID', 'school_name', 'school_street_address', 'school_city', 'school_state', 'school_zip']
   list_filter = ['school_ID', 'school_name', 'school_street_address', 'school_city', 'school_state', 'school_zip']
   search_fields = ['school_ID', 'school_name', 'school_street_address', 'school_city', 'school_state', 'school_zip']

class TeamAdmin(admin.ModelAdmin):
   list_display = ['team_ID', 'school_ID', 'team_name', 'team_coach', 'team_coach_email', 'team_coach_contact']
   list_filter = ['team_ID', 'school_ID', 'team_name', 'team_coach', 'team_coach_email', 'team_coach_contact']
   search_fields = ['team_ID', 'school_ID', 'team_name', 'team_coach', 'team_coach_email', 'team_coach_contact']

class PlayerAdmin(admin.ModelAdmin):
   list_display = ['player_ID', 'player_last_name', 'player_first_name', 'player_address', 'player_city', 'player_state', 'player_zip', 'player_email', 'player_phone', 'eligibility_status']
   list_filter = ['player_ID', 'player_last_name', 'player_first_name', 'player_address', 'player_city', 'player_state', 'player_zip', 'player_email', 'player_phone', 'eligibility_status']
   search_fields = ['player_ID', 'player_last_name', 'player_first_name', 'player_address', 'player_city', 'player_state', 'player_zip', 'player_email', 'player_phone', 'eligibility_status']

class TournamentAdmin(admin.ModelAdmin):
   list_display = ['tournament_ID', 'tournament_name']
   list_filter = ['tournament_ID', 'tournament_name']
   search_fields = ['tournament_ID', 'tournament_name']

def match_pdf(obj):
   url = reverse('admin_match_pdf', args=[obj.match_ID])
   return mark_safe(f'<a href="{url}">PDF</a>')
match_pdf.short_description = 'Information'

class MatchAdmin(admin.ModelAdmin):
   list_display = ['match_ID', 'match_tournament_ID', 'home_team_ID', 'guest_team_ID', 'time', 'date', 'match_referee_ID', match_pdf]
   list_filter = ['match_ID', 'match_tournament_ID', 'home_team_ID', 'guest_team_ID', 'time', 'date', 'match_referee_ID']
   search_fields = ['match_ID', 'match_tournament_ID', 'home_team_ID', 'guest_team_ID', 'time', 'date', 'match_referee_ID']
   actions = [export_to_csv]


class FieldAdmin(admin.ModelAdmin):
   list_display = ['field_ID', 'field_name', 'field_address', 'field_city', 'field_state', 'field_zip', 'field_owner_org', 'field_contact_name', 'field_contact_email', 'field_contact_phone', 'field_notes']
   list_filter = ['field_ID', 'field_name', 'field_address', 'field_city', 'field_state', 'field_zip', 'field_owner_org', 'field_contact_name', 'field_contact_email', 'field_contact_phone', 'field_notes']
   search_fields = ['field_ID', 'field_name', 'field_address', 'field_city', 'field_state', 'field_zip', 'field_owner_org', 'field_contact_name', 'field_contact_email', 'field_contact_phone', 'field_notes']

class ScoreAdmin(admin.ModelAdmin):
   list_display = ['score_ID', 'home_team_score','guest_team_score']
   list_filter = ['score_ID', 'home_team_score','guest_team_score']
   search_fields = ['score_ID', 'home_team_score','guest_team_score']




admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Referee, RefereeAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Score, ScoreAdmin)
