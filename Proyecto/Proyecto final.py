import tkinter as tk
from tkinter import messagebox
import json
from tkinter import filedialog, ttk

class TuringMachineSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Máquina de Turing")

        # Crear un menú
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # Crear la pestaña 'Archivo'
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Guardar configuración", command=self.save_configuration)
        self.file_menu.add_command(label="Cargar configuración", command=self.load_configuration)

        # Crear un frame principal con un canvas para permitir el desplazamiento
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame)
        self.scroll_y = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.transitions = []
        self.configuration = {}
        self.tape = []
        self.head_position = 0
        self.current_state = ""

        self.create_widgets()

    def create_widgets(self):
        # Área para ingresar el alfabeto de entrada
        self.input_alphabet_label = tk.Label(self.scrollable_frame, text="Alfabeto de entrada (separado por comas):")
        self.input_alphabet_label.pack(pady=5)
        self.input_alphabet_entry = tk.Entry(self.scrollable_frame, width=50)
        self.input_alphabet_entry.pack(pady=5)

        # Área para ingresar el alfabeto de la cinta
        self.tape_alphabet_label = tk.Label(self.scrollable_frame, text="Alfabeto de la cinta (separado por comas):")
        self.tape_alphabet_label.pack(pady=5)
        self.tape_alphabet_entry = tk.Entry(self.scrollable_frame, width=50)
        self.tape_alphabet_entry.pack(pady=5)

        # Área para ingresar los estados
        self.states_label = tk.Label(self.scrollable_frame, text="Estados (separados por comas):")
        self.states_label.pack(pady=5)
        self.states_entry = tk.Entry(self.scrollable_frame, width=50)
        self.states_entry.pack(pady=5)

        # Campo para ingresar el estado inicial
        self.initial_state_label = tk.Label(self.scrollable_frame, text="Estado inicial:")
        self.initial_state_label.pack(pady=5)
        self.initial_state_entry = tk.Entry(self.scrollable_frame, width=50)
        self.initial_state_entry.pack(pady=5)

        # Campo para ingresar los estados de aceptación
        self.accepting_states_label = tk.Label(self.scrollable_frame, text="Estados de aceptación (separados por comas):")
        self.accepting_states_label.pack(pady=5)
        self.accepting_states_entry = tk.Entry(self.scrollable_frame, width=50)
        self.accepting_states_entry.pack(pady=5)

        # Área para ingresar las transiciones
        self.transition_label = tk.Label(self.scrollable_frame, text="Agregar transición:")
        self.transition_label.pack(pady=10)

        self.current_state_entry = tk.Entry(self.scrollable_frame)
        self.current_state_entry.insert(0, "Estado actual")
        self.current_state_entry.pack(pady=5)

        self.read_symbol_entry = tk.Entry(self.scrollable_frame)
        self.read_symbol_entry.insert(0, "Símbolo leído")
        self.read_symbol_entry.pack(pady=5)

        self.next_state_entry = tk.Entry(self.scrollable_frame)
        self.next_state_entry.insert(0, "Estado siguiente")
        self.next_state_entry.pack(pady=5)

        self.write_symbol_entry = tk.Entry(self.scrollable_frame)
        self.write_symbol_entry.insert(0, "Símbolo nuevo")
        self.write_symbol_entry.pack(pady=5)

        self.direction_entry = tk.Entry(self.scrollable_frame)
        self.direction_entry.insert(0, "Dirección (L/R)")
        self.direction_entry.pack(pady=5)

        self.add_transition_button = tk.Button(self.scrollable_frame, text="Agregar transición", command=self.add_transition)
        self.add_transition_button.pack(pady=5)

        # Área para mostrar las transiciones agregadas
        self.transitions_display = tk.Label(self.scrollable_frame, text="Transiciones configuradas:")
        self.transitions_display.pack(pady=10)
        self.transitions_listbox = tk.Listbox(self.scrollable_frame, width=80)
        self.transitions_listbox.pack(pady=5)

        # Área para configurar la cinta y visualizar el cabezal
        self.tape_label = tk.Label(self.scrollable_frame, text="Cinta (ingrese la cadena inicial):")
        self.tape_label.pack(pady=10)
        self.tape_entry = tk.Entry(self.scrollable_frame, width=50)
        self.tape_entry.pack(pady=5)

        self.visualize_tape_button = tk.Button(self.scrollable_frame, text="Visualizar cinta", command=self.visualize_tape)
        self.visualize_tape_button.pack(pady=5)

        self.tape_display = tk.Label(self.scrollable_frame, text="Cinta:")
        self.tape_display.pack(pady=5)

        # Botón para ejecutar la máquina paso a paso
        self.step_button = tk.Button(self.scrollable_frame, text="Ejecutar paso", command=self.execute_step)
        self.step_button.pack(pady=5)

        # Label para mostrar el resultado de la ejecución
        self.result_label = tk.Label(self.scrollable_frame, text="")
        self.result_label.pack(pady=5)

    def add_transition(self):
        # Obtener los valores de las entradas
        current_state = self.current_state_entry.get().strip()
        read_symbol = self.read_symbol_entry.get().strip()
        next_state = self.next_state_entry.get().strip()
        write_symbol = self.write_symbol_entry.get().strip()
        direction = self.direction_entry.get().strip().upper()

        # Validar que los campos no estén vacíos y que la dirección sea válida
        if not current_state or not read_symbol or not next_state or not write_symbol:
            messagebox.showerror("Error", "Todos los campos deben estar completos.")
            return
        if direction not in ['L', 'R']:
            messagebox.showerror("Error", "La dirección debe ser 'L' (izquierda) o 'R' (derecha).")
            return

        # Agregar la transición a la lista
        transition = (current_state, read_symbol, next_state, write_symbol, direction)
        self.transitions.append(transition)

        # Actualizar la visualización de las transiciones
        self.transitions_listbox.insert(tk.END, f"{transition[0]}, {transition[1]} -> {transition[2]}, {transition[3]}, {transition[4]}")

    def save_configuration(self):
        input_alphabet = self.input_alphabet_entry.get().split(',')
        tape_alphabet = self.tape_alphabet_entry.get().split(',')
        states = self.states_entry.get().split(',')
        initial_state = self.initial_state_entry.get()
        accepting_states = self.accepting_states_entry.get().split(',')

        self.configuration = {
            'input_alphabet': [symbol.strip() for symbol in input_alphabet],
            'tape_alphabet': [symbol.strip() for symbol in tape_alphabet],
            'states': [state.strip() for state in states],
            'initial_state': initial_state.strip(),
            'accepting_states': [state.strip() for state in accepting_states],
            'transitions': self.transitions
        }

        # Abrir un cuadro de diálogo para guardar el archivo
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as json_file:
                json.dump(self.configuration, json_file, indent=4)
            messagebox.showinfo("Éxito", "Configuración guardada correctamente.")

    def load_configuration(self):
        # Abrir un cuadro de diálogo para cargar un archivo
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as json_file:
                self.configuration = json.load(json_file)

            # Cargar la configuración en la interfaz
            self.input_alphabet_entry.delete(0, tk.END)
            self.input_alphabet_entry.insert(0, ', '.join(self.configuration['input_alphabet']))

            self.tape_alphabet_entry.delete(0, tk.END)
            self.tape_alphabet_entry.insert(0, ', '.join(self.configuration['tape_alphabet']))

            self.states_entry.delete(0, tk.END)
            self.states_entry.insert(0, ', '.join(self.configuration['states']))

            self.initial_state_entry.delete(0, tk.END)
            self.initial_state_entry.insert(0, self.configuration['initial_state'])

            self.accepting_states_entry.delete(0, tk.END)
            self.accepting_states_entry.insert(0, ', '.join(self.configuration['accepting_states']))

            self.transitions = self.configuration['transitions']
            self.transitions_listbox.delete(0, tk.END)
            for transition in self.transitions:
                self.transitions_listbox.insert(tk.END, f"{transition[0]}, {transition[1]} -> {transition[2]}, {transition[3]}, {transition[4]}")

            messagebox.showinfo("Éxito", "Configuración cargada correctamente.")

    def visualize_tape(self):
        tape_string = self.tape_entry.get()
        self.tape = list(tape_string)
        self.head_position = 0
        self.update_tape_display()
        self.result_label.config(text="")  # Reiniciar el resultado al visualizar la cinta
        self.current_state = self.initial_state_entry.get().strip()  # Inicializar el estado actual

    def update_tape_display(self):
        tape_visual = ''.join(self.tape)
        head_visual = ' ' * self.head_position + '^'
        self.tape_display.config(text=f"Cinta: {tape_visual}\nCabezal: {head_visual}\nEstado actual: {self.current_state}")

    def execute_step(self):
        if self.head_position < 0 or self.head_position >= len(self.tape):
            messagebox.showerror("Error", "El cabezal ha salido de los límites de la cinta.")
            return

        # Si el estado actual no se ha inicializado, asigna el estado inicial
        if not self.current_state:
            self.current_state = self.initial_state_entry.get().strip()

        current_symbol = self.tape[self.head_position]
        transition_found = False

        for transition in self.transitions:
            if transition[0] == self.current_state and transition[1] == current_symbol:
                self.current_state = transition[2]
                self.tape[self.head_position] = transition[3]
                self.head_position += -1 if transition[4] == 'L' else 1
                self.update_tape_display()
                transition_found = True
                break

        if not transition_found:
            messagebox.showinfo("Fin de la simulación", "No hay transición disponible para el estado y símbolo actuales.")
            self.result_label.config(text="Cadena rechazada.")
            return

        # Comprobar si el estado actual es un estado de aceptación
        accepting_states = self.accepting_states_entry.get().split(',')
        if self.current_state in accepting_states:
            self.result_label.config(text="Cadena aceptada.")
        else:
            self.result_label.config(text="Cadena en ejecución...")

if __name__ == "__main__":
    root = tk.Tk()
    app = TuringMachineSimulator(root)
    root.mainloop()
