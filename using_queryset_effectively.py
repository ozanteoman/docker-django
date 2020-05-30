from album.models import Song

# For lazy queryset
# first example
song_queryset = Song.objects.filter(album__in=[1, 2])

for song in song_queryset:
    print(song.name)

# second example

song_queryset_1 = Song.objects.filter(album_id=1)
song_queryset_2 = song_queryset_1.filter(category__in=[1, 2])
song_list = list(song_queryset_2)

# for queryset caching
# first example
song_queryset = Song.objects.filter(album__in=[1, 2])
# The query is executed and cached.
for song in song_queryset:
    print(song.name)
# The cache is used and the query won't be executed
for song in song_queryset:
    print(song.name)

# second example
# The following will create two QuerySet's, evaluate them, and throws them away,
# because they are not saving the queryset anywhere to reuse them later.
print([song.name for song in Song.objects.filter(album__in=[1, 2])])
print([song.album.title for song in Song.objects.select_related('album').filter(album__in=[1, 2])])

# Following code saves QuerySet in a variable. When it evaluates,
# it saves the results to its cache(_result_cache).
song_queryset = Song.objects.select_related('album').filter(album_id=[1, 2])
for song in song_queryset:
    print(song.name)

# Using cache from previous evaluation.
song_queryset = Song.objects.select_related('album').filter(album_id=[1, 2])
for song in song_queryset:
    print(song.album.title)

# third example
# slicing
# You can't use filter to queryset anymore.
song_queryset = Song.objects.all()[10:100]
# You can use filter song_queryset_1 but not to song_queryset_2 , song_queryset_3
song_queryset_1 = Song.objects.all()
song_queryset_2 = song_queryset_1[1:10]
song_queryset_3 = song_queryset_2[2:5]

# saves results to cache of song_queryset_1
lst1 = [each.blog.id for each in song_queryset_1]
# saves results to cache of song_queryset_2
lst2 = [each.blog.id for each in song_queryset_2]
# saves results to cache of song_queryset_3
lst3 = [each.blog.id for each in song_queryset_3]

# third-one example
song_queryset = Song.objects.all()
# hit the db
song_list = list(song_queryset)
first_ten_song = song_queryset[:10]
first_five = first_ten_song[:5]

# third-two example
song_queryset = Song.objects.all()
# Queries the database because queryset hasn't been evaluated yet.
print(song_queryset[5])

song_list = list(song_queryset)
# Using cache because evaluation happened in previous list() operation.
print(song_queryset[5])
print(song_queryset[10])

# fourth example
# len() evaluates and saves results to cache.
song_queryset = Song.objects.filter(album_id=1)
ln = len(song_queryset)
# Using cache from previous evaluation.
for song in song_queryset:
    print(song.name)

# fifth example
# Evaluates the queryset and saves results in cache.
song_queryset = Song.objects.filter(album_id=1)
song_list = list(song_queryset)
# Using cache from previous list() evaluation.
for song in song_queryset:
    print(song.name)

# sixth example
# The `if` statement evaluates the queryset and saves results in cache.
song_queryset = Song.objects.filter(album_id=1)
if song_queryset:
    # Using cache from previous if statement evaluation.
    for song in song_queryset:
        print(song.name)

#sixth - one example
song_queryset = Song.objects.filter(album_id=1)
# The `if` statement evaluates the queryset.
if song_queryset:
    print("Yes , songs are existence")

#sixth - three example
song_queryset = Song.objects.filter(album_id=1)
# The `if` statement evaluates the queryset.
if song_queryset.exists():
    print("Yes , songs are existence")



