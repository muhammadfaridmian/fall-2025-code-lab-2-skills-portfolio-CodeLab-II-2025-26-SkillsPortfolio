import tkinter as tk
from tkinter import ttk, messagebox
import os

THEME = {
    'bg_dark': '#1E293B', 'bg_canvas': '#F1F5F9', 'card_white': '#FFFFFF',
    'primary': '#0EA5E9', 'accent': '#6366f1', 'success': '#10B981', 
    'danger': '#EF4444', 'warning': '#F59E0B', 'text_head': '#0F172A', 
    'text_body': '#64748B'
}

class StudentData:
    def __init__(self, line_data):
        parts = line_data.strip().split(',')
        self.id, self.name = parts[0], parts[1]
        self.marks = {f'cw{i+1}': int(parts[i+2]) for i in range(3)}
        self.marks['exam'] = int(parts[5])
        self.calculate_stats()
    
    def calculate_stats(self):
        self.cw_total = sum(self.marks.values()) - self.marks['exam']
        self.overall_score = self.cw_total + self.marks['exam']
        self.percentage = (self.overall_score / 160) * 100
        self.grade = 'A' if self.percentage >= 70 else 'B' if self.percentage >= 60 else 'C' if self.percentage >= 50 else 'D' if self.percentage >= 40 else 'F'
        self.is_failing = self.percentage < 40
    
    def to_file_string(self):
        return f"{self.id},{self.name},{self.marks['cw1']},{self.marks['cw2']},{self.marks['cw3']},{self.marks['exam']}"

class ModernButton(tk.Button):
    def __init__(self, master, text, command, **kwargs):
        super().__init__(master, text=text, font=("Arial", 11), bg=THEME['bg_dark'], 
                         fg="white", bd=0, anchor="w", padx=20, pady=12, 
                         cursor="hand2", command=command, **kwargs)
        self.bind("<Enter>", lambda e: self.config(bg='#334155'))
        self.bind("<Leave>", lambda e: self.config(bg=THEME['bg_dark']))

class EduAnalytics(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GradeBook Pro - Analytics Dashboard")
        self.geometry("1200x750")
        self.state('zoomed')
        self.configure(bg=THEME['bg_canvas'])
        
        self.students = []
        self._setup_data()
        self._create_ui()
        self.show_dashboard()

    def _setup_data(self):
        sample_data = """10
1345,John Curry,8,15,7,45
2345,Sam Sturtivant,14,15,14,77
9876,Lee Scott,17,11,16,99
3724,Matt Thompson,19,11,15,81
1212,Ron Herrema,14,17,18,66
8439,Jake Hobbs,10,11,10,43
2344,Jo Hyde,6,15,10,55
9384,Gareth Southgate,1,1,1,2
8327,Alan Shearer,20,20,20,100
2983,Les Ferdinand,15,17,18,92"""
        
        if not os.path.exists("studentMarks.txt"):
            with open("studentMarks.txt", "w") as f:
                f.write(sample_data)
        
        with open("studentMarks.txt", "r") as f:
            lines = f.readlines()
            if len(lines) > 1:
                self.students = [StudentData(line) for line in lines[1:] if line.strip()]
            else:
                with open("studentMarks.txt", "w") as f:
                    f.write(sample_data)
                self.students = [StudentData(line) for line in sample_data.split('\n')[1:] if line.strip()]

    def _save_data(self):
        try:
            with open("studentMarks.txt", "w") as f:
                f.write(f"{len(self.students)}\n")
                f.write("\n".join(s.to_file_string() for s in self.students))
            return True
        except:
            messagebox.showerror("Error", "Failed to save data")
            return False

    def _create_ui(self):
        
        sidebar = tk.Frame(self, bg=THEME['bg_dark'], width=280)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Brand header
        header_frame = tk.Frame(sidebar, bg=THEME['bg_dark'])
        header_frame.pack(fill="x", pady=30)
        tk.Label(header_frame, text="EDU", font=("Arial", 28, "bold"), 
                bg=THEME['bg_dark'], fg=THEME['primary']).pack()
        tk.Label(header_frame, text="ANALYTICS", font=("Arial", 28, "bold"), 
                bg=THEME['bg_dark'], fg="white").pack()
        
        # Navigation menu
        menu_items = [
            ("📊 Executive Dashboard", self.show_dashboard),
            ("👥 Student Registry", self.show_students),
            ("📈 Performance Analysis", self.show_analysis),
            ("⚠️ At-Risk Monitor", self.show_risk),
            ("🔢 Sort Records", self.show_sort),
            ("➕ Add Student", self.show_add),
            ("🗑️ Delete Student", self.show_delete),
            ("✏️ Update Records", self.show_update)
        ]
        
        for text, command in menu_items:
            ModernButton(sidebar, text, command).pack(fill="x", pady=2)
        
        # Footer
        tk.Frame(sidebar, height=20, bg=THEME['bg_dark']).pack(side="bottom")
        tk.Label(sidebar, text="v2.0 Professional", font=("Arial", 9), 
                bg=THEME['bg_dark'], fg=THEME['text_body']).pack(side="bottom", pady=10)

        # Main content area with scrollbar
        self.main_container = tk.Frame(self, bg=THEME['bg_canvas'])
        self.main_container.pack(side="right", fill="both", expand=True)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self.main_container, bg=THEME['bg_canvas'], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=THEME['bg_canvas'])
        
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw", width=1200)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def clear_main(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

    def create_card(self, parent, title, value, color, width=200):
        card = tk.Frame(parent, bg="white", padx=20, pady=20)
        card.pack(side="left", expand=True, fill="x", padx=10)
        
        # Colored accent bar
        tk.Frame(card, bg=color, height=4).pack(fill="x", pady=(0,12))
        
        # Content
        tk.Label(card, text=title.upper(), font=("Arial", 10), 
                bg="white", fg=THEME['text_body']).pack(anchor="w")
        tk.Label(card, text=value, font=("Arial", 24, "bold"), 
                bg="white", fg=THEME['text_head']).pack(anchor="w")
        
        return card

    def show_dashboard(self):
        self.clear_main()
        tk.Label(self.scroll_frame, text="Executive Dashboard", font=("Arial", 28, "bold"), 
                bg=THEME['bg_canvas'], fg=THEME['text_head']).pack(anchor="w", pady=(0, 20))
        
        # Statistics cards
        stats_frame = tk.Frame(self.scroll_frame, bg=THEME['bg_canvas'])
        stats_frame.pack(fill="x", pady=30)
        
        if self.students:
            avg_score = sum(s.percentage for s in self.students) / len(self.students)
            pass_count = sum(1 for s in self.students if not s.is_failing)
        else:
            avg_score = 0
            pass_count = 0
        
        self.create_card(stats_frame, "Class Average", f"{avg_score:.1f}%", THEME['primary'])
        self.create_card(stats_frame, "Total Students", str(len(self.students)), THEME['warning'])
        self.create_card(stats_frame, "Passing Rate", f"{pass_count}/{len(self.students)}", THEME['success'])
        
        # Visualizations
        viz_frame = tk.Frame(self.scroll_frame, bg=THEME['bg_canvas'])
        viz_frame.pack(fill="x", pady=20)
        
        # Grade distribution chart
        chart_card = tk.Frame(viz_frame, bg="white", padx=25, pady=25)
        chart_card.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(chart_card, text="Grade Distribution", font=("Arial", 14, "bold"), 
                bg="white").pack(anchor="w")
        
        canvas = tk.Canvas(chart_card, bg="white", height=180, highlightthickness=0)
        canvas.pack(fill="x", pady=15)
        
        grades = {'A':0, 'B':0, 'C':0, 'D':0, 'F':0}
        for s in self.students: 
            grades[s.grade] += 1
        max_count = max(grades.values()) or 1
        
        for i, (grade, count) in enumerate(grades.items()):
            x, width = 40 + i*80, 50
            height = (count / max_count) * 120
            color = THEME['success'] if grade in ['A','B'] else THEME['warning'] if grade == 'C' else THEME['danger']
            
            canvas.create_rectangle(x, 150, x+width, 150-height, fill=color, outline="")
            canvas.create_text(x+width/2, 165, text=grade, font=("Arial", 11, "bold"))
            canvas.create_text(x+width/2, 150-height-10, text=str(count), font=("Arial", 10))

        # Pass/Fail pie chart
        pie_card = tk.Frame(viz_frame, bg="white", padx=25, pady=25)
        pie_card.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(pie_card, text="Pass/Fail Ratio", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
        
        pie_canvas = tk.Canvas(pie_card, bg="white", height=180, width=180, highlightthickness=0)
        pie_canvas.pack(pady=15)
        
        pass_count = sum(1 for s in self.students if not s.is_failing)
        fail_count = len(self.students) - pass_count
        
        if self.students:
            pass_angle = (pass_count / len(self.students)) * 360
            pie_canvas.create_arc(20, 20, 160, 160, start=0, extent=pass_angle, 
                                 fill=THEME['success'], outline="")
            pie_canvas.create_arc(20, 20, 160, 160, start=pass_angle, extent=360-pass_angle, 
                                 fill=THEME['danger'], outline="")
        
        tk.Label(pie_card, text=f"Pass: {pass_count} | Fail: {fail_count}", 
                font=("Arial", 11), bg="white").pack()

    def show_students(self):
        self.clear_main()
        tk.Label(self.scroll_frame, text="Student Registry", font=("Arial", 28, "bold"), 
                bg=THEME['bg_canvas']).pack(anchor="w", pady=(0, 20))
        
        # Search bar
        search_frame = tk.Frame(self.scroll_frame, bg=THEME['bg_canvas'])
        search_frame.pack(fill="x", pady=20)
        tk.Entry(search_frame, font=("Arial", 12), width=30).pack(side="right", padx=10)
        tk.Label(search_frame, text="Search:", font=("Arial", 11), 
                bg=THEME['bg_canvas']).pack(side="right")
        
        # Student cards
        for student in sorted(self.students, key=lambda x: x.name):
            card = tk.Frame(self.scroll_frame, bg="white", pady=12, padx=20)
            card.pack(fill="x", pady=6)
            
            # Status indicator
            status_color = THEME['danger'] if student.is_failing else THEME['success']
            tk.Frame(card, bg=status_color, width=6).pack(side="left", fill="y", padx=(0,15))
            
            # Student info
            info_frame = tk.Frame(card, bg="white")
            info_frame.pack(side="left", fill="x", expand=True)
            
            tk.Label(info_frame, text=student.name, font=("Arial", 13, "bold"), 
                    bg="white").pack(anchor="w")
            tk.Label(info_frame, text=f"ID: {student.id} | Grade: {student.grade}", 
                    font=("Arial", 11), bg="white", fg=THEME['text_body']).pack(anchor="w")
            
            # Performance info
            perf_frame = tk.Frame(card, bg="white")
            perf_frame.pack(side="right")
            tk.Label(perf_frame, text=f"{student.percentage:.1f}%", 
                    font=("Arial", 14, "bold"), bg="white").pack()
            
            # Button linked to the report method
            tk.Button(perf_frame, text="View Report", font=("Arial", 9),
                      bg=THEME['primary'], fg="white", cursor="hand2",
                      command=lambda s=student: self.show_student_report(s)).pack()

    def show_student_report(self, student):
        """Create a popup window showing specific student details"""
        report = tk.Toplevel(self)
        report.title(f"Report: {student.name}")
        # FIX: Increased height from 500 to 600 to ensure the percentage is visible
        report.geometry("400x600") 
        report.configure(bg='white')

        # Report Header
        tk.Label(report, text=student.name, font=("Arial", 18, "bold"), 
                 bg='white', fg=THEME['text_head']).pack(pady=(20, 5))
        tk.Label(report, text=f"ID: {student.id}", font=("Arial", 11), 
                 bg='white', fg=THEME['text_body']).pack(pady=(0, 20))

        # Content Container
        content = tk.Frame(report, bg='white', padx=40)
        content.pack(fill='both', expand=True)

        # Helper function for rows
        def add_row(label, value, is_bold=False):
            font = ("Arial", 11, "bold") if is_bold else ("Arial", 11)
            frame = tk.Frame(content, bg='white', pady=5)
            frame.pack(fill='x')
            tk.Label(frame, text=label, font=font, bg='white', fg=THEME['text_head']).pack(side='left')
            tk.Label(frame, text=value, font=font, bg='white', 
                     fg=THEME['primary'] if is_bold else THEME['text_body']).pack(side='right')
            tk.Frame(content, bg=THEME['bg_canvas'], height=1).pack(fill='x', pady=2)

        # Coursework Section
        tk.Label(content, text="COURSEWORK", font=("Arial", 10, "bold"), 
                 fg=THEME['text_body'], bg='white').pack(anchor='w', pady=(10, 10))
        add_row("Assignment 1", str(student.marks['cw1']))
        add_row("Assignment 2", str(student.marks['cw2']))
        add_row("Assignment 3", str(student.marks['cw3']))
        add_row("CW Total", f"{student.cw_total}/60", True)

        # Exam Section
        tk.Label(content, text="EXAMINATION", font=("Arial", 10, "bold"), 
                 fg=THEME['text_body'], bg='white').pack(anchor='w', pady=(20, 10))
        add_row("Final Exam", f"{student.marks['exam']}/100", True)

        # Final Result Section
        tk.Label(content, text="FINAL RESULT", font=("Arial", 10, "bold"), 
                 fg=THEME['text_body'], bg='white').pack(anchor='w', pady=(20, 10))
        
        res_frame = tk.Frame(content, bg=THEME['bg_canvas'], padx=20, pady=15)
        res_frame.pack(fill='x', pady=10)
        
        grade_color = THEME['success'] if student.grade in ['A','B'] else THEME['warning'] if student.grade == 'C' else THEME['danger']
        
        # Display the percentage prominently
        tk.Label(res_frame, text=f"{student.percentage:.1f}%", font=("Arial", 24, "bold"), 
                 bg=THEME['bg_canvas'], fg=THEME['text_head']).pack(expand=True)
        tk.Label(res_frame, text=f"Grade {student.grade}", font=("Arial", 14, "bold"), 
                 bg=THEME['bg_canvas'], fg=grade_color).pack(expand=True)

    def show_analysis(self):
        self.clear_main()
        tk.Label(self.scroll_frame, text="Performance Analysis", font=("Arial", 28, "bold"), 
                bg=THEME['bg_canvas']).pack(anchor="w", pady=(0, 20))
        
        tk.Label(self.scroll_frame, text="Coursework vs Exam Performance Comparison", 
                font=("Arial", 12), bg=THEME['bg_canvas'], fg=THEME['text_body']).pack(anchor="w", pady=(0,20))
        
        for student in self.students:
            frame = tk.Frame(self.scroll_frame, bg="white", padx=20, pady=15)
            frame.pack(fill="x", pady=8)
            
            tk.Label(frame, text=student.name, font=("Arial", 12, "bold"), 
                    bg="white", width=18, anchor="w").pack(side="left")
            
            bars_frame = tk.Frame(frame, bg="white")
            bars_frame.pack(side="left", fill="x", expand=True)
            
            for label, percentage, color in [
                ("Coursework", student.cw_total/60, THEME['primary']),
                ("Final Exam", student.marks['exam']/100, THEME['accent'])
            ]:
                row = tk.Frame(bars_frame, bg="white")
                row.pack(fill="x", pady=3)
                
                tk.Label(row, text=label, font=("Arial", 10), bg="white", width=12).pack(side="left")
                
                # Fixed bar canvas with proper width calculation
                bar_canvas = tk.Canvas(row, bg="#E2E8F0", height=14, width=200, highlightthickness=0)
                bar_canvas.pack(side="left", padx=8)
                
                # Calculate actual pixel width based on percentage
                bar_width = int(200 * percentage)
                bar_canvas.create_rectangle(0, 0, bar_width, 14, fill=color, outline="")
                
                tk.Label(row, text=f"{int(percentage*100)}%", font=("Arial", 10), 
                        bg="white").pack(side="right")

    def show_risk(self):
        self.clear_main()
        tk.Label(self.scroll_frame, text="At-Risk Students", font=("Arial", 28, "bold"), 
                bg=THEME['bg_canvas']).pack(anchor="w", pady=(0, 20))
        
        at_risk = [s for s in self.students if s.is_failing]
        
        if not at_risk:
            success_frame = tk.Frame(self.scroll_frame, bg=THEME['success'], padx=30, pady=25)
            success_frame.pack(fill="x", pady=30)
            tk.Label(success_frame, text="✅ ALL STUDENTS MEETING EXPECTATIONS", 
                    font=("Arial", 16, "bold"), bg=THEME['success'], fg="white").pack()
            return
        
        alert_header = tk.Frame(self.scroll_frame, bg=THEME['danger'], padx=25, pady=20)
        alert_header.pack(fill="x", pady=20)
        tk.Label(alert_header, text="⚠️ INTERVENTION REQUIRED", font=("Arial", 16, "bold"), 
                bg=THEME['danger'], fg="white").pack(anchor="w")
        tk.Label(alert_header, text="Students below 40% overall score", 
                font=("Arial", 12), bg=THEME['danger'], fg="white").pack(anchor="w")
        
        for student in at_risk:
            card = tk.Frame(self.scroll_frame, bg="white", padx=20, pady=18, 
                           highlightbackground=THEME['danger'], highlightthickness=2)
            card.pack(fill="x", pady=8)
            
            tk.Label(card, text=student.name, font=("Arial", 14, "bold"), 
                    bg="white", fg=THEME['danger']).pack(anchor="w")
            
            score_text = f"Current Score: {student.percentage:.1f}% | Grade: {student.grade}"
            tk.Label(card, text=score_text, font=("Arial", 11), bg="white").pack(anchor="w")
            
            advice = "Schedule parent meeting and extra classes" if student.marks['exam'] < 30 else "Provide additional academic support"
            tk.Label(card, text=advice, font=("Arial", 10, "italic"), 
                    bg="white", fg=THEME['text_body']).pack(anchor="w", pady=(5,0))

    def show_sort(self):
        self.clear_main()
        tk.Label(self.scroll_frame, text="Sort Student Records", font=("Arial", 28, "bold"), 
                bg=THEME['bg_canvas']).pack(anchor="w", pady=(0, 20))
        
        # Sort controls - Better organized layout
        control_card = tk.Frame(self.scroll_frame, bg="white", padx=30, pady=25)
        control_card.pack(fill="x", pady=20)
        
        tk.Label(control_card, text="Sort Options", font=("Arial", 16, "bold"), 
                bg="white", fg=THEME['text_head']).pack(anchor="w", pady=(0,20))
        
        # Sort criteria in a clean grid layout
        criteria_container = tk.Frame(control_card, bg="white")
        criteria_container.pack(fill="x", pady=10)
        
        # Create organized sections for each sort type
        sort_sections = [
            ("📝 Name", "name", THEME['primary']),
            ("📊 Percentage", "percentage", THEME['success']),
            ("🎓 Grade", "grade", THEME['warning']),
            ("🔢 Student ID", "id", THEME['accent'])
        ]
        
        for i, (title, key, color) in enumerate(sort_sections):
            section_frame = tk.Frame(criteria_container, bg="white")
            section_frame.pack(side="left", fill="x", expand=True, padx=5)
            
            # Section title
            tk.Label(section_frame, text=title, font=("Arial", 12, "bold"), 
                    bg="white", fg=THEME['text_head']).pack(anchor="w", pady=(0,8))
            
            # Sort buttons for this section
            btn_frame = tk.Frame(section_frame, bg="white")
            btn_frame.pack(fill="x")
            
            for order, order_text in [("asc", "Ascending"), ("desc", "Descending")]:
                btn = tk.Button(btn_frame, text=order_text, font=("Arial", 10),
                              bg=color, fg="white", padx=15, pady=6, width=12,
                              command=lambda k=key, o=order: self.display_sorted(k, o))
                btn.pack(fill="x", pady=3)
        
        # Results area
        self.results_frame = tk.Frame(self.scroll_frame, bg=THEME['bg_canvas'])
        self.results_frame.pack(fill="both", expand=True, pady=20)
        self.display_sorted('name', 'asc')

    def display_sorted(self, key, order):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        reverse = order == 'desc'
        
        if key == 'name':
            sorted_students = sorted(self.students, key=lambda x: x.name, reverse=reverse)
        elif key == 'percentage':
            sorted_students = sorted(self.students, key=lambda x: x.percentage, reverse=reverse)
        elif key == 'grade':
            grade_order = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'F': 4}
            sorted_students = sorted(self.students, key=lambda x: grade_order[x.grade], reverse=reverse)
        else:  # id
            sorted_students = sorted(self.students, key=lambda x: x.id, reverse=reverse)
        
        # Header with current sort info
        header_card = tk.Frame(self.results_frame, bg="white", padx=25, pady=20)
        header_card.pack(fill="x", pady=(0, 15))
        
        sort_display = f"{key.title()} - {order.title()}ending"
        tk.Label(header_card, text=f"Sorted by: {sort_display}", 
                font=("Arial", 14, "bold"), bg="white", fg=THEME['text_head']).pack(anchor="w")
        tk.Label(header_card, text=f"Showing {len(sorted_students)} students", 
                font=("Arial", 11), bg="white", fg=THEME['text_body']).pack(anchor="w")
        
        # Table container - Using grid for perfect alignment
        table_container = tk.Frame(self.results_frame, bg="white")
        table_container.pack(fill="both", expand=True)
        
        # Table header using grid
        header_frame = tk.Frame(table_container, bg=THEME['primary'])
        header_frame.pack(fill="x", padx=20)
        
        # Define columns with exact widths and alignment
        columns = [
            {"name": "Student Name", "width": 250, "anchor": "w"},
            {"name": "ID", "width": 100, "anchor": "w"},
            {"name": "CW Total", "width": 100, "anchor": "center"},
            {"name": "Exam", "width": 80, "anchor": "center"},
            {"name": "Overall %", "width": 100, "anchor": "center"},
            {"name": "Grade", "width": 80, "anchor": "center"}
        ]
        
        # Create header labels using grid
        for col_idx, col in enumerate(columns):
            header_label = tk.Label(header_frame, text=col["name"], font=("Arial", 12, "bold"), 
                                  bg=THEME['primary'], fg="white", width=col["width"]//8,
                                  anchor=col["anchor"])
            header_label.grid(row=0, column=col_idx, padx=2, pady=12, sticky="ew")
        
        # Configure header grid columns to have equal weight
        for col_idx in range(len(columns)):
            header_frame.grid_columnconfigure(col_idx, weight=1)
        
        # Student rows using grid for perfect alignment
        for i, student in enumerate(sorted_students):
            row_color = "white" if i % 2 == 0 else "#f8fafc"
            row_frame = tk.Frame(table_container, bg=row_color)
            row_frame.pack(fill="x", padx=20)
            
            # Name
            name_label = tk.Label(row_frame, text=student.name, font=("Arial", 11), 
                                 bg=row_color, width=columns[0]["width"]//8, anchor="w")
            name_label.grid(row=0, column=0, padx=2, pady=10, sticky="w")
            
            # ID
            id_label = tk.Label(row_frame, text=student.id, font=("Arial", 11), 
                              bg=row_color, width=columns[1]["width"]//8, anchor="w")
            id_label.grid(row=0, column=1, padx=2, pady=10, sticky="w")
            
            # Coursework total
            cw_label = tk.Label(row_frame, text=str(student.cw_total), font=("Arial", 11), 
                               bg=row_color, width=columns[2]["width"]//8, anchor="center")
            cw_label.grid(row=0, column=2, padx=2, pady=10)
            
            # Exam mark
            exam_label = tk.Label(row_frame, text=str(student.marks['exam']), font=("Arial", 11), 
                                 bg=row_color, width=columns[3]["width"]//8, anchor="center")
            exam_label.grid(row=0, column=3, padx=2, pady=10)
            
            # Percentage with color coding
            percentage_color = THEME['success'] if student.percentage >= 60 else THEME['warning'] if student.percentage >= 40 else THEME['danger']
            perc_label = tk.Label(row_frame, text=f"{student.percentage:.1f}%", 
                                 font=("Arial", 11, "bold"), bg=row_color, fg=percentage_color,
                                 width=columns[4]["width"]//8, anchor="center")
            perc_label.grid(row=0, column=4, padx=2, pady=10)
            
            # Grade with color coding
            grade_color = THEME['success'] if student.grade in ['A','B'] else THEME['warning'] if student.grade == 'C' else THEME['danger']
            grade_label = tk.Label(row_frame, text=student.grade, font=("Arial", 11, "bold"), 
                                  bg=row_color, fg=grade_color, width=columns[5]["width"]//8, anchor="center")
            grade_label.grid(row=0, column=5, padx=2, pady=10)
            
            # Configure row grid columns to match header
            for col_idx in range(len(columns)):
                row_frame.grid_columnconfigure(col_idx, weight=1)

    def show_add(self):
        self.clear_main()
        tk.Label(self.scroll_frame, text="Add New Student", font=("Arial", 28, "bold"), 
                bg=THEME['bg_canvas']).pack(anchor="w", pady=(0, 20))
        
        form = tk.Frame(self.scroll_frame, bg="white", padx=30, pady=30)
        form.pack(fill="x", pady=20)
        
        fields = ["ID", "Name", "CW1", "CW2", "CW3", "Exam"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(form, text=field, font=("Arial", 11), bg="white").grid(row=i, column=0, sticky="w", pady=8)
            entry = tk.Entry(form, font=("Arial", 11), width=25)
            entry.grid(row=i, column=1, sticky="w", pady=8, padx=10)
            self.entries[field] = entry
        
        tk.Button(form, text="➕ Add Student", font=("Arial", 12), bg=THEME['success'], fg="white",
                 command=self.add_student).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def add_student(self):
        try:
            data = {field: self.entries[field].get().strip() for field in ["ID", "Name", "CW1", "CW2", "CW3", "Exam"]}
            
            if any(not value for value in data.values()):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            if any(s.id == data["ID"] for s in self.students):
                messagebox.showerror("Error", "ID already exists")
                return
            
            line = f"{data['ID']},{data['Name']},{data['CW1']},{data['CW2']},{data['CW3']},{data['Exam']}"
            self.students.append(StudentData(line))
            self._save_data()
            messagebox.showinfo("Success", "Student added!")
            for entry in self.entries.values():
                entry.delete(0, tk.END)
                
        except ValueError:
            messagebox.showerror("Error", "Invalid marks")

    def show_delete(self):
        self.clear_main()
        tk.Label(self.scroll_frame, text="Delete Student", font=("Arial", 28, "bold"), 
                bg=THEME['bg_canvas']).pack(anchor="w", pady=(0, 20))
        
        for s in self.students:
            frame = tk.Frame(self.scroll_frame, bg="white", pady=8)
            frame.pack(fill="x", pady=2)
            
            tk.Label(frame, text=f"{s.name} (ID: {s.id})", font=("Arial", 11), bg="white").pack(side="left")
            tk.Button(frame, text="🗑️ Delete", font=("Arial", 9), bg=THEME['danger'], fg="white",
                     command=lambda st=s: self.delete_student(st)).pack(side="right")

    def delete_student(self, student):
        if messagebox.askyesno("Confirm", f"Delete {student.name}?"):
            self.students = [s for s in self.students if s.id != student.id]
            self._save_data()
            self.show_delete()

    def show_update(self):
        self.clear_main()
        tk.Label(self.scroll_frame, text="Update Student", font=("Arial", 28, "bold"), 
                bg=THEME['bg_canvas']).pack(anchor="w", pady=(0, 20))
        
        for s in self.students:
            frame = tk.Frame(self.scroll_frame, bg="white", pady=8)
            frame.pack(fill="x", pady=2)
            
            tk.Label(frame, text=f"{s.name} (ID: {s.id}) - {s.grade}", font=("Arial", 11), bg="white").pack(side="left")
            tk.Button(frame, text="✏️ Update", font=("Arial", 9), bg=THEME['warning'], fg="white",
                     command=lambda st=s: self.update_student(st)).pack(side="right")

    def update_student(self, student):
        popup = tk.Toplevel(self)
        popup.title(f"Update {student.name}")
        popup.geometry("300x400")
        
        tk.Label(popup, text=f"Update {student.name}", font=("Arial", 16, "bold")).pack(pady=20)
        
        form = tk.Frame(popup)
        form.pack(fill="both", expand=True, padx=20, pady=10)
        
        fields = [("Name", student.name), ("CW1", student.marks['cw1']), 
                 ("CW2", student.marks['cw2']), ("CW3", student.marks['cw3']), 
                 ("Exam", student.marks['exam'])]
        
        entries = {}
        for i, (label, value) in enumerate(fields):
            tk.Label(form, text=label).grid(row=i, column=0, sticky="w", pady=8)
            entry = tk.Entry(form)
            entry.insert(0, str(value))
            entry.grid(row=i, column=1, sticky="w", pady=8, padx=10)
            entries[label] = entry
        
        def save_update():
            try:
                student.name = entries['Name'].get()
                student.marks['cw1'] = int(entries['CW1'].get())
                student.marks['cw2'] = int(entries['CW2'].get())
                student.marks['cw3'] = int(entries['CW3'].get())
                student.marks['exam'] = int(entries['Exam'].get())
                
                # Recalculate
                student.calculate_stats()
                
                self._save_data()
                messagebox.showinfo("Success", "Updated!")
                popup.destroy()
                self.show_update()
                
            except ValueError:
                messagebox.showerror("Error", "Invalid marks")
        
        tk.Button(form, text="💾 Save", bg=THEME['success'], fg="white", command=save_update).grid(row=len(fields), column=0, columnspan=2, pady=20)

if __name__ == "__main__":
    app = EduAnalytics()
    app.mainloop()