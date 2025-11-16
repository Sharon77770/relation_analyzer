import tkinter as tk
from tkinter import font
from tkinter import scrolledtext

SET_A = [1, 2, 3, 4, 5]
N = len(SET_A)

# 행렬 문자열 변환
def matrix_to_string(matrix, title="Matrix"):
    s = f"\n--- {title} ---\n"
    if not matrix:
        s += " (비어 있음)\n"
        return s
    for row in matrix:
        s += " ".join(map(str, row)) + "\n"
    s += "-" * (len(title) + 6) + "\n"
    return s

# 반사 관계 판별
def is_reflexive(matrix):
    for i in range(N):
        if matrix[i][i] == 0:
            return False
    return True

# 대칭 관계 판별
def is_symmetric(matrix):
    for i in range(N):
        for j in range(i + 1, N):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

# 추이 관계 판별
def is_transitive(matrix):
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if matrix[i][j] == 1 and matrix[j][k] == 1 and matrix[i][k] == 0:
                    return False
    return True

# 동치류 생성
def find_equivalence_classes(matrix):
    results = "\n--- 동치류(Equivalence Classes) 탐색 ---\n"
    results += "1. 각 원소별 동치류:\n"
    element_classes = {}
    for i in range(N):
        element = SET_A[i]
        element_class = []
        for j in range(N):
            if matrix[i][j] == 1:
                element_class.append(SET_A[j])
        element_classes[element] = sorted(list(set(element_class)))
        results += f"[{element}] = {element_classes[element]}\n"

    results += "\n2. 집합 A의 분할 (Partition):\n"
    visited = [False] * N
    partition = []
    for i in range(N):
        if not visited[i]:
            current_class = element_classes[SET_A[i]]
            partition.append(current_class)
            for elem in current_class:
                visited[SET_A.index(elem)] = True
    
    for part in partition:
        results += f"{part}\n"
    return results

# 반사 폐포 생성
def reflexive_closure(matrix):
    closure = [row[:] for row in matrix]
    changed = False
    for i in range(N):
        if closure[i][i] == 0:
            closure[i][i] = 1
            changed = True
    return closure, changed

# 대칭 폐포 생성
def symmetric_closure(matrix):
    closure = [row[:] for row in matrix]
    changed = False
    for i in range(N):
        for j in range(i + 1, N):
            if closure[i][j] != closure[j][i]:
                closure[i][j] = 1
                closure[j][i] = 1
                changed = True
    return closure, changed

# 추이 폐포 생성
def transitive_closure(matrix):
    closure = [row[:] for row in matrix]
    for k in range(N):
        for i in range(N):
            for j in range(N):
                closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])
    return closure, True 

# 샘플 데이터 (레포트용 스크린샷을 위해 생성) 
SAMPLES = {
    '1': {
        'desc': "동치 관계 (샘플 1)",
        'matrix': [
            [1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1]
        ]
    },
    '2': {
        'desc': "동치 아님 (샘플 2)",
        'matrix': [
            [1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
    },
    '3': {
        'desc': "항등 관계 (샘플 3)",
        'matrix': [
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1]
        ]
    },
    '4': {
        'desc': "대칭X, 추이X (샘플 4)",
        'matrix': [
            [1, 1, 0, 1, 0],
            [0, 1, 1, 0, 0],
            [0, 1, 1, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 1]
        ]
    }
}

# GUI로직 

# Tkinter 메인 클래스
class RelationAnalyzerApp:
    
    # 앱 초기화 
    def __init__(self, root):
        self.root = root
        self.root.title("이산수학 Report2")
        self.root.geometry("900x650")

        self.fonts = {
            'title': font.Font(family="Helvetica", size=16, weight="bold"),
            'header': font.Font(family="Helvetica", size=12, weight="bold"),
            'body': font.Font(family="Helvetica", size=10),
            'matrix': font.Font(family="Courier", size=14, weight="bold")
        }
        self.colors = {
            'bg': '#2E2E2E',
            'fg': '#FFFFFF',
            'frame_bg': '#3C3C3C',
            'btn_bg': '#4F4F4F',
            'btn_fg': '#FFFFFF',
            'btn_active_bg': '#6A6A6A',
            'cell_0_bg': '#555555',
            'cell_0_fg': '#DDDDDD',
            'cell_1_bg': '#4A90E2',
            'cell_1_fg': '#FFFFFF',
            'text_bg': '#1E1E1E',
            'text_fg': '#EAEAEA',
            'success': '#7ED321',
            'fail': '#D0021B'
        }
        
        self.root.configure(bg=self.colors['bg'])

        self.matrix_buttons = []
        self.matrix_data = [[0 for _ in range(N)] for _ in range(N)]

        main_frame = tk.Frame(root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        title_label = tk.Label(main_frame, text="관계 행렬 동치 판별기", font=self.fonts['title'], bg=self.colors['bg'], fg=self.colors['fg'])
        title_label.pack(pady=(0, 15))

        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(content_frame, width=450, bg=self.colors['frame_bg'], relief=tk.RIDGE, borderwidth=2, padx=15, pady=15)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        left_frame.pack_propagate(False)

        header1 = tk.Label(left_frame, text="1. 관계 행렬 입력 (A = {1..5})", font=self.fonts['header'], bg=self.colors['frame_bg'], fg=self.colors['fg'])
        header1.pack(anchor='w', pady=(0, 10))

        matrix_grid_frame = tk.Frame(left_frame, bg=self.colors['frame_bg'])
        matrix_grid_frame.pack(pady=10)
        
        for i in range(N):
            row_buttons = []
            for j in range(N):
                btn = tk.Button(matrix_grid_frame, text="0", font=self.fonts['matrix'], 
                                width=3, height=1, relief=tk.GROOVE,
                                bg=self.colors['cell_0_bg'], fg=self.colors['cell_0_fg'],
                                activebackground=self.colors['cell_1_bg'],
                                activeforeground=self.colors['cell_1_fg'],
                                command=lambda r=i, c=j: self.toggle_cell(r, c))
                btn.grid(row=i, column=j, padx=4, pady=4)
                row_buttons.append(btn)
            self.matrix_buttons.append(row_buttons)

        control_frame = tk.Frame(left_frame, bg=self.colors['frame_bg'])
        control_frame.pack(fill=tk.X, pady=15)

        self.analyze_button = tk.Button(control_frame, text="판별하기", font=self.fonts['body'], 
                                        bg='#4A90E2', fg=self.colors['btn_fg'], 
                                        activebackground='#3A70C2', activeforeground=self.colors['btn_fg'],
                                        command=self.run_analysis)
        self.analyze_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.reset_button = tk.Button(control_frame, text="초기화", font=self.fonts['body'], 
                                      bg=self.colors['btn_bg'], fg=self.colors['btn_fg'],
                                      activebackground=self.colors['btn_active_bg'],
                                      command=self.reset_matrix)
        self.reset_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        sample_frame = tk.Frame(left_frame, bg=self.colors['frame_bg'])
        sample_frame.pack(fill=tk.X, pady=10)
        
        sample_header = tk.Label(sample_frame, text="샘플 데이터 로드:", font=self.fonts['header'], bg=self.colors['frame_bg'], fg=self.colors['fg'])
        sample_header.pack(anchor='w')

        sample_btn_frame = tk.Frame(sample_frame, bg=self.colors['frame_bg'])
        sample_btn_frame.pack(fill=tk.X, pady=5)
        
        col_width = 2
        for i, (key, val) in enumerate(SAMPLES.items()):
            btn = tk.Button(sample_btn_frame, text=val['desc'], font=self.fonts['body'],
                            bg=self.colors['btn_bg'], fg=self.colors['btn_fg'],
                            activebackground=self.colors['btn_active_bg'],
                            command=lambda m=val['matrix']: self.load_sample(m))
            btn.grid(row=i//col_width, column=i%col_width, padx=5, pady=2, sticky='ew')
        
        sample_btn_frame.grid_columnconfigure((0, 1), weight=1)

        right_frame = tk.Frame(content_frame, width=450, bg=self.colors['frame_bg'], relief=tk.RIDGE, borderwidth=2, padx=15, pady=15)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)

        header2 = tk.Label(right_frame, text="2. 분석 결과", font=self.fonts['header'], bg=self.colors['frame_bg'], fg=self.colors['fg'])
        header2.pack(anchor='w', pady=(0, 10))

        self.results_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, 
                                                      font=self.fonts['body'], 
                                                      bg=self.colors['text_bg'], 
                                                      fg=self.colors['text_fg'],
                                                      insertbackground=self.colors['fg'], 
                                                      state='disabled')
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        self.results_text.tag_config('success', foreground=self.colors['success'], font=font.Font(family="Helvetica", size=11, weight="bold"))
        self.results_text.tag_config('fail', foreground=self.colors['fail'], font=font.Font(family="Helvetica", size=11, weight="bold"))
        self.results_text.tag_config('header', foreground='#4A90E2', font=self.fonts['header'])

        self.show_message("행렬을 입력하거나 샘플을 로드한 후 '판별하기' 버튼 클릭")

    # 결과창 텍스트 업데이트
    def show_message(self, msg, tag=None):
        self.results_text.configure(state='normal')
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert(tk.END, msg, tag)
        self.results_text.configure(state='disabled')
    
    # 결과창 텍스트 어펜드
    def append_message(self, msg, tag=None):
        self.results_text.configure(state='normal')
        self.results_text.insert(tk.END, msg, tag)
        self.results_text.configure(state='disabled')

    # 토글 버튼 효과
    def toggle_cell(self, r, c):
        current_val = self.matrix_data[r][c]
        new_val = 1 - current_val
        self.matrix_data[r][c] = new_val
        self.update_matrix_buttons()

    # 토글 버튼 업데이트 (샘플데이터)
    def update_matrix_buttons(self):
        for i in range(N):
            for j in range(N):
                val = self.matrix_data[i][j]
                btn = self.matrix_buttons[i][j]
                if val == 1:
                    btn.config(text="1", bg=self.colors['cell_1_bg'], fg=self.colors['cell_1_fg'])
                else:
                    btn.config(text="0", bg=self.colors['cell_0_bg'], fg=self.colors['cell_0_fg'])

    # 매트릭스 초기화
    def reset_matrix(self):
        self.matrix_data = [[0 for _ in range(N)] for _ in range(N)]
        self.update_matrix_buttons()
        self.show_message("행렬이 초기화되었습니다.")

    # 샘플 데이터 로드
    def load_sample(self, sample_matrix):
        self.matrix_data = [row[:] for row in sample_matrix]
        self.update_matrix_buttons()
        self.show_message(f"샘플을 로드했습니다. '판별하기'를 누르세요.")

    # 분석하기 버튼 기능
    def run_analysis(self):
        m = self.matrix_data
        self.results_text.configure(state='normal')
        self.results_text.delete('1.0', tk.END) 

        def add_result(text, tag=None):
            self.results_text.insert(tk.END, text + '\n', tag)
        
        add_result("--- 1. 최초 행렬 동치 관계 판별 ---", 'header')
        is_ref = is_reflexive(m)
        is_sym = is_symmetric(m)
        is_trans = is_transitive(m)
        
        add_result(f"  1. 반사 관계 (Reflexive)?   -> {is_ref}", 'success' if is_ref else 'fail')
        add_result(f"  2. 대칭 관계 (Symmetric)?   -> {is_sym}", 'success' if is_sym else 'fail')
        add_result(f"  3. 추이 관계 (Transitive)? -> {is_trans}", 'success' if is_trans else 'fail')

        if is_ref and is_sym and is_trans:
            add_result("\n[결과] 이 관계는 동치 관계입니다.", 'success')
            class_results = find_equivalence_classes(m)
            add_result(class_results)
        else:
            add_result("\n[결과] 이 관계는 동치 관계가 아닙니다.", 'fail')
            add_result("\n--- 2. 동치 폐포(Equivalence Closure) 생성 ---", 'header')
            
            add_result("\n[단계 1: 반사 폐포 생성]")
            r_closure, r_changed = reflexive_closure(m)
            if not r_changed:
                add_result(">> 이미 반사 관계입니다.")
            add_result(matrix_to_string(r_closure, "반사 폐포 (r(R))"))

            add_result("[단계 2: 대칭 폐포 생성]")
            sr_closure, s_changed = symmetric_closure(r_closure)
            if not s_changed:
                add_result(">> 이미 대칭 관계입니다.")
            add_result(matrix_to_string(sr_closure, "대칭 폐포 (s(r(R)))"))

            add_result("[단계 3: 추이 폐포 생성 (Warshall's)]")
            eq_closure, _ = transitive_closure(sr_closure)
            add_result(matrix_to_string(eq_closure, "최종 동치 폐포 (t(s(r(R))))"))
            
            add_result("\n--- 3. 생성된 동치 폐포의 관계 판별 (검증) ---", 'header')
            final_ref = is_reflexive(eq_closure)
            final_sym = is_symmetric(eq_closure)
            final_trans = is_transitive(eq_closure)
            add_result(f"  1. 반사 관계?   -> {final_ref}", 'success' if final_ref else 'fail')
            add_result(f"  2. 대칭 관계?   -> {final_sym}", 'success' if final_sym else 'fail')
            add_result(f"  3. 추이 관계?   -> {final_trans}", 'success' if final_trans else 'fail')
            
            if final_ref and final_sym and final_trans:
                add_result("\n[결과] 생성된 동치 폐포는 동치 관계입니다.", 'success')
                class_results = find_equivalence_classes(eq_closure)
                add_result(class_results)
            else:
                add_result("\n[오류] 동치 폐포 생성에 실패했습니다.", 'fail')
        
        self.results_text.see("1.0")
        self.results_text.configure(state='disabled')






if __name__ == "__main__":
    root = tk.Tk()
    app = RelationAnalyzerApp(root)
    root.mainloop()
