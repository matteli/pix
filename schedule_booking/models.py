from django.db import models
from django.contrib.sites.models import Site
from django.core.validators import MaxValueValidator, MinValueValidator


class Config(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    school = models.BooleanField(
        default=True, help_text="Demande de l'établissement d'origine."
    )
    max_escort = models.PositiveIntegerField(
        default=0,
        help_text="Nombre maximal d'accompagnateurs. La valeur à 0 enlève la demande de cette information.",
    )
    max_slot = models.PositiveIntegerField(
        default=2,
        help_text="Nombre maximal de créneaux sélectionnable par inscription.",
    )
    show_people = models.BooleanField(
        default=True,
        help_text="Montrer le nombre de persone ou de groupe de personnes.",
    )
    caution_level = models.PositiveIntegerField(
        default=80,
        help_text="Taux d'occupation à partir duquel le créneau passe en orange. Si 100, le niveau n'est pas utilisé.",
    )
    warning_level = models.PositiveIntegerField(
        default=90,
        help_text="Taux d'occupation à partir duquel le créneau passe en rouge. Si 100, le niveau n'est pas utilisé.",
    )
    forbidden_level = models.PositiveIntegerField(
        default=100,
        help_text="Taux d'occupation à partir duquel l'insciption n'est plus possible. Devrait être à 100.",
    )
    recaptcha = models.BooleanField(
        default=False,
        help_text="Ajoute le recaptcha de Google pour empêcher les robots de s'inscrire.",
    )
    recaptcha_private = models.CharField(
        max_length=40, blank=True, help_text="Clé utilisée entre le serveur et google."
    )
    recaptcha_public = models.CharField(
        max_length=40,
        blank=True,
        help_text="Clé utilisée entre le client et le serveur.",
    )
    send_email_confirmation = models.BooleanField(
        default=False, help_text="Envoie un email de confirmation d'inscription."
    )
    beta_test = models.BooleanField(
        default=True,
        help_text="Permet d'afficher des messages qui préviennent les visiteurs que le site en version de test.",
    )
    rgpd = models.BooleanField(
        default=True,
        help_text="Permet d'afficher des messages en rapport au RGPD.",
    )

    def __str__(self):
        return self.site.name


class Place(models.Model):
    name = models.CharField(max_length=100, help_text="Nom du lieu")
    gauge = models.IntegerField(help_text="Jauge maxi")
    order = models.IntegerField(
        help_text="Numéro pour ordonner l'affichage des lieux", default=0
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        schedules = Schedule.objects.all()
        for s in schedules:
            a = Appointment(id="%s-%s" % (self.id, s.id), place=self, schedule=s)
            a.save()


class Schedule(models.Model):
    datetime = models.DateTimeField(help_text="Date et heure du créneau")
    authorizeds = models.CharField(
        max_length=300,
        default="CS CB AU",
        help_text="Authorisation en fonction de l'école (groupes espacés de 2 lettres)",
    )

    class Meta:
        ordering = ["datetime"]

    def __str__(self):
        return self.datetime.isoformat()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        places = Place.objects.all()
        for p in places:
            a = Appointment(id="%s-%s" % (p.id, self.id), place=p, schedule=self)
            a.save()


class Student(models.Model):
    SCHOOLS_CHOICE = [
        ("1G01", "1G01"),
        ("1G02", "1G02"),
        ("1G03", "1G03"),
        ("1G04", "1G04"),
        ("1G05", "1G05"),
        ("1G06", "1G06"),
        ("1G07", "1G07"),
        ("1G08", "1G08"),
        ("1G09", "1G09"),
        ("1ST2S1", "1ST2S1"),
        ("1ST2S2", "1ST2S2"),
        ("1ST2S3", "1ST2S3"),
        ("1STI2D1", "1STI2D1"),
        ("1STI2D2", "1STI2D2"),
        ("1STI2D3", "1STI2D3"),
        ("1STI2D4", "1STI2D4"),
        ("1STI2D5", "1STI2D5"),
        ("1STL", "1STL"),
        ("1STMG1", "1STMG1"),
        ("1STMG2", "1STMG2"),
        ("1STMG3", "1STMG3"),
        ("1STMG4", "1STMG4"),
        ("201", "201"),
        ("202", "202"),
        ("203", "203"),
        ("204", "204"),
        ("205", "205"),
        ("206", "206"),
        ("207", "207"),
        ("208", "208"),
        ("209", "209"),
        ("210", "210"),
        ("211", "211"),
        ("212", "212"),
        ("213", "213"),
        ("214", "214"),
        ("215", "215"),
        ("216", "216"),
        ("217", "217"),
        ("AERO1", "AERO1"),
        ("AERO2", "AERO2"),
        ("AMCRCI1", "AMCRCI1"),
        ("AMCRCI2", "AMCRCI2"),
        ("CICN1", "CICN1"),
        ("CICN2", "CICN2"),
        ("CPRP1", "CPRP1"),
        ("CPRP2", "CPRP2"),
        ("EL1", "EL1"),
        ("EL2", "EL2"),
        ("MCO1", "MCO1"),
        ("MCO2", "MCO2"),
        ("MGI", "MGI"),
        ("MLDS", "MLDS"),
        ("PC2", "PC2"),
        ("PCSI", "PCSI"),
        ("SAM1", "SAM1"),
        ("SAM2", "SAM2"),
        ("SNIR2", "SNIR2"),
        ("SP3S1", "SP3S1"),
        ("SP3S2", "SP3S2"),
        ("SPTSI", "SPTSI"),
        ("SUTSI", "SUTSI"),
        ("TG01", "TG01"),
        ("TG02", "TG02"),
        ("TG03", "TG03"),
        ("TG04", "TG04"),
        ("TG05", "TG05"),
        ("TG06", "TG06"),
        ("TG07", "TG07"),
        ("TG08", "TG08"),
        ("TG09", "TG09"),
        ("TST2S1", "TST2S1"),
        ("TST2S2", "TST2S2"),
        ("TST2S3", "TST2S3"),
        ("TSTI2D1", "TSTI2D1"),
        ("TSTI2D2", "TSTI2D2"),
        ("TSTI2D3", "TSTI2D3"),
        ("TSTI2D4", "TSTI2D4"),
        ("TSTI2D5", "TSTI2D5"),
        ("TSTL", "TSTL"),
        ("TSTMG1", "TSTMG1"),
        ("TSTMG2", "TSTMG2"),
        ("TSTMG3", "TSTMG3"),
        ("TSTMG4", "TSTMG4"),
    ]

    class Meta:
        ordering = ["email"]

    lastname = models.CharField(max_length=100, verbose_name="Nom")
    firstname = models.CharField(max_length=100, verbose_name="Prénom")
    school = models.CharField(
        max_length=4,
        choices=SCHOOLS_CHOICE,
        default="AU02",
        verbose_name="Etablissement d'origine",
    )
    email = models.EmailField(
        unique=True,
        error_messages={"unique": "Un visiteur avec cet email s'est déjà inscrit."},
    )
    people = models.IntegerField(default=1, verbose_name="Nombre de personne")

    def __str__(self):
        return "%s %s <%s>" % (self.firstname, self.lastname, self.email)


class Appointment(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return "%s, %s" % (self.schedule, self.place)
