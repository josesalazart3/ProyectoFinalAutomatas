import tkinter as tk
from tkinter import messagebox
import json
from tkinter import filedialog

class TuringMachineSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Máquina de Turing")
        self.transitions = []
        self.configuration = {}
        self.tape = []
        self.head_position = 0
        self.current_state = ""
        self.create_widgets()

    def create_widgets(self):
        # Área para ingresar el alfabeto de entrada
        self.input_alphabet_label = tk.Label(self.root, text="Alfabeto de entrada (separado por comas):")
        self.input_alphabet_label.pack()
        self.input_alphabet_entry = tk.Entry(self.root)
        self.input_alphabet_entry.pack()

        # Área para ingresar el alfabeto de la cinta
        self.tape_alphabet_label = tk.Label(self.root, text="Alfabeto de la cinta (separado por comas):")
        self.tape_alphabet_label.pack()
        self.tape_alphabet_entry = tk.Entry(self.root)
        self.tape_alphabet_entry.pack()

        # Área para ingresar los estados
        self.states_label = tk.Label(self.root, text="Estados (separados por comas):")
        self.states_label.pack()
        self.states_entry = tk.Entry(self.root)
        self.states_entry.pack()

        # Campo para ingresar el estado inicial
        self.initial_state_label = tk.Label(self.root, text="Estado inicial:")
        self.initial_state_label.pack()
        self.initial_state_entry = tk.Entry(self.root)
        self.initial_state_entry.pack()

        # Campo para ingresar los estados de aceptación
        self.accepting_states_label = tk.Label(self.root, text="Estados de aceptación (separados por comas):")
        self.accepting_states_label.pack()
        self.accepting_states_entry = tk.Entry(self.root)
        self.accepting_states_entry.pack()

        # Área para ingresar las transiciones
        self.transition_label = tk.Label(self.root, text="Agregar transición:")
        self.transition_label.pack()

        self.current_state_entry = tk.Entry(self.root)
        self.current_state_entry.insert(0, "Estado actual")
        self.current_state_entry.pack()

        self.read_symbol_entry = tk.Entry(self.root)
        self.read_symbol_entry.insert(0, "Símbolo leído")
        self.read_symbol_entry.pack()

        self.next_state_entry = tk.Entry(self.root)
        self.next_state_entry.insert(0, "Estado siguiente")
        self.next_state_entry.pack()

        self.write_symbol_entry = tk.Entry(self.root)
        self.write_symbol_entry.insert(0, "Símbolo nuevo")
        self.write_symbol_entry.pack()

        self.direction_entry = tk.Entry(self.root)
        self.direction_entry.insert(0, "Dirección (L/R)")
        self.direction_entry.pack()

        self.add_transition_button = tk.Button(self.root, text="Agregar transición", command=self.add_transition)
        self.add_transition_button.pack()

        # Área para mostrar las transiciones agregadas
        self.transitions_display = tk.Label(self.root, text="Transiciones configuradas:")
        self.transitions_display.pack()
        self.transitions_listbox = tk.Listbox(self.root)
        self.transitions_listbox.pack()

        # Área para configurar la cinta y visualizar el cabezal
        self.tape_label = tk.Label(self.root, text="Cinta (ingrese la cadena inicial):")
        self.tape_label.pack()
        self.tape_entry = tk.Entry(self.root)
        self.tape_entry.pack()

        self.visualize_tape_button = tk.Button(self.root, text="Visualizar cinta", command=self.visualize_tape)
        self.visualize_tape_button.pack()

        self.tape_display = tk.Label(self.root, text="Cinta:")
        self.tape_display.pack()

        # Botón para ejecutar la máquina paso a paso
        self.step_button = tk.Button(self.root, text="Ejecutar paso", command=self.execute_step)
        self.step_button.pack()

        # Label para mostrar el resultado de la ejecución
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        # Botón para guardar la configuración
        self.save_button = tk.Button(self.root, text="Guardar configuración", command=self.save_configuration)
        self.save_button.pack()

        # Botón para cargar la configuración
        self.load_button = tk.Button(self.root, text="Cargar configuración", command=self.load_configuration)
        self.load_button.pack()

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
