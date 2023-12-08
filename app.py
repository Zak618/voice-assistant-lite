import tkinter as tk
from tkinter import ttk
from threading import Thread
import queue
import sounddevice as sd
import vosk
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from skils import *
import voice
import words

class VoiceAssistantApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Голосовой помощник | Made by Rolan")
        self.master.geometry("300x200")
        
        self.master.configure(bg="#043458")

        self.is_running = False
        self.q = queue.Queue()
        self.model = vosk.Model('model_small')
        self.device = sd.default.device = 0, 4
        self.samplerate = int(sd.query_devices(self.device[0], 'input')['default_samplerate'])
        
        self.vectorizer = CountVectorizer()
        self.vectors = self.vectorizer.fit_transform(list(words.data_set.keys()))
        
        self.clf = LogisticRegression()
        self.clf.fit(self.vectors, list(words.data_set.values()))
        
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=5, background="#215E7C", relief="flat")  
        
        self.start_stop_button = ttk.Button(self.master, text="Запустить", command=self.toggle_assistant)
        self.start_stop_button.pack(side=tk.TOP, pady=(50, 0)) 
        
        self.made_by_label = tk.Label(self.master, text="Made By Rolan", font=("Arial", 12), bg="#043458")
        self.made_by_label.pack(side=tk.BOTTOM, pady=(0, 10))  # Размещение надписи внизу
    
    def callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))
    
    def recognize(self, data):
        trg = words.TRIGGERS.intersection(data.split())
        if not trg:
            return
        
        data.replace(list(trg)[0], '')
        text_vector = self.vectorizer.transform([data]).toarray()[0]
        answer = self.clf.predict([text_vector])[0]
        
        func_name = answer.split()[0]
        speaker(answer.replace(func_name, ''))
        exec(func_name + '()')
    
    def main_loop(self):
        with sd.RawInputStream(samplerate=self.samplerate, blocksize=16000, device=self.device[0],
                               dtype="int16", channels=1, callback=self.callback):
            
            rec = vosk.KaldiRecognizer(self.model, self.samplerate)
            while self.is_running:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    data = json.loads(rec.Result())['text']
                    self.recognize(data)
    
    def toggle_assistant(self):
        if not self.is_running:
            self.is_running = True
            self.start_stop_button.configure(text="Остановить", style="TButton")
            self.assistant_thread = Thread(target=self.main_loop)
            self.assistant_thread.start()
        else:
            self.is_running = False
            self.start_stop_button.configure(text="Запустить", style="TButton")

if __name__ == '__main__':
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
