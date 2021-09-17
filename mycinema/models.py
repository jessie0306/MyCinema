from django.db import models

# Create your models here.
class Cinemas(models.Model):
    cine_id = models.AutoField(primary_key=True)
    cine_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    current_movies = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cinemas'


class Members(models.Model):
    member_id = models.CharField(primary_key=True, max_length=255)
    member_pw = models.CharField(max_length=255, blank=True, null=True)
    member_name = models.CharField(max_length=255, blank=True, null=True)
    member_tel = models.CharField(max_length=255, blank=True, null=True)
    resident_num = models.CharField(max_length=255, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    like_genre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'members'


class MovieSchedules(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    cine = models.ForeignKey(Cinemas, models.DO_NOTHING, blank=True, null=True)
    cine_name = models.CharField(max_length=255, blank=True, null=True)
    movie = models.ForeignKey('Movies', models.DO_NOTHING, blank=True, null=True)
    movie_name = models.CharField(max_length=255, blank=True, null=True)
    house_num = models.CharField(max_length=255, blank=True, null=True)
    movie_time = models.CharField(max_length=255, blank=True, null=True)
    movie_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_schedules'


class Movies(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    movie_name = models.CharField(max_length=255, blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    actor = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    age_limit = models.CharField(max_length=255, blank=True, null=True)
    story = models.TextField(blank=True, null=True)
    open_date = models.DateField(blank=True, null=True)
    close_date = models.DateField(blank=True, null=True)
    poster_src = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies'


class MymovieRe(models.Model):
    post_id = models.AutoField(primary_key=True)
    re_pw = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    cont = models.TextField(blank=True, null=True)
    like_genre = models.CharField(max_length=255, blank=True, null=True)
    bip = models.CharField(max_length=255, blank=True, null=True)
    bdate = models.DateTimeField(blank=True, null=True)
    readcnt = models.IntegerField(blank=True, null=True)
    gnum = models.IntegerField(blank=True, null=True)
    onum = models.IntegerField(blank=True, null=True)
    nested = models.IntegerField(blank=True, null=True)
    member = models.ForeignKey(Members, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mymovie_re'


class Nonmembers(models.Model):
    nm_id = models.AutoField(primary_key=True)
    nm_birth = models.DateField(blank=True, null=True)
    nm_tel = models.CharField(max_length=255, blank=True, null=True)
    nm_pw = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nonmembers'


class Tickets(models.Model):
    ticket_id = models.IntegerField(primary_key=True)
    ticket_date = models.DateTimeField(blank=True, null=True)
    cine_name = models.CharField(max_length=255, blank=True, null=True)
    seat = models.CharField(max_length=255, blank=True, null=True)
    movie = models.ForeignKey(Movies, models.DO_NOTHING, blank=True, null=True)
    movie_name = models.CharField(max_length=255, blank=True, null=True)
    member = models.ForeignKey(Members, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tickets'


class TicketsNm(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_date = models.DateTimeField(blank=True, null=True)
    cine_name = models.CharField(max_length=255, blank=True, null=True)
    seat = models.CharField(max_length=255, blank=True, null=True)
    movie_id = models.IntegerField(blank=True, null=True)
    movie_name = models.CharField(max_length=255, blank=True, null=True)
    nm = models.ForeignKey(Nonmembers, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tickets_nm'


class Voc(models.Model):
    post_id = models.AutoField(primary_key=True)
    voc_pw = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    cont = models.TextField(blank=True, null=True)
    voc_type = models.CharField(max_length=255, blank=True, null=True)
    bip = models.CharField(max_length=255, blank=True, null=True)
    bdate = models.DateTimeField(blank=True, null=True)
    readcnt = models.IntegerField(blank=True, null=True)
    gnum = models.IntegerField(blank=True, null=True)
    onum = models.IntegerField(blank=True, null=True)
    nested = models.IntegerField(blank=True, null=True)
    member = models.ForeignKey(Members, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'voc'