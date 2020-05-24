import time

from django.db.models import Prefetch
from django.db import connection, reset_queries

from album.models import Album, Category, Song, Artist

# example one
# it will hit db for each song object

all_songs = Song.objects.all()[:20]
print(all_songs)

# end of the example one

# -------------------------- #

# example two
# only it will hit db two times

all_songs = Song.objects.all().prefetch_related("category")[:20]
print(all_songs)

# end of the example two

# ------------------------- #

# example three for understanding the meaning of self.toppings
# Dikkat etmemiz gereken bir konu , normal querysetin çalışma mantığınd
# first step
song = Song.objects.first()
print(song.category.all())
# second step
song = Song.objects.prefetch_related("category").first()
print(song.category.all())
# end of the example three

# ---------------------------#
# Şuna dikkat etmek gerekirse ,  her bir database sorgusu bir önceki sorguyu ezdiği için
# example four
# step 1
songs = Song.objects.prefetch_related("category").all()[:100]
print([list(song.category.filter(is_visible=True)) for song in songs])
# -------------#
# step 2
song = songs.first()
print(song.category.filter(is_visible=True))
# end of the example four

# --------------------------#
# Aynı zaman da first() , last() gibi
# example five
song = Song.objects.prefetch_related("category").first()
print(song.category.all())
print(song.category.first())
# end of five example

# ------------------------#

# example six
# İlişkili alanların ilişkili alanlarını da kullanmak için birleştirme yapılabilir.
# teker teker çağır.
Album.objects.all()
Album.objects.prefetch_related("song")
Album.objects.prefetch_related("song__category")
# end of the example six

# -------------------#

# example seven
# Burada çalışacak sorgu da 3 kez veritabanına gidecektir.
# burada üç kez databaseye gidecektir.
Song.objects.prefetch_related('album__category').all()
# burada ise iki kez databaseye gidecektir.
Song.objects.select_related('album').prefetch_related('album__category').all()
# end of the example

# ------------------- #

# example eight
# prefetch nesnesi ile çalışmak.
Album.objects.prefetch_related("song__category")
# iki kullanımda da herhangi bir fark görülmeketedir
Album.objects.prefetch_related(Prefetch("song__category"))
# end of the example eight

# ----------------- #

# example nine
# queryset argümanı ile birlikte özel bir sorgu ayarlanabilir.
all_category = Category.objects.all().order_by('-id')
Song.objects.prefetch_related(Prefetch("category", queryset=all_category))
# end of the example nine

# ---------------- #

# example ten
# prefetch select_related ile birlikte kullanılabilir.
# step 1
album = Album.objects.filter(is_visible=False)
categories = Category.objects.all().prefetch_related(Prefetch("album_set", queryset=album)).all()
for category in categories:
    for album in category.album_set.all():
        print(album.artist)
# step 2
album = Album.objects.select_related("artist").filter(is_visible=False)
categories = Category.objects.all().prefetch_related(Prefetch("album_set", queryset=album)).all()
for category in categories:
    for album in category.album_set.all():
        print(album.artist)
# end of the example

# ------------------ #

# example eleven
# to_attr
# step 1
invisible_albums = Album.objects.filter(is_visible=False)
visible_albums = Album.objects.filter(is_visible=True)
categories = Category.objects.prefetch_related(
    Prefetch("album_set", queryset=invisible_albums, to_attr="invisible_albums"),
    Prefetch("album_set", queryset=visible_albums)
)
# step 2
category = Category.objects.prefetch_related(
    Prefetch("album_set", queryset=invisible_albums, to_attr="invisible_albums"),
    Prefetch("album_set", queryset=visible_albums)
).first()
# end of eleven

# ---------------#

# example twelve
# step 1
reset_queries()
start = time.perf_counter()

songs_categories = []
songs = Song.objects.all()[:1000]
for song in songs:
    songs_categories.append(list(song.category.all()))

end = time.perf_counter()
print(f"Finished in : {(end - start):.2f}s")
print("query count", len(connection.queries))
# step 2
reset_queries()
start = time.perf_counter()

songs_categories = []
songs = Song.objects.prefetch_related("category").all()[:1000]
for song in songs:
    songs_categories.append(list(song.category.all()))

end = time.perf_counter()
print(f"Finished in : {(end - start):.2f}s")
print("query count", len(connection.queries))
