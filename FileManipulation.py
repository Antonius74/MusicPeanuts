from mutagen.id3 import ID3, APIC
import urllib.request

audio = ID3("/Users/antoniolatela//PycharmProjects/MusicPeanuts/file/Pink Floyd - The Dark Side of the Moon - Eclipse (FLAC).mp3")

urllib.request.urlretrieve("https://i.ytimg.com/vi/BV-ASc0qkrM/hqdefault.jpg?sqp=-oaymwEXCPYBEIoBSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLAz44oMpt3IkVu5a2TSIIJkftyqPw", "./local-filename.jpg")

with open('./local-filename.jpg', 'rb') as albumart:
    audio['APIC'] = APIC(
                      encoding=3,
                      mime='image/jpeg',
                      type=3, desc=u'Cover',
                      data=albumart.read()
                    )

audio.save()
