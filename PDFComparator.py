import difflib
from PyPDF2 import PdfReader
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def extract_text_from_pdf(pdf_path):
    """Извлекает текст из PDF-файла."""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""  # Добавляем пустую строку, если текст None
    except Exception as e:
        print(f"Ошибка при чтении файла {pdf_path}: {e}")
    return text

def compare_pdfs(file1, file2):
    """Сравнивает два PDF-файла и возвращает различия в HTML формате."""
    text1 = extract_text_from_pdf(file1)
    text2 = extract_text_from_pdf(file2)
    
    # Разбиваем текст на строки для сравнения
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    
    # Создаем differ объект
    d = difflib.HtmlDiff()
    
    # Генерируем HTML с различиями
    diff_html = d.make_file(lines1, lines2, file1, file2, context=True, numlines=3)
    
    return diff_html

def save_diff_to_html(diff_html, output_file):
    """Сохраняет различия в HTML файл."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(diff_html)

def select_file(entry_widget):
    """Открывает диалог выбора файла и вставляет путь в виджет Entry."""
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filepath)

def run_comparison():
    """Выполняет сравнение файлов и показывает результат."""
    file1 = entry_file1.get()
    file2 = entry_file2.get()
    
    if not file1 or not file2:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите оба PDF-файла")
        return
    
    try:
        # Показываем индикатор прогресса
        progress_bar.start()
        root.update_idletasks()
        
        # Выполняем сравнение
        diff_html = compare_pdfs(file1, file2)
        
        # Предлагаем сохранить результат
        output_file = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html")],
            title="Сохранить результат сравнения"
        )
        
        if output_file:
            save_diff_to_html(diff_html, output_file)
            messagebox.showinfo("Успех", f"Результат сравнения сохранен в:\n{output_file}")
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка:\n{str(e)}")
    finally:
        progress_bar.stop()

# Создаем графический интерфейс
root = tk.Tk()
root.title("Сравнение PDF-файлов 1.0    Автор: Пожидаев И.Г., 2025 г.")
root.geometry("600x300")

# Фрейм для выбора файлов
frame_files = ttk.LabelFrame(root, text="Выберите PDF-файлы для сравнения", padding=10)
frame_files.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Поле для первого файла
ttk.Label(frame_files, text="PDF файл 1:").grid(row=0, column=0, sticky=tk.W, pady=5)
entry_file1 = ttk.Entry(frame_files, width=50)
entry_file1.grid(row=0, column=1, padx=5)
ttk.Button(frame_files, text="Обзор...", command=lambda: select_file(entry_file1)).grid(row=0, column=2)

# Поле для второго файла
ttk.Label(frame_files, text="PDF файл 2:").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_file2 = ttk.Entry(frame_files, width=50)
entry_file2.grid(row=1, column=1, padx=5)
ttk.Button(frame_files, text="Обзор...", command=lambda: select_file(entry_file2)).grid(row=1, column=2)

# Кнопка сравнения
btn_compare = ttk.Button(root, text="Сравнить файлы", command=run_comparison)
btn_compare.pack(pady=10)

# Индикатор прогресса
progress_bar = ttk.Progressbar(root, mode='indeterminate', length=300)
progress_bar.pack(pady=10)

root.mainloop()