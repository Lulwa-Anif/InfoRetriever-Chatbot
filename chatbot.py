
---------- Forwarded message ---------
From: Sakshi Joshi <ssjoshi371122@kkwagh.edu.in>
Date: Mon, Aug 5, 2024 at 8:51 PM
Subject: 
To: lulwa anif <luluvaanif53@gmail.com>

import tkinter as tk
from tkinter import filedialog, Text
from PyPDF2 import PdfReader
from PIL import Image, ImageTk
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

nltk.download('punkt')

class DocumentChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("INFO-RETRIEVER")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        self.set_styles()
        
        self.create_widgets()
        
        self.document_text = ""

    def set_styles(self):
        self.bg_color = '#2b2b2b'
        self.fg_color = '#ffffff'
        self.button_color = '#ff6347'
        self.font = ('Helvetica', 12)
        self.title_font = ('Helvetica', 18, 'bold')

    def create_widgets(self):
        # Create canvas for background image
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Add a background image
        try:
            self.bg_image = Image.open("background.jpg")
            self.bg_image = self.bg_image.resize((800, 600), Image.LANCZOS)
            self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
            self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
        except FileNotFoundError:
            self.output_text.insert(tk.END, "Background image not found.\n")

        self.title_label = tk.Label(self.root, text="INFO-RETRIEVER", font=self.title_font, bg=self.bg_color, fg=self.button_color)
        self.canvas.create_window(400, 50, window=self.title_label)

        self.upload_button = tk.Button(self.root, text="Upload Document", command=self.upload_document, bg=self.button_color, fg=self.fg_color, font=self.font)
        self.canvas.create_window(400, 100, window=self.upload_button)
        
        self.question_label = tk.Label(self.root, text="Ask a Question:", font=self.font, bg=self.bg_color, fg=self.fg_color)
        self.canvas.create_window(400, 150, window=self.question_label)
        
        self.question_entry = tk.Entry(self.root, width=50, font=self.font)
        self.canvas.create_window(400, 180, window=self.question_entry)
        
        self.answer_button = tk.Button(self.root, text="Get Answer", command=self.get_answer, bg=self.button_color, fg=self.fg_color, font=self.font)
        self.canvas.create_window(400, 220, window=self.answer_button)
        
        self.summary_button = tk.Button(self.root, text="Get Summary", command=self.get_summary, bg=self.button_color, fg=self.fg_color, font=self.font)
        self.canvas.create_window(400, 260, window=self.summary_button)
        
        self.output_text = Text(self.root, height=10, font=self.font, bg='#3c3f41', fg=self.fg_color)
        self.canvas.create_window(400, 370, window=self.output_text, width=700, height=200)

    def upload_document(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as f:
                pdf = PdfReader(f)
                self.document_text = ""
                for page in pdf.pages:
                    self.document_text += page.extract_text()
            self.output_text.insert(tk.END, "Document uploaded successfully.\n")
    
    def get_answer(self):
        question = self.question_entry.get()
        answer = self.search_document(question)
        self.output_text.insert(tk.END, f"Answer: {answer}\n")
    
    def search_document(self, question):
        sentences = nltk.sent_tokenize(self.document_text)
        question_words = set(nltk.word_tokenize(question.lower()))
        best_sentence = ""
        max_overlap = 0
        for sentence in sentences:
            sentence_words = set(nltk.word_tokenize(sentence.lower()))
            overlap = len(question_words & sentence_words)
            if overlap > max_overlap:
                max_overlap = overlap
                best_sentence = sentence
        return best_sentence if best_sentence else "No relevant answer found."
    
    def get_summary(self):
        parser = PlaintextParser.from_string(self.document_text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 5)  # Summarize to 5 sentences
        summary_text = "\n".join([str(sentence) for sentence in summary])
        self.output_text.insert(tk.END, f"Summary: {summary_text}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentChatbot(root)
    root.mainloop()

