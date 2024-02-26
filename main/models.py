# main/models.py
import os
from django.db import models

class College(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True)
    
    logo = models.ImageField(upload_to='college_logos/', blank=True)
    sports = models.ManyToManyField('Sport', through='Team', related_name='colleges')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Call the "real" save() method.
        super().save(*args, **kwargs)

        # Create a new Team instance for each sport.
        for sport in self.sports.all():
            team, created = Team.objects.get_or_create(college=self, sport=sport)

class Payment(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    reference_code = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"Payment for {self.college.name} - {self.reference_code}"

class Sport(models.Model):
    name = models.CharField(max_length=100)
    sport_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
    
class Team(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, default=1)

    def sports_list(self):
        return self.college.sports.all()

    def __str__(self):
        return f"{self.college.name} - {self.sport.name}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name
    
def upload_path(instance, filename):
    # This function defines the upload path for fixtures and rules files
    return f'sport_info/{instance.sport.name}/{filename}'

class SportInformation(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    fixtures = models.FileField(upload_to=upload_path, null=True, blank=True)
    rules_and_regulations = models.FileField(upload_to=upload_path, null=True, blank=True)

    def __str__(self):
        return f"{self.sport.name} Information"
    
def team_member_image_upload(instance, filename):
    # The image file will be uploaded to MEDIA_ROOT/team_images/<username>.<file_extension>
    file_extension = filename.split('.')[-1]
    return f'team_images/{instance.name}.{file_extension}'

class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    image = models.ImageField(upload_to=team_member_image_upload)
    instagram_profile = models.URLField(blank=True)
    mail_profile = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)

    def __str__(self):
        return self.name
    
def get_upload_path(instance, filename):
    return os.path.join('carousel_images', filename)

class CarouselSlide(models.Model):
    image = models.ImageField(upload_to=get_upload_path)
    alt_text = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.alt_text:
            # If alt_text is not provided, use the file name without extension
            self.alt_text = os.path.splitext(os.path.basename(self.image.name))[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.alt_text
    
class Complaint(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    college = models.CharField(max_length=100)
    category = models.ForeignKey(Sport, on_delete=models.CASCADE)
    complaint = models.TextField()

    def __str__(self):
        return f"Complaint from {self.name} - {self.category.name}"
    
class TeamCaptain(models.Model):
    phone = models.CharField(max_length=20, blank=True)
    captain_name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.captain_name} - {self.college.name} - {self.sport.name}"


class GameResult(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    team_a = models.CharField(max_length=50)
    team_b = models.CharField(max_length=50)
    score_a = models.CharField(max_length=10)
    score_b = models.CharField(max_length=10)
    result = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sport.name} - {self.team_a} vs {self.team_b}"
