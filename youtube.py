#youtube analytics finder for linux made by t0a5ted 2020


from apiclient.discovery import build
import colorama
from colorama import Fore, Style
import os
import pyfiglet

api_key = "PASTE YOUR API KEY HERE"

youtube = build('youtube', 'v3', developerKey=api_key)



def searchornah():
	try:
		result = pyfiglet.figlet_format("Youtube Stats", font = "slant" ) 
		print(Fore.RED + result + "--------------------------------------------------------------------\nMade By t0a5ted\n\n" + Style.RESET_ALL) 
		print("Choose One Of The Below Methods: \n1. Search For Channel\n2. Manually Enter Channel ID\n")
		x = input("Enter 1 or 2: ")
		if x == '1':
			search_user()
		elif x == '2':
			enter_user()
		else:
			clear_screen()
			print("ENTER 1 OR 2... IT'S NOT THAT HARD!\n\n")
			searchornah()
	except KeyboardInterrupt:
		clear_screen()
		exit()

#---------------------------------------------------------------------
def search_user():
	try:
		global chosen_channel_id
		clear_screen()
		query = input('Enter Channel Name To Search: ')
		print(Fore.BLUE + "\nSearching Youtube... This May Take A While...")

		req = youtube.search().list(q=query, part='snippet', type='channel', maxResults=8) #cap queries at 8 so less waiting time
		res = req.execute()

		#print output for reference        remove once project is completed
		#print(res)
		#print("----------------------------------------------------------------")

		channelIDs = []
		x = 1

		for item in res['items']:
			print(x, '. ' + item['snippet']['channelTitle'])
			print(item['snippet']['description'])
			print("\n")
			x = x+1
			channelIDs.append(item['snippet']['channelId'])

		while True:
			chooseChannel = input(Fore.GREEN + 'Which Channel Do You Want To Search (Enter the number 1-8): ')
			print(Style.RESET_ALL)
			if int(chooseChannel) > 0 and int(chooseChannel) < 9 and float(chooseChannel).is_integer() == True:
				#print(channelIDs[int(chooseChannel)-1])
				chosen_channel_id = channelIDs[int(chooseChannel)-1]
				break
			else:
				print(Fore.RED + "\nPlease Select A Valid Number!!")
				print(Style.RESET_ALL)

		clear_screen()
		stats_menu()

		#print(channelIDs)
	except KeyboardInterrupt:
		clear_screen()
		exit()

#---------------------------------------------------------
def clear_screen():
	os.system('clear')
#--------------------------------------------------------

def enter_user():
	global chosen_channel_id
	clear_screen()
	chosen_channel_id =  input("Enter Channel ID: ")
	stats_menu()

#---------------------------------------------------------

def stats_menu():
	clear_screen()

	request = youtube.channels().list(
	part="snippet,contentDetails,statistics",
	id=chosen_channel_id
	)
	response = request.execute()

	#print(response)
	#print("-------------------------------------------------------------------------------------------")


	print(Fore.BLUE + "Channel Name: " + response['items'][0]['snippet']['title'] + Style.RESET_ALL)
	print(Fore.GREEN + "Channel Description: " + response['items'][0]['snippet']['description'] + Style.RESET_ALL)
	try:
		print(Fore.RED + "Country: " + response['items'][0]['snippet']['country'] + Style.RESET_ALL)
	except KeyError:
		print(Fore.RED + "Country: NOT AVAILABLE" + Style.RESET_ALL)
	print(Fore.WHITE + "Videos: " + response['items'][0]['statistics']['videoCount'] + Style.RESET_ALL)
	if response['items'][0]['statistics']['hiddenSubscriberCount'] == True:
		print(Fore.BLUE + "Subscribers: HIDDEN (user has disabled public subscriber count)" + Style.RESET_ALL)
	elif response['items'][0]['statistics']['hiddenSubscriberCount'] == False:
		print(Fore.BLUE + "Subscribers: " + response['items'][0]['statistics']['subscriberCount'] + Style.RESET_ALL)
	print(Fore.GREEN + "Views: " + response['items'][0]['statistics']['viewCount'] + Style.RESET_ALL)

	global highest_views_video
	global highest_views_id
	global highest_views
	global videos
	global ids
	
	videos = []
	ids = []
	next_page_token = None
	upload_playlist = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
	
	while 1:
		res = youtube.playlistItems().list(playlistId=upload_playlist, part='snippet', maxResults=50, pageToken=next_page_token).execute()
		videos += res['items']


		for video in videos:
			ids.append(video['snippet']['resourceId']['videoId'])

		next_page_token = res.get('nextPageToken')
		

		if next_page_token is None:
			break

	highest_views = 0
	highest_views_id = ""

	for videoID in ids:
		request2 = youtube.videos().list(
		part="statistics, snippet",
		id=videoID
		)
		response2 = request2.execute()
		video_views = int(response2['items'][0]['statistics']['viewCount'])
		if int(video_views) > int(highest_views):
			highest_views = int(video_views) #other values are likeCount, dislikeCount, commentCount
			highest_views_id = videoID
		elif int(video_views) < int(highest_views):
			pass

	request3 = youtube.videos().list(
	part="statistics, snippet",
	id=highest_views_id
	)
	response3 = request3.execute()
	#print(response3)
	highest_views_video = str(response3['items'][0]['snippet']['title'])
	print("\n\n")
	print(Fore.RED + "Most Viewed Video: " + highest_views_video + Style.RESET_ALL)
	print(Fore.WHITE + "Views On Highest Viewed Video: ", highest_views, Style.RESET_ALL)


	highest_likes = 0

	for videoID in ids:
		request5 = youtube.videos().list(
		part="statistics, snippet",
		id=videoID
		)
		response5 = request5.execute()
		video_likes = int(response5['items'][0]['statistics']['likeCount'])
		if int(video_likes) > int(highest_likes):
			highest_likes = int(video_likes) #other values are likeCount, dislikeCount, commentCount
			highest_likes_id = videoID
		elif int(video_likes) < int(highest_likes):
			pass

	request6 = youtube.videos().list(
	part="statistics, snippet",
	id=highest_likes_id
	)
	response6 = request6.execute()
	highest_likes_video = str(response6['items'][0]['snippet']['title'])

	print("\n\n")
	print(Fore.RED + "Most Liked Video: " + highest_likes_video + Style.RESET_ALL)
	print(Fore.WHITE + "Likes On Most Liked Video: ", highest_likes, Style.RESET_ALL)
	print("\n\n")





clear_screen()
searchornah()
