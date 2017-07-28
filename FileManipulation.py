from mutagen.id3 import ID3, APIC
import urllib.request
import configparser
import sys
import os

class FileManipulation:
    __config = configparser.RawConfigParser()
    __config.read('ConfigFile.properties')
    __tempImgDir = __config.get('Directory', 'Directory.TempImgDir')


    def __init__(self):
        None

    def setImage (self, filename, imgURL,  localTempImage):
        try:

            print (filename, imgURL, self.__tempImgDir + localTempImage)


            audio = ID3(filename)

            urllib.request.urlretrieve(imgURL, self.__tempImgDir + localTempImage)

            with open(self.__tempImgDir + localTempImage, 'rb') as albumart:
                audio['APIC'] = APIC(
                                  encoding=3,
                                  mime='image/jpeg',
                                  type=3, desc=u'Cover',
                                  data=albumart.read()
                                )
            audio.save()
            os.remove(self.__tempImgDir + localTempImage)
        except Exception as e:
            sys.stderr.write("[Error] Problem during file manipulation: " + str(e))

#fm = FileManipulation()
#fm.setImage( "/Users/antoniolatela/PycharmProjects/MusicPeanuts/file/3719.mp3", "https://i.ytimg.com/vi/zEYJrBoxvOE/default.jpg",  "pippo.jpg")
