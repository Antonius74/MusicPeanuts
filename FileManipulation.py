
from mutagen.id3 import ID3, APIC

audio = ID3("/home/Antonius/PycharmProjects/MusicPeanuts/file/Franco Battiato - L'ombra della luce.mp3")

with open('/home/Antonius/PycharmProjects/MusicPeanuts/temp/img/default.jpg', 'rb') as albumart:
    audio['APIC'] = APIC(
                      encoding=3,
                      mime='image/jpeg',
                      type=3, desc=u'Cover',
                      data=albumart.read()
                    )

audio.save()