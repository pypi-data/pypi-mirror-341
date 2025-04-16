import tkinter as tk 
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
import random
import pandas as pd
from portrait_robot_final import *
from torchvision import transforms
from PIL import Image
import torch
from torchvision.utils import make_grid
from torchvision.transforms.functional import to_pil_image
from portrait_robot_final import attribute_directions, compute_attribute_directions_from_csv
import tkinter.filedialog

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

attr_path = os.path.join(BASE_DIR, "list_attr_celeba.csv")
photos_directory = os.path.join(BASE_DIR, "celeba_5000_sample")
img_path = photos_directory

# GLOBAL VARIABLES
selected_images = [] #global variable for the selected images by the user
selected_attributes = [] #global variable for the selected extra attributes by the user

def on_enter(button):
    """Changes the color of button when mouse hovers over"""

    button.config(bg="#402408", fg="white")

def on_leave(button):
    """Button changes color when the mouse leaves"""

    button.config(bg="#ecd7c6", fg="black")

def random_images(directory, images_list):
    """Chooses 10 random images from a directory containing photos and stores them in a list,
    the names of the photos are also stored in a list """

    images_to_show = []
    images_names = []
    while len(images_to_show) < 10:
        image = os.path.join(directory, random.choice(images_list))
        if image not in images_to_show:
            images_to_show.append(image)
            images_names.append(os.path.basename(image))
    return images_to_show, images_names

def image_selection(img_name, var):
    """Append selected photos in the list of selected images"""
    global selected_images
    img_full_path = os.path.join(BASE_DIR, "celeba_5000_sample", img_name)

    if var.get() == 1:
        if img_full_path not in selected_images:
            selected_images.append(img_full_path)
    else:
        if img_full_path in selected_images:
            selected_images.remove(img_full_path)
    print("Images sélectionnées :", selected_images)


def show_images(frame, images_to_show, images_names):
    """Shows the 10 random images, organised in two rows and 5 columns"""

    image_refs = []
    for index in range(len(images_to_show)):
        img_path = images_to_show[index]
        img_name = images_names[index]

        image = ImageTk.PhotoImage(Image.open(img_path).resize((150, 150)))
        image_refs.append(image)

        row, col = divmod(index, 5)

        tk.Label(frame, image=image).grid(row=row * 2, column=col, padx=0, pady=0)

        var = tk.IntVar(value=0)
        tk.Checkbutton(frame, text="I choose you!", variable=var, bg = "#ad7e66",
                       command=lambda name=img_name, v=var: image_selection(name, v)
                       ).grid(row=row * 2 + 1, column=col, pady=5)

    frame.image_refs = image_refs


def reset_selection(directory, images_list, frame):
    """ Choose new photos and display them if the user doesn't like the previous ones"""

    global selected_images
    selected_images.clear()
    img_list, img_name = random_images(directory, images_list)
    for widget in frame.winfo_children():
        widget.destroy()
    show_images(frame, img_list, img_name)


def attr_selection(attr, v):
    """Selection of extra attributes, appends the attributes in the extra attributes list variable """

    global selected_attributes
    if v.get() == 1:
        if attr not in selected_attributes:
            selected_attributes.append(attr)
    else:
        if attr in selected_attributes:
            selected_attributes.remove(attr)
    print("Attributs sélectionnées :", selected_attributes)


def go_back(window):
    """Destroys the current window in case we want to go back """

    window.destroy()


def open_new_window(attributes, main_window):
    """ Opens the second window containing the extra attributes, this is where users
    choose their extra attributes """

    #create global variable that has the selected attributes

    second_window = tk.Toplevel()
    second_window.title("4BIM Project")
    second_window.geometry("500x600")
    second_window.resizable(False, False)
    second_window.configure(bg="#ecd7c6")

    second_frame = tk.Frame(second_window, bg="#ecd7c6")
    second_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(second_frame, bg="#ecd7c6")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    content_frame = tk.Frame(canvas, bg="#ecd7c6")
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    sec_title = tk.Label(content_frame, text="You can choose some extra characteristics :", font=("Century Gothic", 14, "bold"), bg="#ecd7c6")
    sec_title.grid(row=0, column=0, columnspan=2, pady=10)

    sec_wtd = tk.Label(content_frame, text="Select the attributes that you want to see in your final result :", font=("Century Gothic", 14, "bold"), bg="#ecd7c6")
    sec_wtd.grid(row=1, column=0, columnspan=2, pady=5)

    check_vars = {}
    for index in range(len(attributes)):
        attr = attributes[index]
        check_vars[attr] = tk.IntVar(value=0)
        row = (index // 2) + 2
        column = index % 2
        tk.Checkbutton(content_frame, text=attr, variable=check_vars[attr], bg="#ecd7c6",
                   command=lambda v=check_vars[attr], a=attr: attr_selection(a, v)
                   ).grid(row=row, column=column, padx=10, pady=2, sticky="w")

    validatebutton = tk.Button(second_window, text="I validate my choices!", bg="#ecd7c6", padx=10, pady=5, command=lambda: (main_window.withdraw(), second_window.withdraw(), open_third_window()))
    validatebutton.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.X)  # Make it fill horizontally and aligned to the right

    backbutton = tk.Button(second_window, text="I want to go back", bg="#ecd7c6", padx=10, pady=5, command=lambda: go_back(second_window))
    backbutton.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.X)  # Same for this button

attr_list = []

def open_third_window():
    global attr_list

    selected_imgs, selected_attrs = get_user_choices()

    transform = transforms.Compose([ 
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    images_tensor = []
    for img_path in selected_imgs:
        img = Image.open(img_path).convert("RGB")
        img_tensor = transform(img)
        images_tensor.append(img_tensor)

    images_tensor = torch.stack(images_tensor)

    parent_latents = get_latents_from_images(images_tensor, vae, device)
    children_latents = generate_initial_population(parent_latents, n_children=10)
    children_latents = force_attributes_on_latents(children_latents, attr_list, attribute_directions, attribute_strength)

    generation_history.clear()

    # Lancer directement la sélection dans une nouvelle fenêtre
    open_fourth_window(children_latents)

def open_fourth_window(parent_latents):
    global generation_history

    fourth_window = tk.Toplevel()
    fourth_window.title("New Generation")
    fourth_window.geometry("850x650")
    fourth_window.configure(bg="#FFEBCD")

    frame = tk.Frame(fourth_window, bg="#FFEBCD")
    frame.pack()

    # Génère les enfants
    children_latents = generate_initial_population(parent_latents, n_children=10)
    children_latents = force_attributes_on_latents(children_latents, attr_list, attribute_directions, attribute_strength)
    images = decode_latents_to_images(children_latents, vae, device)

    # Enregistre dans l’historique
    generation_history.append(parent_latents)

    # Affichage + sélection
    check_vars = []
    img_refs = []

    for idx in range(len(images)):
        img = to_pil_image(images[idx])
        img = img.resize((150, 150))
        img_tk = ImageTk.PhotoImage(img)
        img_refs.append(img_tk)

        row, col = divmod(idx, 5)
        img_label = tk.Label(frame, image=img_tk)
        img_label.grid(row=row * 2, column=col, padx=5, pady=5)

        var = tk.IntVar()
        check_vars.append(var)
        cb = tk.Checkbutton(frame, text="Select", variable=var, bg="#FFEBCD")
        cb.grid(row=row * 2 + 1, column=col)

    frame.image_refs = img_refs  # empêcher garbage collection

    def get_selected_children():
        selected = [children_latents[i] for i, v in enumerate(check_vars) if v.get() == 1]
        if not selected:
            return None
        return np.array(selected)

    # Bouton nouvelle génération
    def next_generation():
        selected = get_selected_children()
        if selected is not None:
            fourth_window.destroy()
            open_fourth_window(selected)

    def validate_final_choice():
        selected = get_selected_children()
        if selected is not None and len(selected) == 1:
            fourth_window.destroy()
            idx = [i for i, v in enumerate(check_vars) if v.get() == 1][0]
            open_final_result(images[idx])
        else:
            print("Please select only one image at a time.")


    # Relancer avec sélection (déjà existant)
    button_another = tk.Button(fourth_window, text="Another generation!", bg="#ad7e66", command=next_generation, padx=10, pady=5, width=30)
    button_another.pack(pady=10)

    # Regénérer les enfants avec les mêmes parents (nouveau)
    button_children = tk.Button(fourth_window, text="Generate other children from same parents", bg="#ecd7c6",
              command=lambda: (fourth_window.destroy(), open_fourth_window(parent_latents)),
              padx=10, pady=5, width=30)
    button_children.pack(pady=5)

    # Bouton validé
    button_validate = tk.Button(fourth_window, text="Looks good to me!",font = "14", bg="#f09175", command=validate_final_choice, padx=20, pady=10, width=30)
    button_validate.pack(pady=10)


def get_user_choices():
    return selected_images, selected_attributes

# ------------------- MAIN APPLICATION -------------------
def open_main_window():
    """Opens main window where the 10 random photos are displayed"""

    global selected_images, generation_history
    selected_images = []
    generation_history = []  # historique des latents pour revenir en arrière


    traits = pd.read_csv(attr_path, sep=';', header=0)
    attributes = list(traits)
    attributes.pop(0)

    attributes_modified = []
    for attr in attributes:
        attr = attr.replace("_", " ")
        #print(attr)
        attributes_modified.append(attr)

    #ERASE ATTRIBUTES THAT ARE USELESS, ALL NEEDED ATTRIBUTES ARE IN attributes_modified

    attributes_modified.pop(0)
    attributes_modified.pop(1)
    attributes_modified.remove("Blurry")
    attributes_modified.remove("Goatee")
    attributes_modified.remove("Mouth Slightly Open")
    attributes_modified.remove("Sideburns")
    attributes_modified.remove("Heavy Makeup")
    attributes_modified.remove("Bags Under Eyes")

    main_window = tk.Toplevel()
    main_window.title("4BIM Project")
    main_window.geometry("1000x600")
    main_window.resizable(False, False)
    main_window.configure(bg="#ecd7c6")


    main_label = tk.Label(main_window, bg="#ecd7c6", text="And so we begin...", font=("Century Gothic", 20, "bold"))
    main_label.grid(row=0, column=0, pady=10, padx=10)


    second_label = tk.Label(main_window, text="You are free to choose from the photos below, if you don't find anything you like, you can refresh the page!",
                        bg="#cf7928", fg="white", padx=300, pady=10, font=("Century Gothic", 14))
    second_label.grid(row=1, column=0, pady=5, padx=10)

    images_list = os.listdir(photos_directory)
    images_show, images_name = random_images(photos_directory, images_list)


    frame = tk.Frame(main_window, bg="#ad7e66")
    frame.grid(row=2, column=0, pady=10)

    show_images(frame, images_show, images_name)


    resetbutton = tk.Button(main_window,
                        text="I don't like these photos, redo!",
                        bg="#ecd7c6",
                        command=lambda: reset_selection(photos_directory, images_list, frame),
                        padx=5, pady=5,
                        relief="flat")
    resetbutton.bind("<Enter>", lambda e: on_enter(resetbutton))
    resetbutton.bind("<Leave>", lambda e: on_leave(resetbutton))

    resetbutton.grid(row=3, column=0, pady=10, padx=10)

    validatebutton = tk.Button(main_window,
                           text="Validate my choice, let's move on!",
                           bg="#ecd7c6",
                           command=lambda: open_new_window(attributes_modified, main_window),
                           padx=5, pady=5,
                           relief="flat")
    validatebutton.bind("<Enter>", lambda e: on_enter(validatebutton))
    validatebutton.bind("<Leave>", lambda e: on_leave(validatebutton))

    validatebutton.grid(row=4, column=0, pady=5, padx=10)


    main_window.grid_rowconfigure(0, weight=0)
    main_window.grid_rowconfigure(1, weight=0)
    main_window.grid_rowconfigure(2, weight=1)
    main_window.grid_rowconfigure(3, weight=0)
    main_window.grid_rowconfigure(4, weight=0)

    main_window.grid_columnconfigure(0, weight=1)  # Stretch columns in grid


def open_final_result(image_tensor):
    final_window = tk.Toplevel()
    final_window.title("Final Result")
    final_window.geometry("500x500")
    final_window.configure(bg="#ecd7c6")
    final_description = ("And here is the generated image by VisaGen! \n"
                         "We hope that the character created corresponds to \n"
                         "your wishes and that it was an easy and enjoyable experience!\n"
                         "Come see us again if you have another project in mind!\n")
    
    final_label = tk.Label(final_window, text=final_description, font=("Century Gothic", 10, "bold"), bg="#ecd7c6")
    final_label.pack(pady=20)

    # Convert the tensor to a PIL Image
    img = to_pil_image(image_tensor)
    img = img.resize((256, 256))
    img_tk = ImageTk.PhotoImage(img)

    img_label = tk.Label(final_window, image=img_tk, bg="#ecd7c6")
    img_label.image = img_tk  # garder la référence
    img_label.pack(pady=10)

    # Fonction pour télécharger l'image
    def download_image():
        # Demander à l'utilisateur où enregistrer l'image
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            img.save(file_path)
            print(f"Image saved to: {file_path}")

    # Ajouter un bouton de téléchargement
    download_button = tk.Button(final_window, text="Download", font=("Century Gothic", 14), bg="#f09175", command=download_image)
    download_button.pack(pady=10)


###########################
#####WELCOME WINDOW #######
###########################


if __name__ == "__main__":
    welcome_window = tk.Tk()
    welcome_window.title("Welcome to VisaGen")
    welcome_window.geometry("600x600")
    welcome_window.resizable(False, False)

    welcome_frame = tk.Frame(welcome_window, width=600, height=600, bg="#ecd7c6")
    welcome_frame.grid(row=0, column=0, sticky="nsew")

# Update grid weights to allow the frame to expand
    welcome_window.grid_rowconfigure(0, weight=1)
    welcome_window.grid_columnconfigure(0, weight=1)

    welcome_label = tk.Label(welcome_frame, text="Welcome to VisaGen", fg="black", font=("Century Gothic", 28, "bold"), bg="#ecd7c6")
    welcome_label.place(x=300, y=200, anchor=tk.CENTER)

    description_string = (
        "The rules are pretty simple:\n"
        "By starting this journey, you will have to choose some\n"
        " photos that you like,\n"
        "choose some extra attributes for your characters,\n" 
        "and we will do the job for you.\n"
        "We will suggest some photos that we have created, taking inspiration\n"
        "from the ones you just chose.\n"
        "No worries if you don't resonate with what we suggest\n"
        "We can always recreate new ideas!\n"
        "Enjoy the experience!\n"
        )

    description_label = tk.Label(welcome_frame, text=description_string, fg="white", font=("Century Gothic", 12, "bold"), bg="#ad7e66")
    description_label.place(x=300, y=350, anchor=tk.CENTER)

    start_button = tk.Button(welcome_window,
                         text="Let's start!",
                         bg="#ecd7c6",
                         padx=10, pady=5,
                         command=lambda: (welcome_window.withdraw(), open_main_window()),
                         relief="flat")

    start_button.bind("<Enter>", lambda e: on_enter(start_button))
    start_button.bind("<Leave>", lambda e: on_leave(start_button))

    start_button.grid(row=1, column=0, padx=5, pady=5)
    welcome_window.grid_rowconfigure(1, weight=0)

    welcome_window.update_idletasks()

    welcome_window.mainloop()