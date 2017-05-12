import pafy
import sys 
import time
import subprocess
import os
import pexpect

class YTDnld:

	fileFormat = "mp3"
	filename = ""
	YTFile = None
	YTFileInfo = None

	def __init__(self, args): 
		if len(args) == 1:
			sys.stdout.write ("Please use YTdownload URL -f format (mp3, mp4; if empty default mp3)")
			quit()
		
		try:
			if (len(args)>2 and str(args[2].strip()) == "-f"):
				fileFormat = args[3].lower();
				if fileFormat == "mp4":
					sys.stdout.write("[Info] Apply MP4 format.\n")
					self.fileFormat = "mp4"
				elif fileFormat == "mp3":
					sys.stdout.write("[Info] Apply MP3 format.\n")
					self.fileFormat = "mp3"
				else:
					sys.stdout.write("[Warning] Format not found -> apply default MP3 format.\n")
			else:
				sys.stdout.write("[Info] Format not found -> apply default MP3 format.\n")
				print (self.fileFormat)
		except Exception as e:
			sys.stdout.write("[Warning] Format not found -> apply default MP3 format.\n")

		try:
			self.YTFile = pafy.new(args[1])
		except Exception as e:
			sys.stderr.write("[Error] URL Not found, please retry.")
			quit()

			
	def dwnldYTFile(self):
		if self.fileFormat is "mp3":
			self.YTFileInfo = self.YTFile.getbestaudio()
		else:
			self.YTFileInfo = self.YTFile.getbest()
		self.filename = self.YTFileInfo.download(quiet=True, callback=self.stdoutDownload, filepath=self.YTFileInfo.title + "." + self.YTFileInfo.extension)
		print ()

	def cnvrtYTFile(self):
		if self.fileFormat is "mp3":
			cmdMP3 = "ffmpeg -hide_banner -y -i \"" + self.filename + "\" -codec:a libmp3lame -qscale:a 1 \"" + self.YTFileInfo.title + ".mp3\""
			print(cmdMP3)
			self.execConversion(cmdMP3)
		elif self.fileFormat is "avi":
			#ffmpeg -async 1 -i inputVideo.flv -f avi -b 700k -qscale 0 -ab 160k -ar 44100 outputVideo.avi
			cmdAVI = "ffmpeg -hide_banner -y -async 1 -i \"" + self.filename + "\" -f avi -b 700k -qscale 0 -ab 160k -ar 44100 \"" + self.YTFileInfo.title + ".avi\""
			self.execConversion(cmdAVI)
		elif self.fileFormat is "mp4":
			if self.YTFileInfo.extension == "webm":
				#print (self.YTFileInfo.extension)
				cmdMP4 = "ffmpeg  -hide_banner -y -async 1 -i \"" + self.filename + "\" -f mp4 -vcodec libx264 -preset fast -profile:v main -acodec aac \"" + self.YTFileInfo.title + ".mp4\""
				self.execConversion(cmdMP4)
			None

	def execConversion(self, cmd):		
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
		if self.fileFormat is "mp3" or self.fileFormat is "avi" or self.fileFormat is "mp4" or self.YTFileInfo.extension == "webm" :
			dwnld.destryDwnldFile()
			sys.stdout.write("\n")

	def stdoutDownload(self, total, recvd, ratio, rate, eta):
		percent = (recvd/total)*100
		#time.sleep()
		sys.stdout.write("\r[Downloading file from YT] -> %d%%" % round(percent))
		sys.stdout.flush()

	def stdoutConvert(self, frame_number):
		try:
			sys.stdout.write("\r[Converting file to " + self.fileFormat.upper() + "] -> " + frame_number[frame_number.index("size=")+5:frame_number.index("size=")+15].strip())
			sys.stdout.flush()
		except Exception as e:
			None


	def destryDwnldFile(self):
		os.remove(self.filename)

dwnld = YTDnld(sys.argv)
dwnld.dwnldYTFile()
dwnld.cnvrtYTFile()

