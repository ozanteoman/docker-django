from album.models import Album, Category, Song, Artist

# example one
# it will hit db for each song object

all_songs = Song.objects.all()
print(all_songs)

# end of the example one

# -------------------------- #

# example two
# only it will hit db two times

all_songs = Song.objects.all().prefetch_related("category")
print(all_songs)

# end of the example two

# ------------------------- #

# example three for understanding the meaning of self.toppings
# first step
song = Song.objects.first()
print(song.category.all())
# second step
song = Song.objects.prefetch_related("category").first()
print(song.category.all())
# end of the example three

# ---------------------------#
# example four
# step 1
songs = Song.objects.prefetch_related("category").all()[:100]
print([list(song.category.filter(is_visible=True)) for song in songs])
# -------------#
# step 2
song = songs.first()
print(song.category.filter(is_visible=True))
# end of the example four

#--------------------------#

# example five
song = Song.objects.prefetch_related("category").first()
print(song.category.all())
print(song.category.first())
# end of five example

#------------------------#

#example six
