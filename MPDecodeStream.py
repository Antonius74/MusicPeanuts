import pafy
import sys
import shutil
import os
import pexpect
import configparser



class YTDnld:
    fileFormat = "mp3"
    filename = ""
    YTFile = None
    YTFileInfo = None
    config = configparser.RawConfigParser()
    config.read('ConfigFile.properties')
    ffmpegExe = config.get('ffmpeg', 'ffmpeg.LocalPath')
    tempDir = config.get('Directory', 'Directory.TempDir')
    fileDir = config.get('Directory', 'Directory.FileDir')
    playURL = config.get('YTConfig', 'YTConfig.PlayURL')

    def __init__(self, args):
        if len(args) == 1:
            sys.stdout.write("Please use YTdownload URL -f format (mp3, mp4; if empty default mp3)")
            quit()

        try:
            if (len(args) > 2 and str(args[2].strip()) == "-f"):
                fileFormat = args[3].lower();
                if fileFormat == "mp4":
                    sys.stdout.write("[Info] Apply MP4 format.\n")
                    self.fileFormat = "mp4"
                elif fileFormat == "mp3":
                    sys.stdout.write("[Info] Apply MP3 format.\n")
                    self.fileFormat = "mp3"
                elif fileFormat == "avi":
                    sys.stdout.write("[Info] Apply AVI format.\n")
                    self.fileFormat = "avi"
                else:
                    sys.stdout.write("[Warning] Format not found -> apply default MP3 format.\n")
            else:
                sys.stdout.write("[Info] Format not found -> apply default MP3 format.\n")
        except Exception as e:
            sys.stdout.write("[Warning] Format not found -> apply default MP3 format.\n")

        try:
            if args[1].lower().startswith("^http"):
                self.YTFile = pafy.new(args[1])
            else:
                self.YTFile = pafy.new(self.playURL + args[1])
        except Exception as e:
            sys.stderr.write("[Error] URL Not found, please retry." + e)
            quit()

    def dwnldYTFile(self):
        if self.fileFormat is "mp3":
            self.YTFileInfo = self.YTFile.getbestaudio()
        else:
            self.YTFileInfo = self.YTFile.getbest()
        self.filename = str(os.getpid())
        print (self.filename)
        self.YTFileInfo.download(quiet=True, callback=self.stdoutDownload,
                                                 filepath=self.tempDir + self.filename)

    def cnvrtYTFile(self):
        if self.fileFormat is "mp3":
            cmdMP3 = self.ffmpegExe + "ffmpeg -hide_banner -y -i \"" + self.tempDir + self.filename + "\" -codec:a libmp3lame -qscale:a 1 \"" + self.fileDir + self.filename + ".mp3\""
            self.execConversion(cmdMP3)
            self.renameFile(self.fileDir + self.filename + ".mp3", self.fileDir + self.YTFileInfo.title + ".mp3")
        elif self.fileFormat is "avi":
            cmdAVI = self.ffmpegExe + "ffmpeg -hide_banner -y -async 1 -i \"" + self.tempDir + self.filename + "\" -f avi -b 700k -qscale 0 -ab 160k -ar 44100 \"" + self.fileDir + self.filename + ".avi\""
            self.execConversion(cmdAVI)
            self.renameFile(self.fileDir + self.filename + ".avi", self.fileDir + self.YTFileInfo.title + ".avi")
        elif self.fileFormat is "mp4":
            if self.YTFileInfo.extension == "webm":
                cmdMP4 = self.ffmpegExe + "ffmpeg  -hide_banner -y -async 1 -i \"" + self.tempDir + self.filename + "\" -f mp4 -vcodec libx264 -preset fast -profile:v main -acodec aac \"" + self.fileDir + self.filename + ".mp4\""
                self.execConversion(cmdMP4)
                self.renameFile(self.fileDir + self.filename + ".mp4", self.fileDir + self.YTFileInfo.title + ".mp4")
            elif self.YTFileInfo.extension == "mp4":
                shutil.move(self.tempDir + self.filename, self.fileDir + self.YTFileInfo.title)
            None

    def execConversion(self, cmd):
        print ("\n"+cmd)
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
                    self.stdoutConvert(str(frame_number))
                    thread.close
                elif i == 2:
                    pass
        except ValueError:
            sys.stderr.write (ValueError)

    def stdoutDownload(self, total, recvd, ratio, rate, eta):
        percent = (recvd / total) * 100
        # time.sleep()
        sys.stdout.write("\r[Downloading file from YT] -> %d%%" % round(percent))
        sys.stdout.flush()

    def stdoutConvert(self, frame_number):
        try:
            sys.stdout.write("\r[Converting file to " + self.fileFormat.upper() + "] -> " + frame_number[
                                                                                            frame_number.index(
                                                                                                "size=") + 5:frame_number.index(
                                                                                                "size=") + 15].strip())
            sys.stdout.flush()
        except Exception as e:
            None

    def destryDwnldFile(self):
        os.remove(self.tempDir + self.filename)

    def renameFile(self, pid, filename):
        os.renames(pid, filename)
        dwnld.destryDwnldFile()

dwnld = YTDnld(sys.argv)
dwnld.dwnldYTFile()
dwnld.cnvrtYTFile()