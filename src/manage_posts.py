import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import shutil
import re

POSTS_DIR = 'posts'
SECTIONS = ['main', 'thoughts', 'music']
MEDIA_DIR = 'media'
SUB_DIRS = {'audio': 'audio', 'video': 'video', 'image': 'image'}
HTML_PATH = 'index.html'

for section in SECTIONS:
    os.makedirs(os.path.join(POSTS_DIR, section), exist_ok=True)
for media_type in SUB_DIRS.values():
    os.makedirs(os.path.join(MEDIA_DIR, media_type), exist_ok=True)
    
def clean_filename(filename: str) -> str:
        return re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    
class BlogManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blog Manager")
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Post Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.root, width=50)
        self.title_entry.pack()

        self.content_label = tk.Label(self.root, text="Post Content:")
        self.content_label.pack()

        self.content_text = ScrolledText(self.root, height=20, width=70, wrap=tk.WORD, undo=True)  # Enable undo
        self.content_text.pack()

        self.section_label = tk.Label(self.root, text="Select Section:")
        self.section_label.pack()

        self.section_var = tk.StringVar(value='main')
        for section in SECTIONS:
            tk.Radiobutton(self.root, text=section.capitalize(), variable=self.section_var, value=section).pack(anchor=tk.W)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.save_button = tk.Button(self.button_frame, text="Save Post", command=self.create_post)
        self.save_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self.button_frame, text="Delete Post", command=self.delete_post)
        self.delete_button.pack(side=tk.LEFT)

        self.insert_audio_button = tk.Button(self.button_frame, text="Insert Audio", command=self.insert_audio)
        self.insert_audio_button.pack(side=tk.LEFT)

        self.insert_video_button = tk.Button(self.button_frame, text="Insert Video", command=self.insert_video)
        self.insert_video_button.pack(side=tk.LEFT)

        self.insert_image_button = tk.Button(self.button_frame, text="Insert Image", command=self.insert_image)
        self.insert_image_button.pack(side=tk.LEFT)

        self.root.bind('<Control-b>', self.make_bold)
        self.root.bind('<Control-i>', self.make_italic)
        self.root.bind('<Control-u>', self.make_underline)
        self.root.bind('<Control-s>', self.make_selected)
        self.root.bind('<Control-z>', self.handle_undo)  # Custom undo handler
    

    def create_post(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        section = self.section_var.get()

        if not title or not content:
            messagebox.showerror("Error", "Title and content cannot be empty")
            return

        section_dir = os.path.join(POSTS_DIR, section)
        post_count = len(os.listdir(section_dir)) + 1  
        timestamp = datetime.now().strftime('%d-%m-%Y %H:%M')
        clean_date = datetime.now().strftime('%Y_%m_%d.%H-%M')  

        filename = f"{post_count}_{clean_filename(title).replace(' ', '_')}_{clean_date}.txt"
        filepath = os.path.join(section_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{title}\n")
            f.write(f"{timestamp}\n")
            f.write(f"{content}\n")

        self.update_html()

        messagebox.showinfo("Success", f"Post '{title}' saved.")
        self.clear_form()

    def delete_post(self):
        section = self.section_var.get()
        posts = self.list_posts(section)

        if not posts:
            messagebox.showerror("Error", "No posts found in this section.")
            return

        post_titles = [f"{i + 1}. {post['title']}" for i, post in enumerate(posts)]
        post_to_delete = simpledialog.askstring("Delete Post", f"Choose the index of a post to delete:\n" + "\n".join(post_titles))

        if post_to_delete:
            try:
                post_index = int(post_to_delete) - 1
                post = posts[post_index]
                os.remove(os.path.join(POSTS_DIR, section, post['file']))
                messagebox.showinfo("Success", f"Post '{post['title']}' deleted.")
                self.update_html()
                self.clear_form()
            except (IndexError, ValueError):
                messagebox.showerror("Error", "Invalid post selection.")
        else:
            messagebox.showinfo("Cancelled", "Deletion cancelled.")

    def insert_audio(self):
        self.insert_media("audio", "*.mp3 *.wav", "audio-player")

    def insert_video(self):
        self.insert_media("video", "*.mp4 *.webm *.ogg")

    def insert_image(self):
        self.insert_media("image", "*.png *.jpg *.jpeg *.gif")

    def insert_media(self, media_type, filetypes, css_class=None):
        file_path = filedialog.askopenfilename(title=f"Select {media_type.capitalize()}", filetypes=[(f"{media_type.capitalize()} Files", filetypes)])
        if file_path:
            try:
                media_dest = os.path.join(MEDIA_DIR, SUB_DIRS[media_type], os.path.basename(file_path))
                shutil.copy(file_path, media_dest)  
                media_tag = ''
                if media_type == "audio":
                    media_tag = f'<audio class="{css_class}" controls><source src="{media_dest}" type="audio/mpeg">Your browser does not support the audio element.</audio>'
                elif media_type == "video":
                    media_tag = f'<video controls><source src="{media_dest}" type="video/mp4">Your browser does not support the video element.</video>'
                elif media_type == "image":
                    media_tag = f'<img src="{media_dest}" alt="Image">'
                self.content_text.insert(tk.INSERT, f"\n{media_tag}\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to insert {media_type}: {str(e)}")

    def make_bold(self, event=None):
        self.content_text.insert(tk.INSERT, "<b></b>")

    def make_italic(self, event=None):
        self.content_text.insert(tk.INSERT, "<i></i>")

    def make_underline(self, event=None):
        self.content_text.insert(tk.INSERT, "<u></u>")

    def make_selected(self, event=None):
        self.content_text.insert(tk.INSERT, "<span class=\"selected\"></span>")

    def handle_undo(self, event=None):
        try:
            self.content_text.edit_undo()
        except tk.TclError:
            pass

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)

    def list_posts(self, section):
        section_dir = os.path.join(POSTS_DIR, section)
        post_files = sorted(os.listdir(section_dir))  
        posts = []
        for post_file in post_files:
            with open(os.path.join(section_dir, post_file), 'r', encoding='utf-8') as f:
                title = f.readline().strip()
                date = f.readline().strip()
                posts.append({'title': title, 'file': post_file, 'date': date})
        return posts

    def update_html(self):
        if not os.path.exists(HTML_PATH):
            messagebox.showerror("Error", f"{HTML_PATH} does not exist.")
            return

        with open(HTML_PATH, 'r', encoding='utf-8') as html_file:
            content = html_file.read()

        posts_by_section = {section: [] for section in SECTIONS}

        for section in SECTIONS:
            section_dir = os.path.join(POSTS_DIR, section)
            post_files = sorted(os.listdir(section_dir))  
            for post_file in post_files:
                with open(os.path.join(section_dir, post_file), 'r', encoding='utf-8') as f:
                    title = f.readline().strip()
                    date = f.readline().strip()
                    post_content = f.read().strip()
                    posts_by_section[section].append({'title': title, 'date': date, 'content': post_content})

        content = self.update_section(content, 'main', posts_by_section['main'], 'end-main')
        content = self.update_section(content, 'thoughts', posts_by_section['thoughts'], 'end-thoughts')
        content = self.update_section(content, 'music', posts_by_section['music'], 'end-music')

        with open(HTML_PATH, 'w', encoding='utf-8') as html_file:
            html_file.write(content)

        messagebox.showinfo("Success", "index.html has been updated with the latest posts.")

    def update_section(self, content, section_name, posts, end_section_marker):
        start_marker = f'<!--{section_name}-->'
        start_index = content.find(start_marker)
        if start_index == -1:
            messagebox.showerror("Error", f"Marker for {section_name} not found.")
            return content

        posts_html = ""
        
        total_posts = len(posts)

        for idx, post in enumerate(reversed(posts), 1): 
            posts_html += f"""
            <article class="blog-entry" style="position: relative;">
                <span class="npost selected">#{total_posts - idx + 1}</span>
                <h3>{post['title']}</h3>
                <p class="fecha">{post['date']} <small class="timezone">(UTC-03:00)</small></p>
                <p>{post['content']}</p>
            </article>
            """

        start_index += len(start_marker)
        end_index = content.find(f'<!--{end_section_marker}-->', start_index)
        if end_index == -1:
            end_index = len(content)

        updated_content = content[:start_index] + posts_html + content[end_index:]
        return updated_content

def main():
    root = tk.Tk()
    app = BlogManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()