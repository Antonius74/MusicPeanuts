import pafy
import sys
import shutil
import os
import pexpect
import configparser
import json
from MPytSearchEngine import YTSearchEngine


class YTDecodeStream:
    __fileFormat = "mp3"
    __ReferencePoint = ""
    __filename = ""
    __YTFile = None
    __YTFileInfo = None
    __config = configparser.RawConfigParser()
    __config.read('ConfigFile.properties')
    __ffmpegExe = __config.get('ffmpeg', 'ffmpeg.LocalPath')
    __tempDir = __config.get('Directory', 'Directory.TempDir')
    __fileDir = __config.get('Directory', 'Directory.FileDir')
    __playURL = __config.get('YTConfig', 'YTConfig.PlayURL')

    def __init__(self):
        None

    def __setGlobalEnv(self, args):
        if len(args) == 1:
            sys.stdout.write("Please use YTdownload URL -f format (mp3, mp4; if empty default mp3)")
            quit()

        try:
            if (len(args) > 2 and str(args[2].strip()) == "-f"):
                __fileFormat = args[3].lower();
                if __fileFormat == "mp4":
                    sys.stdout.write("[Info] Apply MP4 format.\n")
                    self.__fileFormat = "mp4"
                elif __fileFormat == "mp3":
                    sys.stdout.write("\n[Info] Apply MP3 format.\n")
                    self.__fileFormat = "mp3"
                elif __fileFormat == "avi":
                    sys.stdout.write("[Info] Apply AVI format.\n")
                    self.__fileFormat = "avi"
                else:
                    sys.stdout.write("[Warning] Format not found -> apply default MP3 format.\n")
            else:
                sys.stdout.write("[Info] Format not found -> apply default MP3 format.\n")
        except Exception as e:
            sys.stdout.write("[Warning] Format not found -> apply default MP3 format.\n")

        try:
            self.__ReferencePoint = args[1]
            if args[1].lower().startswith("^http"):
                self.__YTFile = pafy.new(self.__ReferencePoint)
            else:
                self.__YTFile = pafy.new(self.__playURL + self.__ReferencePoint)
        except Exception as e:
            sys.stderr.write("[Error] URL Not found, please retry." + str(e) + " Reference Point: " + self.__ReferencePoint)
            return False

    def __dwnldYTFile(self):
        try:
            if self.__fileFormat is "mp3":
                self.__YTFileInfo = self.__YTFile.getbestaudio()
            else:
                self.__YTFileInfo = self.__YTFile.getbest()
            self.__filename = str(os.getpid())
            print ("[Info] Preprarind Download -> " + self.__YTFileInfo.title + " - Reference Point: " + self.__ReferencePoint)
            self.__YTFileInfo.download(quiet=True, callback=self.__stdoutDownload,
                                                     filepath=self.__tempDir + self.__filename)
        except Exception as e:
            sys.stderr.write("[Error] Problem during download stream: " + str(e) + " - Reference Point: " + self.__ReferencePoint)
            return False

    def __cnvrtYTFile(self):
        try:
            if self.__fileFormat is "mp3":
                cmdMP3 = self.__ffmpegExe + "ffmpeg -hide_banner -y -i \"" + self.__tempDir + self.__filename + "\" -codec:a libmp3lame -qscale:a 1 \"" + self.__fileDir + self.__filename + ".mp3\""
                self.__execConversion(cmdMP3)
                self.__renameFile(self.__fileDir + self.__filename + ".mp3", self.__fileDir + self.__YTFileInfo.title + ".mp3")
            elif self.__fileFormat is "avi":
                cmdAVI = self.__ffmpegExe + "ffmpeg -hide_banner -y -async 1 -i \"" + self.__tempDir + self.__filename + "\" -f avi -b 700k -qscale 0 -ab 160k -ar 44100 \"" + self.__fileDir + self.__filename + ".avi\""
                self.__execConversion(cmdAVI)
                self.__renameFile(self.__fileDir + self.__filename + ".avi", self.__fileDir + self.__YTFileInfo.title + ".avi")
            elif self.__fileFormat is "mp4":
                if self.__YTFileInfo.extension == "webm":
                    cmdMP4 = self.__ffmpegExe + "ffmpeg  -hide_banner -y -async 1 -i \"" + self.__tempDir + self.__filename + "\" -f mp4 -vcodec libx264 -preset fast -profile:v main -acodec aac \"" + self.__fileDir + self.__filename + ".mp4\""
                    self.__execConversion(cmdMP4)
                    self.__renameFile(self.__fileDir + self.__filename + ".mp4", self.__fileDir + self.__YTFileInfo.title + ".mp4")

                elif self.__YTFileInfo.extension == "mp4":
                    shutil.move(self.__tempDir + self.__filename, self.__fileDir + self.__YTFileInfo.title + ".mp4")
                None
        except Exception as e:
            sys.stderr.write("[Error] Problem during stream download: " + str(e) + " - Reference Point: " + self.__ReferencePoint)
            return False

    def __execConversion(self, cmd):
        try:
            thread = pexpect.spawn(cmd)
            cpl = thread.compile_pattern_list([
                pexpect.EOF,
                "size(.*)"
            ])
            while True:
                i = thread.expect_list(cpl, timeout=None)
                if i == 0:
                    break
                elif i == 1:
                    frame_number = thread.match.group(0)
                    self.__stdoutConvert(str(frame_number))
                    thread.close
                elif i == 2:
                    pass
        except Exception as e:
            sys.stderr.write("[Error] Problem during stream conversion: " + str(e) + " - Reference Point: " + self.__ReferencePoint)

    def __stdoutDownload(self, total, recvd, ratio, rate, eta):
        percent = (recvd / total) * 100
        sys.stdout.write("\r[Info] Prepare file from YT -> %d%%" % round(percent))
        sys.stdout.flush()

    def __stdoutConvert(self, frame_number):
            sys.stdout.write("\r[Info] Converting file to " + self.__fileFormat.upper() + " -> " + frame_number[
                                                                                            frame_number.index(
                                                                                                "size") + 5:frame_number.index(
                                                                                                "size") + 15].strip())
            sys.stdout.flush()

    def __destryDwnldFile(self):
        try:
            os.remove(self.__tempDir + self.__filename)
        except Exception as e:
            sys.stderr.write("[Error] Problem during file deleting: " + str(e) + " - Reference Point: " + self.__ReferencePoint)

    def __renameFile(self, pid, __filename):
        try:
            os.renames(pid, __filename)
            self.__destryDwnldFile()
        except Exception as e:
            sys.stderr.write("[Error] Problem during file renaming: " + str(e) + " - Reference Point: " + self.__ReferencePoint)

    def getPlist(self, pListRef):
        se = YTSearchEngine()
        vList = json.loads(se.getPLdetails(pListRef[1]))
        vListLenght = len(vList)
        i = 1
        print (vList)
        while i<= vListLenght:
            dataRef = str(vList.get(str(i))['DataRef'])
            args = ["PL", dataRef, "-f", "mp3"]
            if self.__setGlobalEnv(args) is False:
                i = i + 1
                continue
            if self.__dwnldYTFile() is False:
                i = i + 1
                continue
            if self.__cnvrtYTFile() is False:
                i = i + 1
                continue
            i = i + 1

    def getSingle(self, args):
        if self.__setGlobalEnv(args) is False:
            quit()
        if self.__dwnldYTFile() is False:
            quit()
        if self.__cnvrtYTFile() is False:
            quit()


args = ["SL", "v2AC41dglnM", "-f", "mp3"]
ds = YTDecodeStream()
ds.getSingle(args)

#args = ["PL", qString, "-f", "mp3"]
#ds = YTDecodeStream()
#ds.getPlist(args)