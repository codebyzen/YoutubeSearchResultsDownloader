#!/usr/bin/env python3

import os
import subprocess
import json
import re
from pprint import pprint
from multiprocessing.dummy import Pool as ThreadPool

def slugify(value):
	"""
	Normalizes string, converts to lowercase, removes non-alpha characters,
	and converts spaces to hyphens.
	"""
	import unicodedata
	value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
	value = str(value)
	value = re.sub('[^\w\s-]', '', value).strip().lower()
	value = re.sub('[-\s]+', '-', value)
	return value

def get_video_info(url):

	yt_bin = './bin/youtube-dl -j '+url
	yt_args = ''
	proc = subprocess.Popen([yt_bin, yt_args], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()

	# with open("data_file.json", "w") as write_file:
	# 	json.dump(out, write_file)

	# with open("data_file.json", encoding="utf-8") as json_file:
	# 	out = json.load(json_file)
	# print(out)
	try:
		data = json.loads(out)
	except ValueError as identifier:
		print("!!!: "+url)
		# pprint(identifier)
	
	path = data['upload_date'][0:4]
	filename = slugify(data['fulltitle'])

	ret = {
		"title": data['fulltitle'],
		"path": path,
		"filename": filename,
		"date": data['upload_date'],
		"description": data['description']+"\n\n"+", ".join(data['tags'])
	}

	return ret

def download(url):
	
	video_data = get_video_info(url)

	if not os.path.exists(video_data['path']):
		os.mkdir(video_data['path'])

	if os.path.exists(video_data['path']+"/"+video_data['filename']+".mp4") and os.path.exists(video_data['path']+"/"+video_data['filename']+".txt"):
		print("Duplicate: "+url)
		return False
	# while os.path.exists(video_data['path']+"/"+video_data['filename']+".txt"):
	# 	matches = re.search("_([\d]+)", video_data['filename'][-2:])
	# 	if matches != None:
	# 		video_data['filename'] = video_data['filename'][0:-2]+"_"+str(int(matches[1])+1)
	# 	else:
	# 		video_data['filename'] = video_data['filename']+"_1"

	descriptionfile = open(video_data['path']+"/"+video_data['filename']+".txt","w") 
	descriptionfile.write(video_data['date']+"\n\n"+video_data['title']+"\n\n"+video_data['description'])
	descriptionfile.close()

	# command = "./bin/youtube-dl -f 'bestvideo[height<=1280][ext=mp4]/best[ext=mp4]' -o \""+video_data['path']+"/"+video_data['filename']+".%(ext)s\" --external-downloader ./bin/aria2c --external-downloader-args '-x 8' "+url
	command = "./bin/youtube-dl -f 'best' -o \""+video_data['path']+"/"+video_data['filename']+".%(ext)s\" --external-downloader ./bin/aria2c --external-downloader-args '-x 8' "+url
	print(command)
	proc = subprocess.Popen([command, ""], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	return out


with open("list.txt", encoding="utf-8") as list_file:
	urlslist = list_file.read().split("\n")

pool = ThreadPool(12)
results = pool.map(download, urlslist)

for i in results:
	print(i)