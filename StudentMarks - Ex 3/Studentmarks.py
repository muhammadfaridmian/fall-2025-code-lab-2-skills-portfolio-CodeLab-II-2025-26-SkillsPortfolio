import tkinter as tk
from tkinter import ttk, messagebox
import math # Needed for the pie chart calculations
import os

# =============================================================================
# CONFIGURATION & VISUAL THEME
# I'm using a "Slate & Emerald" theme. It feels professional and data-heavy.
# =============================================================================
THEME = {
    'bg_dark':      '#1E293B', # Deep slate sidebar
    'bg_canvas':    '#F1F5F9', # Light grey-blue background
    'card_white':   '#FFFFFF',
    'primary':      '#0EA5E9', # Sky blue
    'accent':       '#6366f1', # Indigo
    'success':      '#10B981', # Emerald green
    'danger':       '#EF4444', # Red
    'warning':      '#F59E0B', # Amber
    'text_head':    '#0F172A', # Nearly black
    'text_body':    '#64748B'  # Muted text
}

FONTS = {
    'h1': ("Segoe UI", 22, "bold"),
    'h2': ("Segoe UI", 16, "bold"),
    'h3': ("Segoe UI", 13, "bold"),
    'body': ("Segoe UI", 11),
    'small': ("Segoe UI", 9)
}

# =============================================================================
# LOGIC LAYER: DATA PROCESSING
# =============================================================================
class StudentData:
    """
    Holds all the detailed math for a single student.
    I broke the marks down into components for the 'Detailed Analysis' tab.
    """
    def __init__(self, line_data):
        # Parse the CSV line: ID,Name,CW1,CW2,CW3,Exam
        parts = line_data.strip().split(',')
        
        self.id = parts[0]
        self.name = parts[1]
        
        # Store raw integers
        self.marks = {
            'cw1': int(parts[2]), # out of 20
            'cw2': int(parts[3]), # out of 20
            'cw3': int(parts[4]), # out of 20
            'exam': int(parts[5]) # out of 100
        }
        
        # The heavy lifting / Math
        self.cw_total = sum([self.marks['cw1'], self.marks['cw2'], self.marks['cw3']])
        self.overall_score = self.cw_total + self.marks['exam']
        
        # Percentage calc (Max score is 160)
        self.percentage = (self.overall_score / 160) * 100
        self.grade = self._calculate_grade()
        
        # Flag for the "At Risk" category
        self.is_failing = self.percentage < 40

    def _calculate_grade(self):
        if self.percentage >= 70: return 'A'
        if self.percentage >= 60: return 'B'
        if self.percentage >= 50: return 'C'
        if self.percentage >= 40: return 'D'
        return 'F'

# =============================================================================
# CUSTOM UI WIDGETS
# Making things look pretty requires some custom classes
# =============================================================================
class ModernButton(tk.Button):
    """A button that highlights when you hover over it."""
    def __init__(self, master, text, icon, command):
        self.default_bg = THEME['bg_dark']
        self.hover_bg = '#334155' # slightly lighter slate
        
        super().__init__(master, text=f"  {icon}  {text}", font=FONTS['h3'], 
                         bg=self.default_bg, fg="white", activebackground=self.hover_bg,
                         activeforeground="white", bd=0, anchor="w", padx=25, pady=12,
                         cursor="hand2", command=command)
        
        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, e):
        self.config(bg=self.hover_bg)
        
    def _on_leave(self, e):
        self.config(bg=self.default_bg)

# =============================================================================
# MAIN APPLICATION
# =============================================================================
class GradeBookPro(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("GradeBook AI | Enterprise Edition")
        self.geometry("1280x800")
        self.state('zoomed') # Start maximized
        self.configure(bg=THEME['bg_canvas'])
        
        self.students = []
        
        # 1. Init System
        self._check_files()
        self._load_data()
        
        # 2. Build Layout
        self._setup_sidebar()
        self._setup_main_area()
        
        # 3. Launch Dashboard by default
        self.show_dashboard()

    # --- Data Handling ---
    def _check_files(self):
        # If the file doesn't exist, I'll create it so the code works immediately.
        if not os.path.exists("studentMarks.txt"):
            with open("studentMarks.txt", "w") as f:
                f.write("10\n") # Header count
                # Dummy data: ID, Name, CW1, CW2, CW3, Exam
                data = """1001,Alice Carter,18,19,18,92
1002,Bob Miller,12,14,11,65
1003,Charlie Davis,5,8,6,40
1004,Diana Prince,20,20,19,98
1005,Evan Wright,8,9,8,35
1006,Fiona Gallagher,15,16,15,78
1007,George King,11,10,12,55
1008,Hannah Montana,19,18,20,90
1009,Ian Malcolm,14,14,14,72
1010,Jack Sparrow,2,4,3,15"""
                f.write(data)

    def _load_data(self):
        try:
            with open("studentMarks.txt", "r") as f:
                lines = f.readlines()
                for line in lines[1:]: # Skip the count line
                    if line.strip():
                        self.students.append(StudentData(line))
        except Exception:
            messagebox.showerror("Data Error", "Critical error loading database file.")

    # --- UI Structure ---
    def _setup_sidebar(self):
        self.sidebar = tk.Frame(self, bg=THEME['bg_dark'], width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Brand / Logo
        title = tk.Label(self.sidebar, text="EDU\nANALYTICS", font=("Segoe UI", 30, "bold"), 
                         bg=THEME['bg_dark'], fg=THEME['primary'], justify="center")
        title.pack(pady=(40, 40))
        
        # Menu Items
        ModernButton(self.sidebar, "Executive Dashboard", "📊", self.show_dashboard).pack(fill="x", pady=2)
        ModernButton(self.sidebar, "Student Registry", "👥", self.show_registry).pack(fill="x", pady=2)
        ModernButton(self.sidebar, "Assessment Breakdown", "📈", self.show_breakdown).pack(fill="x", pady=2)
        ModernButton(self.sidebar, "At-Risk Monitor", "⚠️", self.show_risk_monitor).pack(fill="x", pady=2)
        
        # Version info footer
        tk.Label(self.sidebar, text="v4.5.2 stable", fg="#475569", bg=THEME['bg_dark']).pack(side="bottom", pady=20)

    def _setup_main_area(self):
        # Container for content
        self.main_frame = tk.Frame(self, bg=THEME['bg_canvas'])
        self.main_frame.pack(side="right", fill="both", expand=True)
        
        # We need scrolling for detailed lists
        self.canvas = tk.Canvas(self.main_frame, bg=THEME['bg_canvas'], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_inner = tk.Frame(self.canvas, bg=THEME['bg_canvas'])
        
        self.scroll_inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_inner, anchor="nw", width=1000)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        self.scrollbar.pack(side="right", fill="y")

    def _clear_view(self):
        for widget in self.scroll_inner.winfo_children():
            widget.destroy()

    # =========================================================================
    # CATEGORY 1: EXECUTIVE DASHBOARD (Visuals)
    # =========================================================================
    def show_dashboard(self):
        self._clear_view()
        tk.Label(self.scroll_inner, text="Executive Overview", font=FONTS['h1'], bg=THEME['bg_canvas'], fg=THEME['text_head']).pack(anchor="w")
        
        # 1. Top Cards Row
        row1 = tk.Frame(self.scroll_inner, bg=THEME['bg_canvas'])
        row1.pack(fill="x", pady=20)
        
        # Calc stats
        avg = sum(s.percentage for s in self.students) / len(self.students)
        passes = sum(1 for s in self.students if not s.is_failing)
        
        self._draw_kpi_card(row1, "Class Average", f"{avg:.1f}%", THEME['primary'])
        self._draw_kpi_card(row1, "Total Enrolled", str(len(self.students)), THEME['warning'])
        self._draw_kpi_card(row1, "Pass Rate", f"{passes}/{len(self.students)}", THEME['success'])

        # 2. Charts Area
        chart_row = tk.Frame(self.scroll_inner, bg=THEME['bg_canvas'])
        chart_row.pack(fill="x", pady=10)
        
        # Grade Distribution (Bar Chart)
        self._draw_bar_chart(chart_row)
        
        # Pass vs Fail (Pie Chart)
        self._draw_pie_chart(chart_row)

    def _draw_kpi_card(self, parent, title, value, color):
        """Creates a nice shadowed box for a single statistic."""
        card = tk.Frame(parent, bg=THEME['card_white'], padx=20, pady=20)
        card.pack(side="left", expand=True, fill="x", padx=10)
        
        # Decorative colored bar
        tk.Frame(card, bg=color, height=4).pack(fill="x", pady=(0,10))
        
        tk.Label(card, text=title.upper(), font=FONTS['small'], fg=THEME['text_body'], bg="white").pack(anchor="w")
        tk.Label(card, text=value, font=("Segoe UI", 28, "bold"), fg=THEME['text_head'], bg="white").pack(anchor="w")

    def _draw_bar_chart(self, parent):
        """Manually draws a bar chart on a canvas."""
        frame = tk.Frame(parent, bg="white", padx=20, pady=20)
        frame.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(frame, text="Grade Distribution", font=FONTS['h3'], bg="white", fg=THEME['text_head']).pack(anchor="w")
        
        # Canvas for drawing
        h = 200
        c = tk.Canvas(frame, bg="white", height=h, highlightthickness=0)
        c.pack(fill="x", pady=10)
        
        # Get data
        grades = {'A':0, 'B':0, 'C':0, 'D':0, 'F':0}
        for s in self.students: grades[s.grade] += 1
        max_val = max(grades.values()) if grades else 1
        
        # Draw bars
        x_start = 30
        bar_w = 50
        gap = 40
        
        for i, (grade, count) in enumerate(grades.items()):
            x = x_start + (i * (bar_w + gap))
            bar_h = (count / max_val) * (h - 40) # Scale height
            
            # Color logic
            color = THEME['success'] if grade in ['A','B'] else (THEME['warning'] if grade=='C' else THEME['danger'])
            
            # Draw bar
            c.create_rectangle(x, h-20, x+bar_w, (h-20)-bar_h, fill=color, outline="")
            # Draw text
            c.create_text(x + bar_w/2, h-5, text=grade, font=("Segoe UI", 10, "bold"))
            c.create_text(x + bar_w/2, (h-20)-bar_h-10, text=str(count), fill="#666")

    def _draw_pie_chart(self, parent):
        """Manually draws a pie chart for Pass/Fail."""
        frame = tk.Frame(parent, bg="white", padx=20, pady=20)
        frame.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(frame, text="Pass/Fail Ratio", font=FONTS['h3'], bg="white", fg=THEME['text_head']).pack(anchor="w")
        
        c = tk.Canvas(frame, bg="white", height=200, width=200, highlightthickness=0)
        c.pack(pady=10)
        
        pass_c = sum(1 for s in self.students if not s.is_failing)
        fail_c = len(self.students) - pass_c
        
        if len(self.students) == 0: return

        # Calculate angles (360 degrees total)
        pass_angle = (pass_c / len(self.students)) * 360
        
        # Draw Pass Arc (Green)
        c.create_arc(10, 10, 190, 190, start=0, extent=pass_angle, fill=THEME['success'], outline="white")
        # Draw Fail Arc (Red)
        c.create_arc(10, 10, 190, 190, start=pass_angle, extent=360-pass_angle, fill=THEME['danger'], outline="white")
        
        # Legend
        tk.Label(frame, text=f"Passing: {pass_c}   |   Failing: {fail_c}", bg="white", fg="#666").pack()

    # =========================================================================
    # CATEGORY 2: STUDENT REGISTRY (Detailed List)
    # =========================================================================
    def show_registry(self):
        self._clear_view()
        
        # Header
        head = tk.Frame(self.scroll_inner, bg=THEME['bg_canvas'])
        head.pack(fill="x", pady=(0,20))
        tk.Label(head, text="Student Registry", font=FONTS['h1'], bg=THEME['bg_canvas'], fg=THEME['text_head']).pack(side="left")
        
        # Search bar (Simple simulation)
        entry = tk.Entry(head, font=FONTS['body'])
        entry.pack(side="right", padx=10)
        tk.Label(head, text="Search:", bg=THEME['bg_canvas']).pack(side="right")

        # Render list
        for s in sorted(self.students, key=lambda x: x.name):
            self._render_student_card(s)

    def _render_student_card(self, s):
        card = tk.Frame(self.scroll_inner, bg="white", pady=10, padx=15)
        card.pack(fill="x", pady=5)
        
        # Layout grid inside card
        card.columnconfigure(1, weight=1)
        
        # 1. Status Indicator
        col = THEME['danger'] if s.is_failing else THEME['success']
        tk.Frame(card, bg=col, width=5).grid(row=0, column=0, rowspan=2, sticky="ns", padx=(0,15))
        
        # 2. Basic Info
        tk.Label(card, text=s.name, font=FONTS['h3'], bg="white", fg=THEME['text_head']).grid(row=0, column=1, sticky="w")
        tk.Label(card, text=f"ID: {s.id}", font=FONTS['small'], bg="white", fg=THEME['text_body']).grid(row=1, column=1, sticky="w")
        
        # 3. Score Info
        score_txt = f"Total: {s.percentage:.1f}%"
        tk.Label(card, text=score_txt, font=FONTS['body'], bg="white").grid(row=0, column=2, sticky="e", padx=20)
        
        # 4. "View Full Report" Button
        # Using lambda to pass the specific student object 's' to the function
        btn = tk.Button(card, text="View Full Report", bg=THEME['bg_dark'], fg="white", 
                        font=("Segoe UI", 9), cursor="hand2",
                        command=lambda st=s: self.open_report_card(st))
        btn.grid(row=1, column=2, sticky="e", padx=20)

    def open_report_card(self, student):
        """Opens a Pop-Up Toplevel Window to look like a physical report card."""
        top = tk.Toplevel(self)
        top.title(f"Report Card - {student.name}")
        top.geometry("500x500")
        top.configure(bg="white")
        
        # Header
        tk.Label(top, text="OFFICIAL ACADEMIC RECORD", font=FONTS['h2'], bg="white", fg=THEME['primary']).pack(pady=20)
        
        # Student Details
        detail_frame = tk.Frame(top, bg="#f8f9fa", padx=20, pady=20)
        detail_frame.pack(fill="x", padx=20)
        tk.Label(detail_frame, text=f"Student Name: {student.name}", font=FONTS['body'], bg="#f8f9fa").pack(anchor="w")
        tk.Label(detail_frame, text=f"Student ID: {student.id}", font=FONTS['body'], bg="#f8f9fa").pack(anchor="w")
        
        # Marks Table
        tk.Label(top, text="Assessment Breakdown", font=FONTS['h3'], bg="white", pady=20).pack(anchor="w", padx=20)
        
        # Helper for drawing a table row
        def row(txt, score, max_score):
            f = tk.Frame(top, bg="white")
            f.pack(fill="x", padx=40, pady=2)
            tk.Label(f, text=txt, bg="white", width=20, anchor="w").pack(side="left")
            tk.Label(f, text=f"{score} / {max_score}", bg="white", font=FONTS['h3']).pack(side="right")

        row("Coursework 1", student.marks['cw1'], 20)
        row("Coursework 2", student.marks['cw2'], 20)
        row("Coursework 3", student.marks['cw3'], 20)
        row("Final Exam", student.marks['exam'], 100)
        
        tk.Frame(top, bg="#ccc", height=1).pack(fill="x", padx=20, pady=20)
        
        # Final Grade
        lbl = tk.Label(top, text=f"Final Grade: {student.grade} ({student.percentage:.1f}%)", 
                       font=FONTS['h2'], bg="white", fg=THEME['text_head'])
        lbl.pack()
        
        if student.is_failing:
            tk.Label(top, text="RESULT: FAIL", fg=THEME['danger'], font=FONTS['h3'], bg="white").pack()
        else:
            tk.Label(top, text="RESULT: PASS", fg=THEME['success'], font=FONTS['h3'], bg="white").pack()


    # =========================================================================
    # CATEGORY 3: ASSESSMENT BREAKDOWN (Coursework Analysis)
    # =========================================================================
    def show_breakdown(self):
        self._clear_view()
        tk.Label(self.scroll_inner, text="Coursework vs Exam Analysis", font=FONTS['h1'], bg=THEME['bg_canvas'], fg=THEME['text_head']).pack(anchor="w", pady=(0,20))
        
        # Explanation text
        tk.Label(self.scroll_inner, text="Compare how students perform in continuous assessment (CW) versus high-pressure exams.", 
                 font=FONTS['body'], bg=THEME['bg_canvas'], fg=THEME['text_body']).pack(anchor="w", pady=(0,20))

        # We'll just list them with dual progress bars
        for s in self.students:
            frame = tk.Frame(self.scroll_inner, bg="white", padx=15, pady=10)
            frame.pack(fill="x", pady=5)
            
            tk.Label(frame, text=s.name, font=FONTS['h3'], bg="white", width=20, anchor="w").pack(side="left")
            
            # Container for bars
            bars = tk.Frame(frame, bg="white")
            bars.pack(side="left", fill="x", expand=True)
            
            # Logic: Scale bar widths
            # CW Total is 60. Exam is 100.
            cw_pct = (s.cw_total / 60)
            ex_pct = (s.marks['exam'] / 100)
            
            self._draw_mini_bar(bars, "CW", cw_pct, THEME['primary'])
            self._draw_mini_bar(bars, "Exam", ex_pct, THEME['accent'])

    def _draw_mini_bar(self, parent, label, pct, color):
        row = tk.Frame(parent, bg="white")
        row.pack(fill="x", pady=2)
        tk.Label(row, text=label, font=FONTS['small'], bg="white", width=5).pack(side="left")
        
        canvas = tk.Canvas(row, bg="#E2E8F0", height=10, highlightthickness=0)
        canvas.pack(side="left", fill="x", expand=True, padx=5)
        
        # Draw the fill
        w = 200 * pct # approximating visual width (responsive is harder in pack)
        # Canvas supports relative width resizing via bind, but keeping it simple/stable here:
        canvas.update() # force update to get width
        width = canvas.winfo_width()
        
        canvas.create_rectangle(0,0, width*pct, 10, fill=color, outline="")
        
        tk.Label(row, text=f"{int(pct*100)}%", font=FONTS['small'], bg="white").pack(side="right")


    # =========================================================================
    # CATEGORY 4: AT-RISK MONITOR (New Feature)
    # =========================================================================
    def show_risk_monitor(self):
        self._clear_view()
        
        # Header styling with Red alert
        head = tk.Frame(self.scroll_inner, bg=THEME['danger'], padx=20, pady=20)
        head.pack(fill="x", pady=(0,20))
        
        tk.Label(head, text="⚠️ AT-RISK MONITOR", font=FONTS['h2'], bg=THEME['danger'], fg="white").pack(anchor="w")
        tk.Label(head, text="Students in this list are scoring below 40% overall.", bg=THEME['danger'], fg="white").pack(anchor="w")
        
        # Filter Logic
        at_risk_students = [s for s in self.students if s.is_failing]
        
        if not at_risk_students:
            tk.Label(self.scroll_inner, text="✅ No students are currently at risk. Great job!", 
                     font=FONTS['h3'], bg=THEME['bg_canvas'], fg=THEME['success']).pack(pady=50)
            return

        for s in at_risk_students:
            card = tk.Frame(self.scroll_inner, bg="white", bd=1, highlightbackground=THEME['danger'], highlightthickness=1, padx=15, pady=15)
            card.pack(fill="x", pady=5)
            
            tk.Label(card, text=s.name, font=FONTS['h3'], bg="white", fg=THEME['danger']).pack(anchor="w")
            
            # Intervention Logic
            advice = "Action Required: Schedule parent meeting."
            if s.marks['exam'] < 30:
                advice = "Action Required: Supplemental Exam Revision classes needed."
            
            tk.Label(card, text=f"Current Grade: {s.grade} ({s.percentage:.1f}%)", bg="white").pack(anchor="w")
            tk.Label(card, text=advice, font=("Segoe UI", 10, "italic"), fg=THEME['text_body'], bg="white").pack(anchor="w", pady=(5,0))


if __name__ == "__main__":
    # Run the application
    app = GradeBookPro()
    app.mainloop()