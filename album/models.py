from django.db import models


class Artist(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Album(models.Model):
    artist = models.ForeignKey(to=Artist, on_delete=models.CASCADE, related_name="album", null=False)
    category = models.ManyToManyField(to=Category)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True)
    cover_image = models.URLField(null=True, max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class Song(models.Model):
    album = models.ForeignKey(to=Album, on_delete=models.CASCADE, related_name="song")
    category = models.ManyToManyField(to=Category)
    name = models.CharField(max_length=50)
    cover_image = models.URLField(null=True, max_length=255)
    sound_file = models.FileField(null=True)

    def __str__(self):
        return f"{self.name} - {self.category.all()}"
