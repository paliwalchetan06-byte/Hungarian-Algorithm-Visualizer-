import tkinter as tk
from tkinter import messagebox
import numpy as np
from scipy.optimize import linear_sum_assignment
import matplotlib.pyplot as plt

# Function to calculate optimal assignment
def calculate_assignment():
    try:
        n = int(size_entry.get())
        matrix = []

        # Read matrix input and handle empty cells
        for i in range(n):
            row = []
            for j in range(n):
                val_str = entries[i][j].get()
                val = int(val_str) if val_str.strip() != "" else 0
                row.append(val)
            matrix.append(row)

        cost_matrix = np.array(matrix)

        # Apply Hungarian Algorithm
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        total_cost = 0
        result_text = "Optimal Assignment:\n\n"
        assignment_matrix = np.zeros_like(cost_matrix)

        for i in range(n):
            agent = row_ind[i]
            task = col_ind[i]
            cost = cost_matrix[agent, task]
            total_cost += cost
            result_text += f"Agent {agent+1} --> Task {task+1} | Cost = {cost}\n"
            assignment_matrix[agent, task] = cost

        result_text += f"\nMinimum Total Cost = {total_cost}"

        # Display result
        messagebox.showinfo("Result", result_text)

        # Heatmap Visualization
        plt.imshow(cost_matrix, cmap='viridis', interpolation='nearest')
        for i in range(n):
            for j in range(n):
                color = "red" if assignment_matrix[i, j] != 0 else "black"
                plt.text(j, i, str(cost_matrix[i, j]), ha='center', va='center', color=color)

        plt.title("Assignment Problem Heatmap (Red = Assigned)")
        plt.xlabel("Tasks")
        plt.ylabel("Agents")
        plt.xticks(range(n))
        plt.yticks(range(n))
        plt.colorbar(label="Cost")
        plt.tight_layout()
        plt.show()

    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers in all cells.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to create matrix input fields
def create_matrix():
    try:
        global entries
        n = int(size_entry.get())
        if n <= 0:
            messagebox.showerror("Error", "Number of agents/tasks must be positive.")
            return

        # Clear previous matrix
        for widget in matrix_frame.winfo_children():
            widget.destroy()

        entries = []
        for i in range(n):
            row_entries = []
            for j in range(n):
                e = tk.Entry(matrix_frame, width=5)
                e.grid(row=i, column=j, padx=5, pady=5)
                e.insert(0, "0")  # default value
                row_entries.append(e)
            entries.append(row_entries)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for the number of agents/tasks.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Assignment Problem Solver with Visualization")

tk.Label(root, text="Enter number of Agents/Tasks:").pack(pady=5)
size_entry = tk.Entry(root)
size_entry.pack(pady=5)

tk.Button(root, text="Create Matrix", command=create_matrix).pack(pady=5)

matrix_frame = tk.Frame(root)
matrix_frame.pack(pady=10)

tk.Button(root, text="Calculate Optimal Assignment", command=calculate_assignment).pack(pady=10)

root.mainloop()
