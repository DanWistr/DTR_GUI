import customtkinter as ctk
from PIL import Image
import pywinstyles

# Initialize the main application window
root = ctk.CTk()
root.title("DTR Face Recognition")
root.attributes("-fullscreen", True)
#root.state("zoomed")

# Get dimensions after initialization
root.update()
window_width = root.winfo_width()
window_height = root.winfo_height()

# Configure grid layout of root
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=0)
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=3)
root.grid_rowconfigure(2, weight=0)

# Load and apply background image
bg_image = ctk.CTkImage(Image.open("images/ui bg.png"), size=(window_width, window_height))
bg_label = ctk.CTkLabel(root, image=bg_image, text="")
bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

#Empty space for layout
empty_space = ctk.CTkLabel(root, text="", height=int(window_height*0.08))
empty_space.grid(row=0, column=0, columnspan=3, sticky="nsew")
pywinstyles.set_opacity(empty_space, 0.0)

# LIVE FEED Frame (left side)
live_feed_frame = ctk.CTkFrame(root)
live_feed_frame.grid(row=1, column=0, padx=(15,0), pady=5, sticky="nsew")
live_label = ctk.CTkLabel(live_feed_frame, text="LIVE FEED", font=("Arial", 22, "bold"), text_color="black")
live_label.place(relx=0.5, rely=0.5, anchor="center")

# TABLE Frame (right side)
table_frame = ctk.CTkFrame(root)
table_frame.grid(row=1, column=1, padx=(10,15), pady=5, sticky="nsew")
table_label = ctk.CTkLabel(table_frame, text="TABLE", font=("Arial", 22, "bold"), text_color="black")
table_label.place(relx=0.5, rely=0.5, anchor="center")

# CONTROL BUTTONS: place them *inside* the table_frame, anchored NE
btn_container = ctk.CTkFrame(root, fg_color="transparent" ,bg_color="#17759b")
btn_container.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

start_button = ctk.CTkButton(btn_container, text="", width=50, height=50, fg_color = "#176448", bg_color="#17759b", hover_color="#083a28")
start_button.pack(side="left", padx=(0, 8))

stop_button = ctk.CTkButton(btn_container, text="", width=50, height=50,fg_color="grey", bg_color="#17759b", hover_color="#4a4d4e")
stop_button.pack(side="left")

# INFO (bottom) Frame
info_frame = ctk.CTkFrame(root, fg_color="#002B28")
info_frame.grid(row=2, column=0, columnspan=2, padx=15, pady=(5, 15), sticky="nsew")
info_frame.grid_columnconfigure(0, weight=0)
info_frame.grid_columnconfigure(1, weight=40)
info_frame.grid_rowconfigure(0, weight=1)
info_frame.grid_rowconfigure(1, weight=1)
info_frame.grid_rowconfigure(2, weight=1)
info_frame.grid_rowconfigure(3, weight=1)

photo_placeholder = ctk.CTkLabel(info_frame, text="", width=300, height=300, fg_color="white", corner_radius=5)
photo_placeholder.grid(row=0, column=0, padx=10, pady=10, sticky = "w", rowspan=4)

# TIME IN (largest)
time_in_label = ctk.CTkLabel(info_frame, text="TIME IN:", text_color="white", font=("Arial", 72, "bold"), anchor="w")
time_in_label.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 0))

small_font = ("Arial", 38, "bold")

name_label = ctk.CTkLabel( info_frame, text="NAME:", text_color="white", font=small_font, anchor="w")
name_label.grid(row=1, column=1, sticky="w", padx=10, pady=0)

emp_label = ctk.CTkLabel( info_frame, text="EMP#:", text_color="white", font=small_font, anchor="w")
emp_label.grid(row=2, column=1, sticky="w", padx=10, pady=0)

dept_label = ctk.CTkLabel(info_frame, text="DEPT:", text_color="white", font=small_font, anchor="w")
dept_label.grid(row=3, column=1, sticky="w", padx=10, pady=(0, 10))


root.mainloop()
