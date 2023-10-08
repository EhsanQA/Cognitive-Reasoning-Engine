import tkinter as tk
from tkinter import messagebox

class ParagraphLabeler:
    def __init__(self, root, labels):
        self.root = root
        self.labels = labels
        self.paragraph_index = 0
        self.paragraphs = []
        self.selected_labels = {}

        self.text_label = tk.Label(root, text="Paragraph:")
        self.text_label.pack()

        self.text_box = tk.Text(root, wrap=tk.WORD, height=10, width=50)
        self.text_box.pack()

        self.label_checkboxes = []
        for label in labels:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(root, text=label, variable=var)
            checkbox.pack()
            self.label_checkboxes.append((label, var))

        self.next_button = tk.Button(root, text="Next Paragraph", command=self.next_paragraph)
        self.next_button.pack()

        self.save_button = tk.Button(root, text="Save Labels", command=self.save_labels)
        self.save_button.pack()

        self.load_state()

    def load_paragraphs(self):
        with open("E:\Cognitive Reasoning Engine\Dataset\Soccernet\Soccernet_Labeled.txt", "r") as file:
            self.paragraphs = file.read().split('\n\n')
        self.display_paragraph()

    def load_state(self):
        try:
            with open("state.txt", "r") as file:
                state = file.readlines()
                self.paragraph_index = int(state[0])
                for line in state[1:]:
                    paragraph, *labels = line.strip().split("|")
                    self.selected_labels[paragraph] = labels
            self.load_paragraphs()
            self.display_paragraph()
        except FileNotFoundError:
            self.load_paragraphs()
            self.display_paragraph()

    def save_state(self):
        with open("state.txt", "w") as file:
            file.write(str(self.paragraph_index) + "\n")
            for paragraph, labels in self.selected_labels.items():
                labels_str = "|".join(labels)
                file.write(f"{paragraph}|{labels_str}\n")

    def display_paragraph(self):
        if self.paragraph_index < len(self.paragraphs):
            self.text_box.delete("1.0", tk.END)
            self.text_box.insert(tk.END, self.paragraphs[self.paragraph_index])

    def next_paragraph(self):
        self.selected_labels[self.paragraphs[self.paragraph_index]] = []
        for label, var in self.label_checkboxes:
            if var.get() == 1:
                self.selected_labels[self.paragraphs[self.paragraph_index]].append(label)
        self.paragraph_index += 1
        self.display_paragraph()

    def save_labels(self):
        with open("labels.txt", "a") as file:
            for paragraph, labels in self.selected_labels.items():
                labels_str = ', '.join(labels)
                file.write(f"Paragraph: {paragraph}\nLabels: {labels_str}\n\n")
        self.save_state()
        messagebox.showinfo("Saved", "Labels saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Paragraph Labeler")

    labels = [
        "Label1", "Label2", "Label3",  # Add your labels here
        # ...
        "Label35", "Label36", "Label37"
    ]

    labeler = ParagraphLabeler(root, labels)
    root.mainloop()
