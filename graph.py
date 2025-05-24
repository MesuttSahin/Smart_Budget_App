import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_category_bar_chart(frame, username, results):
    if not results:
        return
    
    for widget in frame.winfo_children():
        widget.destroy()
    
    categories = [row[0] for row in results]
    amounts = [row[1] for row in results]
    
    fig, ax = plt.subplots(figsize=(5, 3))  
    
    ax.bar(categories, amounts, color='skyblue')
    ax.set_title("Kategoriye göre harcamalar")
    ax.set_ylabel("Tutar")
    ax.set_xlabel("Kategori")
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    fig.tight_layout()  
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
