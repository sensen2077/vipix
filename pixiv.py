import requests
import re
import os
import tkinter as tk
from tkinter import ttk, messagebox


def download_image(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"{filename} downloaded successfully.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e.response.status_code} {e.response.reason}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"General error: {e}")


def start_download():
    target = target_entry.get()
    pages = int(pages_entry.get())
    save_folder = save_folder_entry.get()

    if not target or not pages or not save_folder:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    url2 = rf'https://www.vilipix.com/tags/{target}/illusts?p='
    ibk = re.compile(
        r'</div> <a href="/user/undefined" target="_blank" class="user-name" data-v-ece93980></a></div></li><li class="pix-card" style="width:184px;" data-v-ece93980><div class="illust" style="width:184px;height:184px;" data-v-ece93980><a href="(?P<rl>.*?)" target="_blank"',
        re.S)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    payload = {
        "limit": "16",
        "offset": "0",
        "type": "0",
    }
    pay = {
        "limit": "8",
        "offset": "0",
        "picture_id": "116850700",
        "user_id": "9906436",
    }

    if not os.path.exists(rf"D:\picture"):
        os.mkdir(r"D:\picture")
    if not os.path.exists(rf"D:\picture\{save_folder}"):
        os.mkdir(rf"D:\picture\{save_folder}")
        print(rf"D:\picture\{save_folder} directory created")
    else:
        print("Directory already exists")

    b = 1
    for a in range(1, pages + 1):
        url1 = url2 + str(a)
        u = r"https://www.vilipix.com/"
        resp = requests.get(url1, headers=headers, params=payload)
        lueluelue = ibk.finditer(resp.text)
        for j in lueluelue:
            url3 = u + j.group("rl")
            print(url3)
            res = requests.get(url3, headers=headers, params=pay)
            obj = re.compile(r'<a href="javascript: void.*?"><img src="(?P<ur>.*?)" alt=".*?">', re.S)
            urls_names = obj.finditer(res.text)
            for i in urls_names:
                image_url = i.group("ur")
                savepath = rf"D:\picture\{save_folder}\draw" + str(b) + ".webp"
                download_image(image_url, savepath)
                b += 1
            res.close()
        print(f"Page {a}:{url1} done!")
        resp.close()

    messagebox.showinfo("Download Complete", "All images have been downloaded successfully.")


# Create GUI
root = tk.Tk()
root.title("Vilipix Image Downloader")

# Target label and entry
target_label = ttk.Label(root, text="Target Tag:")
target_label.grid(column=0, row=0, padx=10, pady=10)
target_entry = ttk.Entry(root, width=30)
target_entry.grid(column=1, row=0, padx=10, pady=10)

# Pages label and entry
pages_label = ttk.Label(root, text="Number of Pages:")
pages_label.grid(column=0, row=1, padx=10, pady=10)
pages_entry = ttk.Entry(root, width=30)
pages_entry.grid(column=1, row=1, padx=10, pady=10)

# Save folder label and entry
save_folder_label = ttk.Label(root, text="Save Folder Name:")
save_folder_label.grid(column=0, row=2, padx=10, pady=10)
save_folder_entry = ttk.Entry(root, width=30)
save_folder_entry.grid(column=1, row=2, padx=10, pady=10)

# Start button
start_button = ttk.Button(root, text="Start Download", command=start_download)
start_button.grid(column=0, row=3, columnspan=2, padx=10, pady=20)

root.mainloop()
