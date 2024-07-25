#Mini-Project Program By Chandrakant Shelke(196028_CO)
#We import the modules & library which we are needed
import os
import tkinter as tk #creating the graphical user interface.
import pickle #serializing and deserializing Python objects.
from tkinter import filedialog #open a file dialog to choose directories.
from pygame import mixer #handling audio playback.
from tkinter import PhotoImage #handle images.


class Player(tk.Frame): # inherits from tk.Frame

	#The __init__ method initializes the player:
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		mixer.init()

		#Checks if a file songs.pickle exists:
		#If it exists, it loads the playlist from the file.
		#If not, it initializes an empty playlist.
		if os.path.exists('songs.pickle'):  
			with open('songs.pickle', 'rb') as f:
				self.playlist = pickle.load(f)
		else:
			self.playlist=[]

		self.current = 0 #keep track of the currently playing song index.
		self.paused = True #check if the song is paused.
		self.played = False #check if a song has been played.

		#Calls methods to create the GUI components.
		self.create_frames()
		self.track_widgets()
		self.control_widgets()
		self.tracklist_widgets()
		
	#Creating of 3 frames in a window
	def create_frames(self):
		#Creating first frame of Song Track
		self.track = tk.LabelFrame(self, text='Song Track',
					font=("times new roman",15,"bold"),
					bg="black",fg="white",bd=5,relief=tk.GROOVE)
		self.track.config(width=410,height=300)
		self.track.grid(row=0, column=0, padx=10)

                #Creating Second frame for Tracklist or Playlist
		self.tracklist = tk.LabelFrame(self, text=f'PlayList - {str(len(self.playlist))}',
							font=("times new roman",15,"bold"),
							bg="black",fg="white",bd=5,relief=tk.GROOVE)
		self.tracklist.config(width=190,height=400)
		self.tracklist.grid(row=0, column=1, rowspan=3, pady=5)

        #Creating Third Frame for Controls
		self.controls = tk.LabelFrame(self,
							font=("times new roman",15,"bold"),
							bg="white",fg="white",bd=2,relief=tk.GROOVE)
		self.controls.config(width=410,height=80)
		self.controls.grid(row=2, column=0, pady=5, padx=10)


	def track_widgets(self):
		self.canvas = tk.Label(self.track, image=img)
		self.canvas.configure(width=400, height=240)
		self.canvas.grid(row=0, column=0)

		self.songtrack = tk.Label(self.track, font=("times new roman",16,"bold"),
						bg="white",fg="dark blue")
		self.songtrack['text'] = '!....MUSICXY MP3 PLAYER....!'
		self.songtrack.config(width=30, height=1)
		self.songtrack.grid(row=1,column=0,padx=10)

	def control_widgets(self):
		self.loadSongs = tk.Button(self.controls, bg='green', fg='white', font=10)
		self.loadSongs['text'] = 'Load Songs'
		self.loadSongs['command'] = self.retrieve_songs
		self.loadSongs.grid(row=0, column=0, padx=10)

        #Function for change the Songs as Previous
		self.prev = tk.Button(self.controls, image=prev)
		self.prev['command'] = self.prev_song
		self.prev.grid(row=0, column=1)

        #Function for Pause the Songs
		self.pause = tk.Button(self.controls, image=pause)
		self.pause['command'] = self.pause_song
		self.pause.grid(row=0, column=2)

        #Function for change the Songs as next
		self.next = tk.Button(self.controls, image=next_)
		self.next['command'] = self.next_song
		self.next.grid(row=0, column=3)

        #Function for change the Volume
		self.volume = tk.DoubleVar(self)
		self.slider = tk.Scale(self.controls, from_ = 0, to = 10, orient = tk.HORIZONTAL)
		self.slider['variable'] = self.volume
		self.slider.set(8)
		mixer.music.set_volume(0.8)
		self.slider['command'] = self.change_volume
		self.slider.grid(row=0, column=4, padx=5)

	#Creating Tracklist Widgets
	def tracklist_widgets(self):
		#This method creates widgets for the tracklist frame.
		self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
		self.scrollbar.grid(row=0,column=1, rowspan=5, sticky='ns')

		#Creates a vertical scrollbar.
		self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE,
					 yscrollcommand=self.scrollbar.set, selectbackground='sky blue')

		self.enumerate_songs()
		self.list.config(height=22)
		self.list.bind('<Double-1>', self.play_song)
		self.scrollbar.config(command=self.list.yview)
		self.list.grid(row=0, column=0, rowspan=5)

	#Creates a listbox to display the playlist and binds it to a 
	#double-click event to play the selected song.
	def retrieve_songs(self):
		#This method retrieves songs from a directory.
		self.songlist = []
		directory = filedialog.askdirectory()
		for root_, dirs, files in os.walk(directory):
				for file in files:
					if os.path.splitext(file)[1] == '.mp3':
						path = (root_ + '/' + file).replace('\\','/')
						self.songlist.append(path)
		#Opens a directory dialog to select a directory and 
		#adds all .mp3 files to self.songlist.
		with open('songs.pickle', 'wb') as f:
			pickle.dump(self.songlist, f)
		self.playlist = self.songlist
		self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
		self.list.delete(0, tk.END)
		self.enumerate_songs()
		
	#Saves the song list to songs.pickle and updates the playlist and listbox.
	def enumerate_songs(self):
		#This method adds songs to the listbox.
		for index, song in enumerate(self.playlist):
			self.list.insert(index, os.path.basename(song))

	#Inserts each song into the listbox.
	def play_song(self, event=None):
		#This method plays a selected song.
		if event is not None:
			self.current = self.list.curselection()[0]
			for i in range(len(self.playlist)):
				self.list.itemconfigure(i, bg="white")
		#If triggered by an event, sets the current song to the selected one 
		#and resets the listbox item colors.
		print(self.playlist[self.current])
		mixer.music.load(self.playlist[self.current])
		self.songtrack['anchor'] = 'w'
		self.songtrack['text'] = os.path.basename(self.playlist[self.current])
		
		#Loads and displays the current song.
		self.pause['image'] = play
		self.paused = False
		self.played = True
		self.list.activate(self.current)
		self.list.itemconfigure(self.current, bg='sky blue')

		mixer.music.play()
         #Updates the button image and states, highlights the current song, and starts playing it.
	def pause_song(self):
		#This method pauses or unpauses the song.
		if not self.paused:
			self.paused = True
			mixer.music.pause()
			self.pause['image'] = pause
		else:
			if self.played == False:
				self.play_song()
			self.paused = False
			mixer.music.unpause()
			self.pause['image'] = play

	def prev_song(self):
		if self.current > 0:
			self.current -= 1
		else:
			self.current = 0
		self.list.itemconfigure(self.current + 1, bg='white')
		self.play_song()

	def next_song(self):
		if self.current < len(self.playlist) - 1:
			self.current += 1
		else:
			self.current = 0
		self.list.itemconfigure(self.current - 1, bg='white')
		self.play_song()

	def change_volume(self, event=None):
		self.v = self.volume.get()
		mixer.music.set_volume(self.v / 10)

# ----------------------------- Main -------------------------------------------
#Create a Tkinter Window
root = tk.Tk()
root.geometry('600x400') #Configure the Tkinter window size
root.wm_title('MUSICXY MP3 PLAYER') #Title of the window

#Making images as a PhotoImage
img =PhotoImage(file='images/img.gif')
next_=PhotoImage(file='images/next.gif')
prev=PhotoImage(file='images/previous.gif')
play=PhotoImage(file='images/play.gif')
pause=PhotoImage(file='images/pause.gif')

app = Player(master=root)
app.mainloop()
root.mainloop()
