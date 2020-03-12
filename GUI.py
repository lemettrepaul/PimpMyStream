import tkinter as tk
import PimpMyStream as pms

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        #URL
        self.URL_label = tk.Label(self, text="Lien de votre stream youtube :")
        self.URL_label.pack()

        self.url_textbox = tk.Text(self, height=1, width=40)
        self.url_textbox.pack()

        #Delay
        self.delay_label = tk.Label(self, text="Durée du vote en secondes :")
        self.delay_label.pack()

        self.delay_textbox = tk.Text(self, height=1, width=5)
        self.delay_textbox.pack()

        #Choix
        self.choice_label = tk.Label(self, text="Rentrez vos choix de votes (séparés par un ';')\n par exemple : 'wow;cs;lol'")
        self.choice_label.pack()

        self.choice_textbox = tk.Text(self, height=2, width=40)
        self.choice_textbox.pack()

        #Submit Button
        self.submit_button = tk.Button(self)
        self.submit_button["text"] = "Commencer le vote"
        self.submit_button["command"] = self.submit
        self.submit_button.pack(side="top")


    def submit(self):

        stream_url = self.url_textbox.get("1.0", tk.END)
        delay = self.delay_textbox.get("1.0", tk.END)
        choices = self.choice_textbox.get("1.0", tk.END)
        print(choices)
        title = "du coup ?"
        pms.run_poll(delay, choices, stream_url, title)

root = tk.Tk()
root.geometry("400x200")
root.title("Démocratie sur mon stream")
app = Application(master=root)
app.mainloop()