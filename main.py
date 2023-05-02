import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image
import os
from pytube import YouTube
from functools import partial
import urllib
import io
import asyncio


# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    WIDTH = 1100
    HEIGHT = 580

    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        # configure window
        self.title("Youtube Downloader")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)

        self.label_url = customtkinter.CTkLabel(
            master=self,
            text='Youtube URL',
            anchor='w',
            font=('Sans Serif', -15)
        )

        self.entry_url = customtkinter.CTkEntry(
            master=self,
            width=500,
            placeholder_text='https://www.youtube.com/'
        )

        self.image = customtkinter.CTkImage(
            light_image=Image.open('2.jpg'),
            size=(500, 400)
        )

        self.frame_image = customtkinter.CTkLabel(
            master=self,
            image=self.image,
            text=''
        )
        self.download_button = customtkinter.CTkButton(
            master=self,
            width=500,
            text='Download',
            command=self.download_music
        )

        self.label_url.pack()
        self.entry_url.pack()
        self.frame_image.pack()
        self.download_button.pack()

    async def execute_async_download(self):
        await self.loop.run_in_executor(None, self.download_music)
        
    def download_music(self):
        url = self.entry_url.get()
        root = 'Download_Youtube'
        if url:
            try:
                yt = YouTube(url)
                self.get_image(yt.thumbnail_url)
                video = yt.streams.get_audio_only()
                out_file = video.download(output_path=root)
                base, ext = os.path.splitext(out_file)
                new_file = f'{base}.mp3'
                os.rename(out_file, new_file)
            except FileExistsError as e:
                tkinter.messagebox.showerror(
                    title='File Exists',
                    message=e
                )
                os.remove(os.path.join(root, base + ext))

    def get_image(self, url):
        response = urllib.request.urlopen(url)
        io_image = io.BytesIO(response.read())
        image = Image.open(io_image)
        self.image.configure(
            light_image=image)


if __name__ == "__main__":
    app = App()
    app.mainloop()
