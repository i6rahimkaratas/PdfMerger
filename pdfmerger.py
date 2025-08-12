import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os

class ModernImageToPDFConverter:
    def __init__(self, master):
        self.master = master
        master.title("Resimden PDF'e Dönüştürücü v2.0")
        master.geometry("600x650")
        master.resizable(False, False)

        
        self.BG_COLOR = "#f0f0f0"
        self.FRAME_COLOR = "#ffffff"
        self.ACCENT_COLOR = "#0078D7"
        self.TEXT_COLOR = "#333333"
        self.SUCCESS_COLOR = "#107C10"
        self.ERROR_COLOR = "#D83B01"

        master.configure(bg=self.BG_COLOR)

        
        self.style = ttk.Style(master)
        self.style.theme_use('clam')

        
        self.style.configure('Card.TFrame', background=self.FRAME_COLOR)
        
        
        self.style.configure('Card.TLabel', background=self.FRAME_COLOR, foreground=self.TEXT_COLOR)
        self.style.configure('Header.TLabel', background=self.BG_COLOR, foreground=self.TEXT_COLOR, font=("Helvetica", 20, "bold"))
        self.style.configure('Status.TLabel', background=self.BG_COLOR, foreground="gray", font=("Helvetica", 10, "italic"))
        
        
        self.style.configure('TButton', font=("Helvetica", 10)) 
        self.style.configure('Accent.TButton', background=self.ACCENT_COLOR, foreground='white', font=('Helvetica', 12, 'bold'), borderwidth=0, padding=10)
        self.style.map('Accent.TButton',
            background=[('active', '#005a9e')]
        )

        
        self.image_paths = []
        self.save_dir = ""

        
        self.create_widgets()

    def create_widgets(self):
        
        title_label = ttk.Label(self.master, text="Resimleri PDF'e Dönüştür", style='Header.TLabel')
        title_label.pack(pady=(20, 10))

        
        input_frame = ttk.Frame(self.master, padding=20, style='Card.TFrame')
        input_frame.pack(padx=20, pady=10, fill=tk.X)
        
        step1_label = ttk.Label(input_frame, text="1. Adım: Dosyaları Seçin", font=("Helvetica", 12, "bold"), style='Card.TLabel')
        step1_label.pack(anchor="w")

        select_button = ttk.Button(input_frame, text="Resim Dosyalarını Seç...", command=self.select_images, style='Accent.TButton')
        select_button.pack(fill=tk.X, pady=(10, 5))
        
        
        list_container = tk.Frame(input_frame, bg=self.FRAME_COLOR)
        list_container.pack(fill=tk.BOTH, expand=True, pady=5)

        self.listbox = tk.Listbox(
            list_container, height=8, selectmode=tk.SINGLE, bg="#eeeeee", fg=self.TEXT_COLOR,
            highlightthickness=0, borderwidth=1, relief="solid"
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        
        output_frame = ttk.Frame(self.master, padding=20, style='Card.TFrame')
        output_frame.pack(padx=20, pady=10, fill=tk.X)
        
        step2_label = ttk.Label(output_frame, text="2. Adım: Çıktı Ayarları", font=("Helvetica", 12, "bold"), style='Card.TLabel')
        step2_label.pack(anchor="w", pady=(0, 10))

        path_button = ttk.Button(output_frame, text="Kaydedilecek Konumu Seç...", command=self.select_save_dir)
        path_button.pack(fill=tk.X)
        
        self.save_path_label = ttk.Label(output_frame, text="Konum seçilmedi.", style='Card.TLabel', foreground="gray", wraplength=500)
        self.save_path_label.pack(anchor="w", pady=(5, 10))
        
        pdf_name_label = ttk.Label(output_frame, text="PDF Dosya Adı:", style='Card.TLabel')
        pdf_name_label.pack(anchor="w")
        self.pdf_name_entry = ttk.Entry(output_frame, font=("Helvetica", 10))
        self.pdf_name_entry.pack(fill=tk.X, pady=(5, 0))

        
        self.save_button = ttk.Button(self.master, text="PDF OLUŞTUR", command=self.convert_and_save, style='Accent.TButton')
        self.save_button.pack(padx=20, pady=20, fill=tk.X)
        
        
        self.status_label = ttk.Label(self.master, text="Başlamak için resimleri seçin.", style='Status.TLabel')
        self.status_label.pack(pady=(0, 10))

    
    def select_images(self):
        file_paths = filedialog.askopenfilenames(title="Birleştirilecek resimleri seçin")
        
        if file_paths:
            self.image_paths = sorted(list(file_paths))
            
            valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
            self.image_paths = [p for p in self.image_paths if p.lower().endswith(valid_extensions)]

            if not self.image_paths:
                messagebox.showwarning("Uyarı", "Seçilen dosyalar arasında desteklenen formatta (.jpg, .png vb.) resim bulunamadı.")
                return

            self.listbox.delete(0, tk.END)
            for path in self.image_paths:
                self.listbox.insert(tk.END, "  " + os.path.basename(path))
            
            self.status_label.config(text=f"{len(self.image_paths)} adet resim işlenmek için hazır.", foreground=self.TEXT_COLOR)

    def select_save_dir(self):
        directory = filedialog.askdirectory(title="Kaydedilecek konumu seçin")
        if directory:
            self.save_dir = directory
            self.save_path_label.config(text=f"Kaydedilecek Klasör: {self.save_dir}", foreground=self.TEXT_COLOR)

    def convert_and_save(self):
        if not self.image_paths:
            messagebox.showerror("Hata", "Lütfen önce birleştirmek için resimler seçin!")
            return
        if not self.save_dir:
            messagebox.showerror("Hata", "Lütfen PDF'in kaydedileceği konumu seçin!")
            return
        
        pdf_name = self.pdf_name_entry.get().strip()
        if not pdf_name:
            messagebox.showerror("Hata", "Lütfen PDF dosyası için bir ad girin!")
            return

        if not pdf_name.lower().endswith('.pdf'):
            pdf_name += '.pdf'

        output_path = os.path.join(self.save_dir, pdf_name)

        try:
            self.status_label.config(text="Dönüştürme işlemi başladı...", foreground=self.ACCENT_COLOR)
            self.master.update_idletasks()

            images_to_convert = []
            first_image = Image.open(self.image_paths[0]).convert('RGB')
            
            for path in self.image_paths[1:]:
                img = Image.open(path).convert('RGB')
                images_to_convert.append(img)

            first_image.save(
                output_path, "PDF", resolution=100.0, 
                save_all=True, append_images=images_to_convert
            )
            
            self.status_label.config(text=f"Başarılı! PDF kaydedildi.", foreground=self.SUCCESS_COLOR)
            messagebox.showinfo("İşlem Tamamlandı", f"PDF dosyası başarıyla oluşturuldu!\n\nKonum: {output_path}")
            
            self.listbox.delete(0, tk.END)
            self.image_paths = []
            self.pdf_name_entry.delete(0, tk.END)
            self.status_label.config(text="Yeni bir işlem için resim seçin.", foreground="gray")

        except Exception as e:
            self.status_label.config(text=f"Bir hata oluştu!", foreground=self.ERROR_COLOR)
            messagebox.showerror("Hata", f"PDF oluşturulurken bir hata meydana geldi:\n\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernImageToPDFConverter(root)
    root.mainloop()
