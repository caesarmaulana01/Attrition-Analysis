import joblib
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import warnings

# Suppress joblib warning
warnings.filterwarnings("ignore", category=UserWarning)

class EmployeeAttritionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prediksi Attrition Pegawai")
        self.root.geometry("900x700")
        
        # Initialize employee_data dictionary
        self.employee_data = {}
        
        # Load model
        try:
            self.model = joblib.load("LogisticRegression_best_model.pkl")
            # Mendapatkan nama fitur dari model
            if hasattr(self.model, 'feature_names_in_'):
                self.feature_names = self.model.feature_names_in_
            else:
                # Fallback jika model tidak menyimpan nama fitur
                self.feature_names = [
                    'Age', 'DailyRate', 'DistanceFromHome', 'Education', 'EnvironmentSatisfaction',
                    'Gender', 'HourlyRate', 'JobInvolvement', 'JobLevel', 'JobSatisfaction',
                    'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 'OverTime',
                    'PercentSalaryHike', 'PerformanceRating', 'RelationshipSatisfaction',
                    'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear',
                    'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole',
                    'YearsSinceLastPromotion', 'YearsWithCurrManager',
                    'BusinessTravel_Travel_Frequently', 'BusinessTravel_Travel_Rarely',
                    'Department_Research & Development', 'Department_Sales',
                    'EducationField_Life Sciences', 'EducationField_Marketing',
                    'EducationField_Medical', 'EducationField_Other',
                    'EducationField_Technical Degree', 'JobRole_Human Resources',
                    'JobRole_Laboratory Technician', 'JobRole_Manager',
                    'JobRole_Manufacturing Director', 'JobRole_Research Director',
                    'JobRole_Research Scientist', 'JobRole_Sales Executive',
                    'JobRole_Sales Representative', 'MaritalStatus_Married',
                    'MaritalStatus_Single'
                ]
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat model: {e}")
            self.root.destroy()
            return
        
        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_numerical_tab()
        self.create_categorical_tab()
        self.create_result_tab()
        
        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        self.predict_btn = ttk.Button(self.button_frame, text="Prediksi", command=self.predict)
        self.predict_btn.pack(side=tk.RIGHT, padx=5)
        
        self.reset_btn = ttk.Button(self.button_frame, text="Reset", command=self.reset_form)
        self.reset_btn.pack(side=tk.RIGHT, padx=5)

    def create_numerical_tab(self):
        """Tab untuk input numerik"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Data Numerik")
        
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Numerical inputs
        numerical_fields = [
            ("Age", "Usia (tahun)", 18, 70),
            ("DailyRate", "Daily Rate", 0, None),
            ("DistanceFromHome", "Jarak dari rumah (km)", 0, None),
            ("Education", "Tingkat pendidikan (1-5)", 1, 5),
            ("EnvironmentSatisfaction", "Kepuasan lingkungan kerja (1-4)", 1, 4),
            ("Gender", "Gender (0=Female, 1=Male)", 0, 1),
            ("HourlyRate", "Hourly Rate", 0, None),
            ("JobInvolvement", "Keterlibatan pekerjaan (1-4)", 1, 4),
            ("JobLevel", "Level pekerjaan (1-5)", 1, 5),
            ("JobSatisfaction", "Kepuasan pekerjaan (1-4)", 1, 4),
            ("MonthlyIncome", "Pendapatan bulanan", 0, None),
            ("MonthlyRate", "Monthly Rate", 0, None),
            ("NumCompaniesWorked", "Jumlah perusahaan sebelumnya", 0, None),
            ("OverTime", "Lembur (0=Tidak, 1=Ya)", 0, 1),
            ("PercentSalaryHike", "Persentase kenaikan gaji", 0, None),
            ("PerformanceRating", "Rating performa (1-4)", 1, 4),
            ("RelationshipSatisfaction", "Kepuasan hubungan (1-4)", 1, 4),
            ("StockOptionLevel", "Level stock option (0-3)", 0, 3),
            ("TotalWorkingYears", "Total tahun bekerja", 0, None),
            ("TrainingTimesLastYear", "Frekuensi training tahun lalu", 0, None),
            ("WorkLifeBalance", "Keseimbangan kerja-hidup (1-4)", 1, 4),
            ("YearsAtCompany", "Tahun bekerja di perusahaan", 0, None),
            ("YearsInCurrentRole", "Tahun di posisi saat ini", 0, None),
            ("YearsSinceLastPromotion", "Tahun sejak promosi terakhir", 0, None),
            ("YearsWithCurrManager", "Tahun dengan manager saat ini", 0, None)
        ]
        
        for i, (field, label, min_val, max_val) in enumerate(numerical_fields):
            frame = ttk.Frame(scrollable_frame, padding="5")
            frame.grid(row=i, column=0, sticky="ew")
            
            lbl = ttk.Label(frame, text=label, width=30, anchor="e")
            lbl.pack(side=tk.LEFT, padx=5)
            
            entry = ttk.Entry(frame, width=15)
            entry.pack(side=tk.LEFT, padx=5)
            
            # Store reference to entry widget
            self.employee_data[field] = entry
    
    def create_categorical_tab(self):
        """Tab untuk input kategori"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Data Kategori")
        
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Categorical groups - disesuaikan dengan nama fitur saat training
        category_groups = [
            ("BusinessTravel", "Business Travel", ["Travel_Frequently", "Travel_Rarely"]),
            ("Department", "Department", ["Research & Development", "Sales"]),
            ("EducationField", "Education Field", ["Life Sciences", "Marketing", "Medical", "Other", "Technical Degree"]),
            ("JobRole", "Job Role", [
                "Human Resources", "Laboratory Technician", "Manager", 
                "Manufacturing Director", "Research Director", "Research Scientist",
                "Sales Executive", "Sales Representative"
            ]),
            ("MaritalStatus", "Marital Status", ["Married", "Single"])
        ]
        
        row = 0
        for prefix, group_name, options in category_groups:
            group_frame = ttk.LabelFrame(scrollable_frame, text=group_name, padding="10")
            group_frame.grid(row=row, column=0, sticky="ew", pady=5)
            row += 1
            
            # Create radio buttons for each option
            selected_var = tk.StringVar()
            for i, option in enumerate(options):
                # Create column name sesuai dengan yang digunakan saat training
                col_name = f"{prefix}_{option.replace(' ', '_')}"
                
                rb = ttk.Radiobutton(
                    group_frame, 
                    text=option, 
                    variable=selected_var,
                    value=col_name
                )
                rb.grid(row=i, column=0, sticky="w", padx=5, pady=2)
                
                # Store reference to radio button variable
                self.employee_data[col_name] = selected_var
    
    def create_result_tab(self):
        """Tab untuk menampilkan hasil prediksi"""
        self.result_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.result_tab, text="Hasil Prediksi")
        
        # Prediction result
        self.result_frame = ttk.LabelFrame(self.result_tab, text="Hasil Prediksi", padding="20")
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.prediction_label = ttk.Label(
            self.result_frame, 
            text="Prediksi: -", 
            font=('Helvetica', 12, 'bold')
        )
        self.prediction_label.pack(pady=5)
        
        self.probability_label = ttk.Label(
            self.result_frame, 
            text="Probabilitas: -", 
            font=('Helvetica', 10)
        )
        self.probability_label.pack(pady=5)
        
        self.recommendation_label = ttk.Label(
            self.result_frame, 
            text="Rekomendasi: -", 
            font=('Helvetica', 10, 'italic')
        )
        self.recommendation_label.pack(pady=5)
    
    def collect_input_data(self):
        """Mengumpulkan semua data input"""
        data = {}
        
        # Numerical data
        for field, widget in self.employee_data.items():
            if isinstance(widget, ttk.Entry):
                value = widget.get()
                try:
                    data[field] = float(value) if value else 0.0
                except ValueError:
                    messagebox.showerror("Error", f"Nilai tidak valid untuk {field}")
                    return None
        
        # Categorical data (radio buttons)
        for field, var in self.employee_data.items():
            if isinstance(var, tk.StringVar):
                selected = var.get()
                # Set 1.0 for selected option, 0.0 for others in the same group
                data[field] = 1.0 if field == selected else 0.0
        
        # Pastikan semua fitur yang diperlukan ada
        for feature in self.feature_names:
            if feature not in data:
                data[feature] = 0.0  # Isi dengan default 0 jika tidak ada
        
        return data
    
    def predict(self):
        """Melakukan prediksi berdasarkan input"""
        input_data = self.collect_input_data()
        if input_data is None:
            return
        
        try:
            # Convert to DataFrame dengan urutan kolom yang benar
            df = pd.DataFrame([input_data])[self.feature_names]
            
            # Make prediction
            prediction = self.model.predict(df)
            prediction_proba = self.model.predict_proba(df)
            
            # Update result tab
            self.notebook.select(self.result_tab)
            
            self.prediction_label.config(
                text=f"Prediksi: {'Ya' if prediction[0] == 1 else 'Tidak'} (Attrition)",
                foreground="red" if prediction[0] == 1 else "green"
            )
            
            self.probability_label.config(
                text=f"Probabilitas:\n- Tidak Attrition: {prediction_proba[0][0]*100:.2f}%\n- Attrition: {prediction_proba[0][1]*100:.2f}%"
            )
            
            if prediction[0] == 1:
                self.recommendation_label.config(
                    text="Rekomendasi: Pegawai berisiko tinggi untuk attrition. Disarankan untuk melakukan intervensi HR.",
                    foreground="red"
                )
            else:
                self.recommendation_label.config(
                    text="Rekomendasi: Pegawai berisiko rendah untuk attrition.",
                    foreground="green"
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat prediksi: {e}")
    
    def reset_form(self):
        """Reset semua input"""
        for widget in self.employee_data.values():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.StringVar):
                widget.set("")
        
        # Reset result display
        self.prediction_label.config(text="Prediksi: -", foreground="black")
        self.probability_label.config(text="Probabilitas: -")
        self.recommendation_label.config(text="Rekomendasi: -", foreground="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeAttritionApp(root)
    root.mainloop()