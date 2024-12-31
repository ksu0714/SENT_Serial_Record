############################################################################################################################################################
#단일 시리얼 채널에 대해 측정 방식으로 인디케이터 


# import tkinter as tk
# from tkinter import scrolledtext, filedialog, messagebox
# import serial
# import serial.tools.list_ports
# import threading
# from queue import Queue
# from datetime import datetime

# class SerialMonitorFrame(tk.Frame):
#     def __init__(self, parent, port=None):
#         super().__init__(parent)
        
#         self.port = port
#         self.baud_rate = 460800
#         self.ser = None

#         # 큐와 스레드 관련 변수
#         self.is_reading = False
#         self.data_queue = Queue()
#         self.max_lines = 500

#         self.init_ui()

#     def init_ui(self):
#         self.label = tk.Label(self, text="Select COM Port:")
#         self.label.pack()

#         self.com_port_var = tk.StringVar()
#         self.com_port_menu = tk.OptionMenu(self, self.com_port_var, *self.get_com_ports())
#         self.com_port_menu.pack()

#         self.connect_button = tk.Button(self, text="Connect", command=self.connect_serial)
#         self.connect_button.pack()

#         self.label = tk.Label(self, text="Enter command:")
#         self.label.pack()

#         self.entry = tk.Entry(self, width=30)
#         self.entry.pack()

#         self.send_button = tk.Button(self, text="Send", command=self.send_command, state=tk.DISABLED)
#         self.send_button.pack()

#         # 측정 버튼과 CH1, CH2 인디케이터 추가
#         self.measure_button = tk.Button(self, text="Measure", command=self.measure, state=tk.DISABLED)
#         self.measure_button.pack()

#         self.ch1_label = tk.Label(self, text="CH1:")
#         self.ch1_label.pack()
#         self.ch1_value = tk.Label(self, text="---")
#         self.ch1_value.pack()

#         self.ch2_label = tk.Label(self, text="CH2:")
#         self.ch2_label.pack()
#         self.ch2_value = tk.Label(self, text="---")
#         self.ch2_value.pack()

#         self.output = scrolledtext.ScrolledText(self, width=70, height=20, state='normal')
#         self.output.pack()

#     def get_com_ports(self):
#         ports = serial.tools.list_ports.comports()
#         return [port.device for port in ports]

#     def connect_serial(self):
#         port = self.com_port_var.get()
#         if port:
#             try:
#                 self.ser = serial.Serial(port, self.baud_rate, timeout=1)
#                 self.is_reading = True
#                 self.send_button.config(state=tk.NORMAL)
#                 self.measure_button.config(state=tk.NORMAL)
#                 self.connect_button.config(state=tk.DISABLED)

#                 self.label.config(text=f"Connected to {port}")

#                 self.read_thread = threading.Thread(target=self.read_from_serial)
#                 self.read_thread.daemon = True
#                 self.read_thread.start()

#                 self.update_gui()

#                 self.output.insert(tk.END, f"Connected to {port}\n")
#             except serial.SerialException as e:
#                 tk.messagebox.showerror("Serial Port Error", f"Failed to open serial port {port}: {e}")
#         else:
#             tk.messagebox.showwarning("No Port Selected", "Please select a COM port before connecting.")

#     def send_command(self):
#         command = self.entry.get()
#         if command and self.ser.is_open:
#             try:
#                 self.ser.write(command.encode('utf-8') + b'\n')
#                 self.output.insert(tk.END, f"Sent: {command}\n")
#                 self.entry.delete(0, tk.END)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Failed to send command: {e}\n")
#             self.output.see(tk.END)

#     def measure(self):
#         if self.ser.is_open:
#             try:
#                 self.ser.write(b'l\n')  # 측정 명령 전송
#                 self.output.insert(tk.END, "Sent: l\n")
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Failed to send measure command: {e}\n")
#             self.output.see(tk.END)

#     def read_from_serial(self):
#         while self.is_reading:
#             try:
#                 data = self.ser.readline().decode('utf-8').strip()
#                 if data:
#                     self.data_queue.put(data)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Serial error: {e}\n")
#                 self.is_reading = False

#     def update_gui(self):
#         while not self.data_queue.empty():
#             data = self.data_queue.get()
#             self.output.insert(tk.END, f"Received: {data}\n")
#             if "FastCH:Standard format" in data:
#                 try:
#                     parts = data.split(",")
#                     ch1 = parts[1].strip()
#                     ch2 = parts[2].strip()
#                     self.ch1_value.config(text=ch1)
#                     self.ch2_value.config(text=ch2)
#                 except Exception as e:
#                     self.output.insert(tk.END, f"Error parsing measurement data: {e}\n")
#             self.output.see(tk.END)

#         self.after(50, self.update_gui)


# class SerialMonitorApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Multi Serial Monitor")
#         self.geometry("800x600")

#         self.init_ui()

#     def init_ui(self):
#         self.frame = SerialMonitorFrame(self)
#         self.frame.pack(fill="both", expand=True)

#     def on_closing(self):
#         self.frame.is_reading = False
#         if self.frame.ser and self.frame.ser.is_open:
#             self.frame.ser.close()
#         self.destroy()

# if __name__ == "__main__":
#     app = SerialMonitorApp()
#     app.protocol("WM_DELETE_WINDOW", app.on_closing)
#     app.mainloop()


##################################################################################


## 장치 추가, 삭제
## ID 입력 기능 추가

# import tkinter as tk
# from tkinter import scrolledtext, messagebox
# import serial
# import serial.tools.list_ports
# import threading
# from queue import Queue

# class SerialDeviceFrame(tk.Frame):
#     """
#     단일 시리얼 장치를 위한 Frame.
#     - 포트 선택, 연결/해제
#     - 명령 전송, 측정(l\n) 전송
#     - ID를 입력받아, 수신 데이터에 함께 표시
#     - 백그라운드 스레드로 수신 -> Queue -> GUI 업데이트
#     - 로그 저장
#     """
#     def __init__(self, parent, app_reference, device_index):
#         """
#         :param parent: 부모 위젯 (여기서는 device들을 담을 컨테이너 Frame)
#         :param app_reference: MultiSerialMonitorApp 객체 (글로벌 Baud Rate, used_ports 등 참조)
#         :param device_index: 내부적으로 부여하는 디바이스 순번(0, 1, 2, ...)
#         """
#         super().__init__(parent)
#         self.app = app_reference
#         self.device_index = device_index  # 내부 관리용 인덱스

#         # 시리얼 관련
#         self.ser = None
#         self.is_reading = False
#         self.read_thread = None
#         self.data_queue = Queue()

#         # 현재 연결된 포트 (중복 체크, 해제 시 사용)
#         self.current_port = None

#         # ID를 사용자에게 입력받기 위한 StringVar
#         self.id_var = tk.StringVar(value="")  # 초기값은 빈 문자열

#         # UI 초기화
#         self.init_ui()

#     def init_ui(self):
#         # 상단 라벨 (Device X)
#         title_label = tk.Label(self, text=f"[Device Frame #{self.device_index + 1}]", 
#                                font=('Arial', 12, 'bold'))
#         title_label.pack(pady=(5, 2), anchor='w')

#         # ID 입력
#         id_frame = tk.Frame(self)
#         id_frame.pack(fill='x')
#         tk.Label(id_frame, text="Device ID:").pack(side='left')
#         tk.Entry(id_frame, textvariable=self.id_var, width=10).pack(side='left', padx=(5, 10))

#         # 포트 선택 메뉴
#         tk.Label(self, text="Select COM Port:").pack(anchor='w')
#         self.com_port_var = tk.StringVar(value="")
#         ports = self.get_com_ports()
#         if ports:
#             self.com_port_var.set(ports[0])  # 기본값 (있으면 첫 번째)
#         self.com_port_menu = tk.OptionMenu(self, self.com_port_var, *ports)
#         self.com_port_menu.pack(fill='x')

#         # Connect / Disconnect 버튼
#         button_frame = tk.Frame(self)
#         button_frame.pack(fill='x', pady=2)
#         self.connect_button = tk.Button(button_frame, text="Connect", width=8, command=self.connect_serial)
#         self.connect_button.pack(side='left', padx=(0, 5))
#         self.disconnect_button = tk.Button(button_frame, text="Disconnect", width=10, 
#                                            command=self.disconnect_serial, state=tk.DISABLED)
#         self.disconnect_button.pack(side='left')

#         # 명령 전송
#         tk.Label(self, text="Enter command:").pack(anchor='w', pady=(5,0))
#         self.entry = tk.Entry(self, width=30)
#         self.entry.pack()
#         self.send_button = tk.Button(self, text="Send", command=self.send_command, state=tk.DISABLED)
#         self.send_button.pack(pady=2)

#         # 측정 버튼
#         self.measure_button = tk.Button(self, text="Measure", command=self.measure, state=tk.DISABLED)
#         self.measure_button.pack(pady=2)

#         # ID / CH1 / CH2 라벨
#         self.id_label = tk.Label(self, text="ID: ---")
#         self.id_label.pack()
#         self.ch1_label = tk.Label(self, text="CH1: ---")
#         self.ch1_label.pack()
#         self.ch2_label = tk.Label(self, text="CH2: ---")
#         self.ch2_label.pack()

#         # 출력 창
#         self.output = scrolledtext.ScrolledText(self, width=70, height=8)
#         self.output.pack(pady=5)

#     def get_com_ports(self):
#         """현재 PC에서 사용 가능한 COM 포트 목록 반환"""
#         ports = serial.tools.list_ports.comports()
#         return [port.device for port in ports]

#     def refresh_port_list(self):
#         """포트 목록 갱신 시 호출."""
#         new_ports = self.get_com_ports()
#         menu = self.com_port_menu["menu"]
#         menu.delete(0, "end")  # 기존 목록 삭제
#         for p in new_ports:
#             menu.add_command(label=p, 
#                              command=lambda value=p: self.com_port_var.set(value))

#         # 현재 선택된 포트가 유효하지 않으면 기본값 재설정
#         if self.com_port_var.get() not in new_ports:
#             self.com_port_var.set(new_ports[0] if new_ports else "")

#     def connect_serial(self):
#         """Connect 버튼 동작: 글로벌 Baud Rate로 포트 연결. 중복 연결 방지."""
#         port = self.com_port_var.get()
#         if not port:
#             messagebox.showwarning("No Port Selected", 
#                                    f"[Device #{self.device_index+1}] Please select a COM port.")
#             return

#         # 이미 사용 중인 포트인지 확인
#         if port in self.app.used_ports:
#             messagebox.showwarning("Port In Use", 
#                                    f"Port {port} is already connected by another device.")
#             return

#         try:
#             baud_rate = self.app.global_baud_rate
#             self.ser = serial.Serial(port, baud_rate, timeout=1)
#             self.is_reading = True
#             self.connect_button.config(state=tk.DISABLED)
#             self.disconnect_button.config(state=tk.NORMAL)
#             self.send_button.config(state=tk.NORMAL)
#             self.measure_button.config(state=tk.NORMAL)

#             self.current_port = port
#             self.app.used_ports.add(port)  # 포트 중복 방지 세트에 추가

#             self.output.insert(tk.END, f"Connected to {port} (Baud: {baud_rate})\n")
#             self.output.see(tk.END)

#             # 수신 스레드 시작
#             self.read_thread = threading.Thread(target=self.read_from_serial, daemon=True)
#             self.read_thread.start()

#             # 주기적으로 UI 업데이트
#             self.after(50, self.update_gui)

#         except serial.SerialException as e:
#             messagebox.showerror("Serial Port Error", f"Failed to open {port}\nError: {e}")

#     def disconnect_serial(self):
#         """Disconnect 버튼 동작."""
#         if self.ser and self.ser.is_open:
#             self.close()
#             self.output.insert(tk.END, "Disconnected.\n")
#             self.output.see(tk.END)

#         self.connect_button.config(state=tk.NORMAL)
#         self.disconnect_button.config(state=tk.DISABLED)
#         self.send_button.config(state=tk.DISABLED)
#         self.measure_button.config(state=tk.DISABLED)

#     def send_command(self):
#         """Send 버튼 동작: 입력된 명령을 시리얼로 전송."""
#         if not (self.ser and self.ser.is_open):
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return

#         command = self.entry.get()
#         if command:
#             try:
#                 self.ser.write(command.encode('utf-8') + b'\n')
#                 self.output.insert(tk.END, f"Sent: {command}\n")
#                 self.entry.delete(0, tk.END)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Failed to send command: {e}\n")
#             self.output.see(tk.END)

#     def measure(self):
#         """Measure 버튼 동작: 'l\\n' 명령 전송."""
#         if not (self.ser and self.ser.is_open):
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return
#         try:
#             self.ser.write(b'l\n')
#             self.output.insert(tk.END, "Sent: l\n")
#         except serial.SerialException as e:
#             self.output.insert(tk.END, f"Failed to send measure command: {e}\n")
#         self.output.see(tk.END)

#     def read_from_serial(self):
#         """백그라운드 스레드: 시리얼 데이터를 읽어서 Queue에 저장."""
#         while self.is_reading:
#             try:
#                 line = self.ser.readline().decode('utf-8', errors='replace').strip()
#                 if line:
#                     self.data_queue.put(line)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Serial read error: {e}\n")
#                 self.output.see(tk.END)
#                 self.is_reading = False
#                 break

#     def update_gui(self):
#         """메인 스레드에서 Queue에 쌓인 데이터를 처리 & 특정 포맷 파싱."""
#         while not self.data_queue.empty():
#             data = self.data_queue.get()
#             self.output.insert(tk.END, f"Received: {data}\n")

#             # 특정 포맷 예시: "FastCH:Standard format, value1, value2"
#             # ID, CH1, CH2 를 표시
#             if "FastCH:Standard format" in data:
#                 try:
#                     parts = data.split(",")
#                     ch1 = parts[1].strip()
#                     ch2 = parts[2].strip()

#                     # 사용자 입력한 ID를 가져와 함께 표시
#                     current_id = self.id_var.get()
#                     # 라벨 업데이트
#                     self.id_label.config(text=f"ID: {current_id}")
#                     self.ch1_label.config(text=f"CH1: {ch1}")
#                     self.ch2_label.config(text=f"CH2: {ch2}")

#                     # 로그 창에도 기록
#                     self.output.insert(
#                         tk.END, 
#                         f"Parsed => ID={current_id}, CH1={ch1}, CH2={ch2}\n"
#                     )
#                 except Exception as e:
#                     self.output.insert(tk.END, f"Error parsing data: {e}\n")

#             self.output.see(tk.END)

#         if self.is_reading:
#             self.after(50, self.update_gui)

#     def close(self):
#         """
#         이 Frame(장치)을 종료(Disconnect)할 때 호출:
#         - 스레드 종료
#         - 포트 닫기
#         - used_ports에서 제거
#         """
#         self.is_reading = False
#         if self.ser and self.ser.is_open:
#             try:
#                 self.ser.close()
#             except:
#                 pass
#         if self.current_port in self.app.used_ports:
#             self.app.used_ports.remove(self.current_port)
#         self.current_port = None

#     def save_log_to_file(self):
#         """
#         현재 ScrolledText에 표시된 내용을 'deviceX.log' 형식으로 저장
#         """
#         log_text = self.output.get("1.0", tk.END)
#         filename = f"device_{self.device_index+1}.log"
#         try:
#             with open(filename, "w", encoding="utf-8") as f:
#                 f.write(log_text)
#             messagebox.showinfo("Log Saved", 
#                                 f"[Device #{self.device_index+1}] Log saved to {filename}")
#         except OSError as e:
#             messagebox.showerror("Save Error", 
#                                  f"Failed to save log for Device #{self.device_index+1}\nError: {e}")


# class MultiSerialMonitorApp(tk.Tk):
#     """
#     여러 SerialDeviceFrame을 동적으로 추가/제거하며
#     동시에 여러 시리얼 장치를 모니터링할 수 있는 메인 앱.
#     - Add Device / Remove Device
#     - Global Baud Rate
#     - Connect All, Measure All, Refresh Ports, Save Logs
#     - used_ports(집합)으로 포트 중복 연결 방지
#     """
#     def __init__(self):
#         super().__init__()
#         self.title("Multi Serial Monitor (Dynamic)")
#         self.geometry("1100x850")

#         # 현재 사용 중인 포트를 관리 (중복 연결 방지)
#         self.used_ports = set()

#         # 글로벌 Baud Rate (초기값)
#         self.global_baud_rate = 460800

#         # 디바이스(Frame)들을 담을 리스트
#         self.device_frames = []

#         # 상단 컨트롤 UI
#         self.init_top_controls()

#         # 디바이스들을 담을 메인 컨테이너 프레임
#         self.devices_container = tk.Frame(self)
#         self.devices_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)

#         # 종료 처리
#         self.protocol("WM_DELETE_WINDOW", self.on_closing)

#     def init_top_controls(self):
#         """
#         상단부: Baud Rate 설정, Connect All, Measure All, Refresh Ports, Save Logs,
#         Add Device, Remove Device
#         """
#         top_frame = tk.Frame(self)
#         top_frame.pack(side="top", fill="x", padx=5, pady=5)

#         # 글로벌 Baud Rate 설정
#         tk.Label(top_frame, text="Global Baud Rate:").pack(side='left', padx=(0, 5))
#         self.baud_entry_var = tk.StringVar(value=str(self.global_baud_rate))
#         self.baud_entry = tk.Entry(top_frame, width=10, textvariable=self.baud_entry_var)
#         self.baud_entry.pack(side='left', padx=(0, 10))

#         # Baud Rate 설정 버튼
#         self.set_baud_button = tk.Button(top_frame, text="Set Baud Rate", command=self.set_baud_rate)
#         self.set_baud_button.pack(side='left', padx=(0, 15))

#         # Connect All
#         self.connect_all_button = tk.Button(top_frame, text="Connect All", command=self.connect_all)
#         self.connect_all_button.pack(side="left", padx=(0, 10))

#         # Measure All
#         self.measure_all_button = tk.Button(top_frame, text="Measure All", command=self.measure_all)
#         self.measure_all_button.pack(side="left", padx=(0, 10))

#         # Refresh Ports
#         self.refresh_ports_button = tk.Button(top_frame, text="Refresh Ports", command=self.refresh_all_ports)
#         self.refresh_ports_button.pack(side="left", padx=(0, 10))

#         # Save Logs
#         self.save_logs_button = tk.Button(top_frame, text="Save Logs", command=self.save_all_logs)
#         self.save_logs_button.pack(side="left", padx=(0, 10))

#         # Add / Remove Device
#         self.add_device_button = tk.Button(top_frame, text="Add Device", command=self.add_device)
#         self.add_device_button.pack(side="left", padx=(20, 10))

#         self.remove_device_button = tk.Button(top_frame, text="Remove Device", command=self.remove_device)
#         self.remove_device_button.pack(side="left", padx=(0, 10))

#     def add_device(self):
#         """사용자가 디바이스를 추가 (새 Frame)"""
#         device_index = len(self.device_frames)
#         frame = SerialDeviceFrame(self.devices_container, self, device_index)
#         frame.pack(side="top", fill="x", expand=True, padx=5, pady=5)
#         self.device_frames.append(frame)

#     def remove_device(self):
#         """사용자가 마지막 디바이스를 제거"""
#         if not self.device_frames:
#             return  # 제거할 디바이스 없음
#         frame = self.device_frames.pop()
#         frame.close()      # 연결되어 있으면 닫기
#         frame.destroy()    # UI 제거

#     def set_baud_rate(self):
#         """상단에 입력된 Baud Rate를 global_baud_rate에 반영"""
#         val = self.baud_entry_var.get()
#         try:
#             new_baud = int(val)
#             self.global_baud_rate = new_baud
#             messagebox.showinfo("Baud Rate", f"Global Baud Rate set to {new_baud}")
#         except ValueError:
#             messagebox.showwarning("Invalid Value", "Please enter a valid integer for Baud Rate.")

#     def connect_all(self):
#         """모든 Frame에 대해 connect_serial() 호출"""
#         for frame in self.device_frames:
#             if frame.com_port_var.get():
#                 frame.connect_serial()

#     def measure_all(self):
#         """모든 Frame에 대해 measure() 호출"""
#         for frame in self.device_frames:
#             frame.measure()

#     def refresh_all_ports(self):
#         """모든 Frame의 포트 목록을 갱신"""
#         for frame in self.device_frames:
#             frame.refresh_port_list()

#     def save_all_logs(self):
#         """모든 Frame에 대해 로그 저장"""
#         for frame in self.device_frames:
#             frame.save_log_to_file()

#     def on_closing(self):
#         """창이 닫힐 때 모든 장치 Disconnect -> 스레드 종료 -> 창 파괴"""
#         for frame in self.device_frames:
#             frame.close()
#         self.destroy()


# if __name__ == "__main__":
#     app = MultiSerialMonitorApp()
#     app.mainloop()


## 장치 2x5 그리드 배치
## 장치 최대 10개개


# import tkinter as tk
# from tkinter import scrolledtext, messagebox
# import serial
# import serial.tools.list_ports
# import threading
# from queue import Queue

# class SerialDeviceFrame(tk.Frame):
#     """
#     단일 시리얼 장치를 위한 Frame.
#     - 포트 선택, 연결/해제
#     - 명령 전송, 측정(l\n) 전송
#     - ID / ID2 인디케이터
#     - 백그라운드 스레드로 수신 -> Queue -> GUI 업데이트
#     """
#     def __init__(self, parent, app_reference, device_label):
#         """
#         :param parent: 이 Frame을 담을 부모(그리드에 배치될 컨테이너)
#         :param app_reference: MultiSerialMonitorApp (글로벌 Baud Rate, used_ports 등 참조)
#         :param device_label: '장치1', '장치2', ... 이런 식의 문자열
#         """
#         super().__init__(parent)
#         self.app = app_reference
#         self.device_label = device_label  # "장치1", "장치2", ...

#         # 시리얼 관련
#         self.ser = None
#         self.is_reading = False
#         self.read_thread = None
#         self.data_queue = Queue()

#         # 현재 연결된 포트
#         self.current_port = None

#         # 사용자 입력 ID (CH1, CH2 파싱 시 표시)
#         self.id_var = tk.StringVar(value="")

#         # UI 초기화
#         self.init_ui()

#     def init_ui(self):
#         # 상단 라벨 (장치N)
#         title_label = tk.Label(self, text=f"[{self.device_label}]",
#                                font=('Arial', 12, 'bold'))
#         title_label.pack(pady=(5, 2), anchor='w')

#         # ID 입력
#         id_frame = tk.Frame(self)
#         id_frame.pack(fill='x')
#         tk.Label(id_frame, text="Device ID:").pack(side='left')
#         tk.Entry(id_frame, textvariable=self.id_var, width=10).pack(side='left', padx=(5, 10))

#         # 포트 선택 메뉴
#         tk.Label(self, text="Select COM Port:").pack(anchor='w')
#         self.com_port_var = tk.StringVar(value="")
#         ports = self.get_com_ports()
#         if ports:
#             self.com_port_var.set(ports[0])  # 기본값(있으면 첫 번째)
#         self.com_port_menu = tk.OptionMenu(self, self.com_port_var, *ports)
#         self.com_port_menu.pack(fill='x')

#         # Connect / Disconnect 버튼
#         button_frame = tk.Frame(self)
#         button_frame.pack(fill='x', pady=2)
#         self.connect_button = tk.Button(button_frame, text="Connect", width=8, command=self.connect_serial)
#         self.connect_button.pack(side='left', padx=(0, 5))
#         self.disconnect_button = tk.Button(button_frame, text="Disconnect", width=10,
#                                            command=self.disconnect_serial, state=tk.DISABLED)
#         self.disconnect_button.pack(side='left')

#         # 명령 전송
#         tk.Label(self, text="Enter command:").pack(anchor='w', pady=(5, 0))
#         self.entry = tk.Entry(self, width=30)
#         self.entry.pack()
#         self.send_button = tk.Button(self, text="Send", command=self.send_command, state=tk.DISABLED)
#         self.send_button.pack(pady=2)

#         # 측정 버튼
#         self.measure_button = tk.Button(self, text="Measure", command=self.measure, state=tk.DISABLED)
#         self.measure_button.pack(pady=2)

#         # ID / ID2 / CH1 / CH2 라벨
#         self.id_label = tk.Label(self, text="ID: ---")
#         self.id_label.pack()
#         self.id2_label = tk.Label(self, text="ID2: ---")   # 새로 추가한 ID2 라벨
#         self.id2_label.pack()
#         self.ch1_label = tk.Label(self, text="CH1: ---")
#         self.ch1_label.pack()
#         self.ch2_label = tk.Label(self, text="CH2: ---")
#         self.ch2_label.pack()

#         # 출력 창
#         self.output = scrolledtext.ScrolledText(self, width=70, height=8)
#         self.output.pack(pady=5)

#     def get_com_ports(self):
#         """현재 PC에서 사용 가능한 COM 포트 목록 반환"""
#         ports = serial.tools.list_ports.comports()
#         return [port.device for port in ports]

#     def refresh_port_list(self):
#         """포트 목록 갱신 시 호출"""
#         new_ports = self.get_com_ports()
#         menu = self.com_port_menu["menu"]
#         menu.delete(0, "end")  # 기존 목록 삭제
#         for p in new_ports:
#             menu.add_command(label=p,
#                              command=lambda value=p: self.com_port_var.set(value))

#         # 현재 선택된 포트가 유효하지 않으면 기본값 재설정
#         if self.com_port_var.get() not in new_ports:
#             self.com_port_var.set(new_ports[0] if new_ports else "")

#     def connect_serial(self):
#         """Connect 버튼 동작: 글로벌 Baud Rate로 포트 연결, 중복 연결 방지"""
#         port = self.com_port_var.get()
#         if not port:
#             messagebox.showwarning("No Port Selected",
#                                    f"[{self.device_label}] Please select a COM port.")
#             return

#         # 이미 사용 중인 포트인지 확인
#         if port in self.app.used_ports:
#             messagebox.showwarning("Port In Use", f"Port {port} is already connected by another device.")
#             return

#         try:
#             baud_rate = self.app.global_baud_rate
#             self.ser = serial.Serial(port, baud_rate, timeout=1)
#             self.is_reading = True
#             self.connect_button.config(state=tk.DISABLED)
#             self.disconnect_button.config(state=tk.NORMAL)
#             self.send_button.config(state=tk.NORMAL)
#             self.measure_button.config(state=tk.NORMAL)

#             self.current_port = port
#             self.app.used_ports.add(port)  # 포트 중복 방지 세트에 추가

#             self.output.insert(tk.END, f"Connected to {port} (Baud: {baud_rate})\n")
#             self.output.see(tk.END)

#             # 수신 스레드 시작
#             self.read_thread = threading.Thread(target=self.read_from_serial, daemon=True)
#             self.read_thread.start()

#             # 주기적으로 UI 업데이트
#             self.after(50, self.update_gui)

#         except serial.SerialException as e:
#             messagebox.showerror("Serial Port Error", f"Failed to open {port}\nError: {e}")

#     def disconnect_serial(self):
#         """Disconnect 버튼 동작"""
#         if self.ser and self.ser.is_open:
#             self.close()
#             self.output.insert(tk.END, "Disconnected.\n")
#             self.output.see(tk.END)

#         self.connect_button.config(state=tk.NORMAL)
#         self.disconnect_button.config(state=tk.DISABLED)
#         self.send_button.config(state=tk.DISABLED)
#         self.measure_button.config(state=tk.DISABLED)

#     def send_command(self):
#         """Send 버튼 동작: 입력된 명령을 시리얼로 전송"""
#         if not (self.ser and self.ser.is_open):
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return

#         command = self.entry.get()
#         if command:
#             try:
#                 self.ser.write(command.encode('utf-8') + b'\n')
#                 self.output.insert(tk.END, f"Sent: {command}\n")
#                 self.entry.delete(0, tk.END)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Failed to send command: {e}\n")
#             self.output.see(tk.END)

#     def measure(self):
#         """Measure 버튼 동작: 'l\\n' 명령 전송"""
#         if not (self.ser and self.ser.is_open):
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return
#         try:
#             self.ser.write(b'l\n')
#             self.output.insert(tk.END, "Sent: l\n")
#         except serial.SerialException as e:
#             self.output.insert(tk.END, f"Failed to send measure command: {e}\n")
#         self.output.see(tk.END)

#     def read_from_serial(self):
#         """백그라운드 스레드: 시리얼 데이터를 읽어서 Queue에 저장"""
#         while self.is_reading:
#             try:
#                 line = self.ser.readline().decode('utf-8', errors='replace').strip()
#                 if line:
#                     self.data_queue.put(line)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Serial read error: {e}\n")
#                 self.output.see(tk.END)
#                 self.is_reading = False
#                 break

#     def update_gui(self):
#         """
#         메인 스레드에서 Queue에 쌓인 데이터를 처리 & 특정 포맷 파싱
#         - ID2 파싱: "ID=00009" 등
#         - FastCH:Standard format => CH1, CH2
#         - ID (사용자 입력) => 라벨에 표시
#         """
#         while not self.data_queue.empty():
#             data = self.data_queue.get()
#             self.output.insert(tk.END, f"{data}\n")  # "Received: ..." 형식 그대로 출력

#             # 1) ID2 파싱: "ID=00009" 같은 패턴
#             if "ID=" in data:
#                 try:
#                     # "ID=00009" 이후부터 콤마 전까지 추출
#                     start_idx = data.index("ID=") + len("ID=")
#                     id2_candidate = data[start_idx:].split(",")[0].strip()
#                     # ID2 라벨 업데이트
#                     self.id2_label.config(text=f"ID2: {id2_candidate}")
#                     # 로그에 파싱 결과 출력
#                     self.output.insert(tk.END, f"Parsed => ID2={id2_candidate}\n")
#                 except Exception as ex:
#                     self.output.insert(tk.END, f"Error parsing ID2: {ex}\n")

#             # 2) FastCH:Standard format => CH1, CH2 파싱
#             if "FastCH:Standard format" in data:
#                 try:
#                     parts = data.split(",")
#                     # parts[0] : "Received: FastCH:Standard format(CH1 CH2)"
#                     ch1 = parts[1].strip()
#                     ch2 = parts[2].strip()

#                     # 사용자 입력한 ID는 id_var.get()
#                     current_id = self.id_var.get()
#                     # ID 라벨 업데이트
#                     self.id_label.config(text=f"ID: {current_id}")
#                     self.ch1_label.config(text=f"CH1: {ch1}")
#                     self.ch2_label.config(text=f"CH2: {ch2}")

#                     # 로그에도 표시
#                     self.output.insert(tk.END, f"Parsed => ID={current_id}, CH1={ch1}, CH2={ch2}\n")
#                 except Exception as e:
#                     self.output.insert(tk.END, f"Error parsing CH1/CH2: {e}\n")

#             self.output.see(tk.END)

#         if self.is_reading:
#             self.after(50, self.update_gui)

#     def close(self):
#         """
#         이 Frame(장치)을 종료(Disconnect)할 때 호출:
#         - 스레드 종료
#         - 포트 닫기
#         - used_ports에서 제거
#         """
#         self.is_reading = False
#         if self.ser and self.ser.is_open:
#             try:
#                 self.ser.close()
#             except:
#                 pass
#         if self.current_port in self.app.used_ports:
#             self.app.used_ports.remove(self.current_port)
#         self.current_port = None


# class MultiSerialMonitorApp(tk.Tk):
#     """
#     최대 10개의 시리얼 장치를 (2행 x 5열) 화면에 배치하여
#     동시에 여러 시리얼 장치를 모니터링할 수 있는 메인 앱.
#     - Add Device / Remove Device
#     - Global Baud Rate
#     - Connect All, Measure All, Refresh Ports
#     - used_ports(집합)으로 포트 중복 연결 방지
#     """
#     def __init__(self):
#         super().__init__()
#         self.title("Multi Serial Monitor (2x5 Grid)")
#         self.geometry("1300x600")

#         # 현재 사용 중인 포트를 관리 (중복 연결 방지)
#         self.used_ports = set()

#         # 글로벌 Baud Rate (초기값)
#         self.global_baud_rate = 460800

#         # 디바이스(Frame)들을 담을 리스트
#         self.device_frames = []

#         # 상단 컨트롤 UI
#         self.init_top_controls()

#         # 디바이스들을 담을 메인 컨테이너 (grid로 2행 x 5열)
#         self.devices_container = tk.Frame(self)
#         self.devices_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)

#         # 그리드 row/column 설정 (2행 x 5열)
#         for r in range(2):
#             self.devices_container.rowconfigure(r, weight=1)
#         for c in range(5):
#             self.devices_container.columnconfigure(c, weight=1)

#         # 종료 처리
#         self.protocol("WM_DELETE_WINDOW", self.on_closing)

#     def init_top_controls(self):
#         """
#         상단부: Baud Rate 설정, Connect All, Measure All, Refresh Ports,
#         Add Device, Remove Device
#         """
#         top_frame = tk.Frame(self)
#         top_frame.pack(side="top", fill="x", padx=5, pady=5)

#         # 글로벌 Baud Rate 설정
#         tk.Label(top_frame, text="Global Baud Rate:").pack(side='left', padx=(0, 5))
#         self.baud_entry_var = tk.StringVar(value=str(self.global_baud_rate))
#         self.baud_entry = tk.Entry(top_frame, width=10, textvariable=self.baud_entry_var)
#         self.baud_entry.pack(side='left', padx=(0, 10))

#         # Baud Rate 설정 버튼
#         self.set_baud_button = tk.Button(top_frame, text="Set Baud Rate", command=self.set_baud_rate)
#         self.set_baud_button.pack(side='left', padx=(0, 15))

#         # Connect All
#         self.connect_all_button = tk.Button(top_frame, text="Connect All", command=self.connect_all)
#         self.connect_all_button.pack(side="left", padx=(0, 10))

#         # Measure All
#         self.measure_all_button = tk.Button(top_frame, text="Measure All", command=self.measure_all)
#         self.measure_all_button.pack(side="left", padx=(0, 10))

#         # Refresh Ports
#         self.refresh_ports_button = tk.Button(top_frame, text="Refresh Ports", command=self.refresh_all_ports)
#         self.refresh_ports_button.pack(side="left", padx=(0, 10))

#         # Add / Remove Device
#         self.add_device_button = tk.Button(top_frame, text="Add Device", command=self.add_device)
#         self.add_device_button.pack(side="left", padx=(20, 10))

#         self.remove_device_button = tk.Button(top_frame, text="Remove Device", command=self.remove_device)
#         self.remove_device_button.pack(side="left", padx=(0, 10))

#     def add_device(self):
#         """사용자가 디바이스를 추가 (새 Frame). 최대 10개까지만."""
#         device_index = len(self.device_frames)
#         if device_index >= 10:
#             messagebox.showwarning("Limit Reached", "Cannot add more than 10 devices.")
#             return

#         device_label = f"장치{device_index + 1}"
#         frame = SerialDeviceFrame(self.devices_container, self, device_label)

#         # 2행 x 5열 배치
#         row = device_index // 5
#         col = device_index % 5
#         frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

#         self.device_frames.append(frame)

#     def remove_device(self):
#         """
#         사용자가 마지막 디바이스를 제거
#         - device_frames가 비어있지 않다면 pop() -> close(), UI 제거
#         - 그리드 레이아웃에서 해당 위치가 비게 됨
#         """
#         if not self.device_frames:
#             return  # 제거할 디바이스 없음
#         frame = self.device_frames.pop()
#         frame.close()      # 연결되어 있으면 닫기
#         frame.destroy()    # UI 제거

#     def set_baud_rate(self):
#         """상단에 입력된 Baud Rate를 global_baud_rate에 반영"""
#         val = self.baud_entry_var.get()
#         try:
#             new_baud = int(val)
#             self.global_baud_rate = new_baud
#             messagebox.showinfo("Baud Rate", f"Global Baud Rate set to {new_baud}")
#         except ValueError:
#             messagebox.showwarning("Invalid Value", "Please enter a valid integer for Baud Rate.")

#     def connect_all(self):
#         """모든 Frame에 대해 connect_serial() 호출"""
#         for frame in self.device_frames:
#             if frame.com_port_var.get():
#                 frame.connect_serial()

#     def measure_all(self):
#         """모든 Frame에 대해 measure() 호출"""
#         for frame in self.device_frames:
#             frame.measure()

#     def refresh_all_ports(self):
#         """모든 Frame의 포트 목록을 갱신"""
#         for frame in self.device_frames:
#             frame.refresh_port_list()

#     def on_closing(self):
#         """창이 닫힐 때 모든 장치 Disconnect -> 스레드 종료 -> 창 파괴"""
#         for frame in self.device_frames:
#             frame.close()
#         self.destroy()


# if __name__ == "__main__":
#     app = MultiSerialMonitorApp()
#     app.mainloop()





## 개별 누적 저장 기능 추가
##

# import tkinter as tk
# from tkinter import scrolledtext, messagebox
# import serial
# import serial.tools.list_ports
# import threading
# from queue import Queue
# import datetime

# class SerialDeviceFrame(tk.Frame):
#     """
#     단일 시리얼 장치를 위한 Frame.
#     - 포트 선택, 연결/해제
#     - 명령 전송, 측정(l\n) 전송
#     - ID / ID2 인디케이터
#     - 수신 데이터(백그라운드 스레드) -> Queue -> GUI 업데이트
#     - 측정 기록(measure_history)에 (측정횟수, ID, ID2, CH1, CH2) 저장
#     """
#     def __init__(self, parent, app_reference, device_label):
#         """
#         :param parent: devices_container (2x5 grid에 배치될 부모 Frame)
#         :param app_reference: MultiSerialMonitorApp 객체
#         :param device_label: "장치1", "장치2", ... 와 같은 이름
#         """
#         super().__init__(parent)
#         self.app = app_reference
#         self.device_label = device_label

#         # 시리얼 관련
#         self.ser = None
#         self.is_reading = False
#         self.read_thread = None
#         self.data_queue = Queue()

#         # 현재 연결된 포트
#         self.current_port = None

#         # 사용자 입력 ID (CH1, CH2 파싱 시 표시)
#         self.id_var = tk.StringVar(value="")

#         # 장치별 측정번호, 측정 기록 저장용
#         self.measure_count = 0
#         self.measure_history = []
#         # 예: [(1, "id값", "id2값", "ch1값", "ch2값"), (2, ...), ...]

#         self.init_ui()

#     def init_ui(self):
#         # 상단 라벨 (장치N)
#         title_label = tk.Label(self, text=f"[{self.device_label}]",
#                                font=('Arial', 12, 'bold'))
#         title_label.pack(pady=(5, 2), anchor='w')

#         # ID 입력
#         id_frame = tk.Frame(self)
#         id_frame.pack(fill='x')
#         tk.Label(id_frame, text="Device ID:").pack(side='left')
#         tk.Entry(id_frame, textvariable=self.id_var, width=10).pack(side='left', padx=(5, 10))

#         # 포트 선택 메뉴
#         tk.Label(self, text="Select COM Port:").pack(anchor='w')
#         self.com_port_var = tk.StringVar(value="")
#         ports = self.get_com_ports()
#         if ports:
#             self.com_port_var.set(ports[0])  
#         self.com_port_menu = tk.OptionMenu(self, self.com_port_var, *ports)
#         self.com_port_menu.pack(fill='x')

#         # Connect / Disconnect 버튼
#         button_frame = tk.Frame(self)
#         button_frame.pack(fill='x', pady=2)
#         self.connect_button = tk.Button(button_frame, text="Connect", width=8, command=self.connect_serial)
#         self.connect_button.pack(side='left', padx=(0, 5))
#         self.disconnect_button = tk.Button(button_frame, text="Disconnect", width=10,
#                                            command=self.disconnect_serial, state=tk.DISABLED)
#         self.disconnect_button.pack(side='left')

#         # 명령 전송
#         tk.Label(self, text="Enter command:").pack(anchor='w', pady=(5, 0))
#         self.entry = tk.Entry(self, width=30)
#         self.entry.pack()
#         self.send_button = tk.Button(self, text="Send", command=self.send_command, state=tk.DISABLED)
#         self.send_button.pack(pady=2)

#         # 측정 버튼
#         self.measure_button = tk.Button(self, text="Measure", command=self.measure, state=tk.DISABLED)
#         self.measure_button.pack(pady=2)

#         # ID / ID2 / CH1 / CH2 라벨
#         self.id_label = tk.Label(self, text="ID: ---")
#         self.id_label.pack()
#         self.id2_label = tk.Label(self, text="ID2: ---")
#         self.id2_label.pack()
#         self.ch1_label = tk.Label(self, text="CH1: ---")
#         self.ch1_label.pack()
#         self.ch2_label = tk.Label(self, text="CH2: ---")
#         self.ch2_label.pack()

#         # 출력 창
#         self.output = scrolledtext.ScrolledText(self, width=70, height=8)
#         self.output.pack(pady=5)

#     def get_com_ports(self):
#         """현재 PC에서 사용 가능한 COM 포트 목록 반환"""
#         ports = serial.tools.list_ports.comports()
#         return [port.device for port in ports]

#     def refresh_port_list(self):
#         """포트 목록 갱신 시 호출"""
#         new_ports = self.get_com_ports()
#         menu = self.com_port_menu["menu"]
#         menu.delete(0, "end")  # 기존 목록 삭제
#         for p in new_ports:
#             menu.add_command(label=p, command=lambda value=p: self.com_port_var.set(value))

#         if self.com_port_var.get() not in new_ports:
#             self.com_port_var.set(new_ports[0] if new_ports else "")

#     def connect_serial(self):
#         """Connect 버튼 동작: 글로벌 Baud Rate로 포트 연결, 중복 연결 방지"""
#         port = self.com_port_var.get()
#         if not port:
#             messagebox.showwarning("No Port Selected",
#                                    f"[{self.device_label}] Please select a COM port.")
#             return

#         # 이미 사용 중인 포트인지 확인
#         if port in self.app.used_ports:
#             messagebox.showwarning("Port In Use", f"Port {port} is already connected by another device.")
#             return

#         try:
#             baud_rate = self.app.global_baud_rate
#             self.ser = serial.Serial(port, baud_rate, timeout=1)
#             self.is_reading = True
#             self.connect_button.config(state=tk.DISABLED)
#             self.disconnect_button.config(state=tk.NORMAL)
#             self.send_button.config(state=tk.NORMAL)
#             self.measure_button.config(state=tk.NORMAL)

#             self.current_port = port
#             self.app.used_ports.add(port)

#             self.output.insert(tk.END, f"Connected to {port} (Baud: {baud_rate})\n")
#             self.output.see(tk.END)

#             # 연결되었으므로 Save Data 버튼 활성화 여부 갱신
#             self.app.update_save_button_state()

#             # 수신 스레드 시작
#             self.read_thread = threading.Thread(target=self.read_from_serial, daemon=True)
#             self.read_thread.start()

#             # 주기적으로 UI 업데이트
#             self.after(50, self.update_gui)

#         except serial.SerialException as e:
#             messagebox.showerror("Serial Port Error", f"Failed to open {port}\nError: {e}")

#     def disconnect_serial(self):
#         """Disconnect 버튼 동작"""
#         if self.ser and self.ser.is_open:
#             self.close()
#             self.output.insert(tk.END, "Disconnected.\n")
#             self.output.see(tk.END)

#         self.connect_button.config(state=tk.NORMAL)
#         self.disconnect_button.config(state=tk.DISABLED)
#         self.send_button.config(state=tk.DISABLED)
#         self.measure_button.config(state=tk.DISABLED)

#         # 연결 해제 후 Save Data 버튼 상태 갱신
#         self.app.update_save_button_state()

#     def send_command(self):
#         """Send 버튼 동작: 입력된 명령을 시리얼로 전송"""
#         if not self.is_connected():
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return

#         command = self.entry.get()
#         if command:
#             try:
#                 self.ser.write(command.encode('utf-8') + b'\n')
#                 self.output.insert(tk.END, f"Sent: {command}\n")
#                 self.entry.delete(0, tk.END)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Failed to send command: {e}\n")
#             self.output.see(tk.END)

#     def measure(self):
#         """Measure 버튼 동작: 'l\\n' 명령 전송"""
#         if not self.is_connected():
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return
#         try:
#             self.ser.write(b'l\n')
#             self.output.insert(tk.END, "Sent: l\n")
#         except serial.SerialException as e:
#             self.output.insert(tk.END, f"Failed to send measure command: {e}\n")
#         self.output.see(tk.END)

#     def read_from_serial(self):
#         """백그라운드 스레드: 시리얼 데이터를 계속 읽어서 Queue에 저장"""
#         while self.is_reading:
#             try:
#                 line = self.ser.readline().decode('utf-8', errors='replace').strip()
#                 if line:
#                     self.data_queue.put(line)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Serial read error: {e}\n")
#                 self.output.see(tk.END)
#                 self.is_reading = False
#                 break

#     def update_gui(self):
#         """
#         메인 스레드에서 Queue에 쌓인 데이터를 처리 & 특정 포맷 파싱
#         - ID2 파싱: "ID=00009" 등
#         - FastCH:Standard format => CH1, CH2 파싱 (측정 히스토리 기록)
#         """
#         while not self.data_queue.empty():
#             data = self.data_queue.get()
#             self.output.insert(tk.END, f"{data}\n")

#             # 1) ID2 파싱: "ID=..." 패턴
#             parsed_id2 = None
#             if "ID=" in data:
#                 try:
#                     start_idx = data.index("ID=") + len("ID=")
#                     parsed_id2 = data[start_idx:].split(",")[0].strip()
#                     self.id2_label.config(text=f"ID2: {parsed_id2}")
#                     self.output.insert(tk.END, f"Parsed => ID2={parsed_id2}\n")
#                 except Exception as ex:
#                     self.output.insert(tk.END, f"Error parsing ID2: {ex}\n")

#             # 2) FastCH:Standard format => CH1, CH2
#             if "FastCH:Standard format" in data:
#                 try:
#                     parts = data.split(",")
#                     ch1 = parts[1].strip()
#                     ch2 = parts[2].strip()

#                     current_id = self.id_var.get()
#                     self.id_label.config(text=f"ID: {current_id}")
#                     self.ch1_label.config(text=f"CH1: {ch1}")
#                     self.ch2_label.config(text=f"CH2: {ch2}")

#                     # 측정 횟수+1
#                     self.measure_count += 1

#                     # 측정 이력 저장: (측정번호, ID, ID2, CH1, CH2)
#                     self.measure_history.append(
#                         (self.measure_count, current_id, parsed_id2 if parsed_id2 else "", ch1, ch2)
#                     )

#                     self.output.insert(
#                         tk.END,
#                         f"Parsed => ID={current_id}, CH1={ch1}, CH2={ch2}, measure_count={self.measure_count}\n"
#                     )
#                 except Exception as e:
#                     self.output.insert(tk.END, f"Error parsing CH1/CH2: {e}\n")

#             self.output.see(tk.END)

#         if self.is_reading:
#             self.after(50, self.update_gui)

#     def is_connected(self):
#         """장치가 현재 시리얼 포트에 연결되어 있는지 여부 반환"""
#         return (self.ser is not None) and self.ser.is_open

#     def close(self):
#         """이 Frame(장치)을 종료(Disconnect)할 때 호출"""
#         self.is_reading = False
#         if self.ser and self.ser.is_open:
#             try:
#                 self.ser.close()
#             except:
#                 pass
#         if self.current_port in self.app.used_ports:
#             self.app.used_ports.remove(self.current_port)
#         self.current_port = None


# class MultiSerialMonitorApp(tk.Tk):
#     """
#     최대 10개의 시리얼 장치를 (2행 × 5열)로 화면에 배치해 모니터링.
#     + Save Data 버튼으로 전체 장치의 측정 기록을 시간스탬프 텍스트 파일로 저장.
#     """
#     def __init__(self):
#         super().__init__()
#         self.title("Multi Serial Monitor (2x5 Grid + Save)")
#         self.geometry("1300x600")

#         # 현재 사용 중인 포트를 관리 (중복 연결 방지)
#         self.used_ports = set()

#         # 글로벌 Baud Rate (초기값)
#         self.global_baud_rate = 460800

#         # 디바이스(Frame)들을 담을 리스트
#         self.device_frames = []

#         # 상단 컨트롤 UI
#         self.init_top_controls()

#         # 디바이스들을 담을 메인 컨테이너 (grid로 2행 × 5열)
#         self.devices_container = tk.Frame(self)
#         self.devices_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)

#         # 그리드 row/column 설정 (2행 × 5열)
#         for r in range(2):
#             self.devices_container.rowconfigure(r, weight=1)
#         for c in range(5):
#             self.devices_container.columnconfigure(c, weight=1)

#         # 종료 처리
#         self.protocol("WM_DELETE_WINDOW", self.on_closing)

#     def init_top_controls(self):
#         """
#         상단부: Baud Rate 설정, Connect All, Measure All, Refresh Ports,
#         Add Device, Remove Device, Save Data
#         """
#         top_frame = tk.Frame(self)
#         top_frame.pack(side="top", fill="x", padx=5, pady=5)

#         # 글로벌 Baud Rate 설정
#         tk.Label(top_frame, text="Global Baud Rate:").pack(side='left', padx=(0, 5))
#         self.baud_entry_var = tk.StringVar(value=str(self.global_baud_rate))
#         self.baud_entry = tk.Entry(top_frame, width=10, textvariable=self.baud_entry_var)
#         self.baud_entry.pack(side='left', padx=(0, 10))

#         self.set_baud_button = tk.Button(top_frame, text="Set Baud Rate", command=self.set_baud_rate)
#         self.set_baud_button.pack(side='left', padx=(0, 15))

#         # Connect All
#         self.connect_all_button = tk.Button(top_frame, text="Connect All", command=self.connect_all)
#         self.connect_all_button.pack(side="left", padx=(0, 10))

#         # Measure All
#         self.measure_all_button = tk.Button(top_frame, text="Measure All", command=self.measure_all)
#         self.measure_all_button.pack(side="left", padx=(0, 10))

#         # Refresh Ports
#         self.refresh_ports_button = tk.Button(top_frame, text="Refresh Ports", command=self.refresh_all_ports)
#         self.refresh_ports_button.pack(side="left", padx=(0, 10))

#         # Add / Remove Device
#         self.add_device_button = tk.Button(top_frame, text="Add Device", command=self.add_device)
#         self.add_device_button.pack(side="left", padx=(20, 10))

#         self.remove_device_button = tk.Button(top_frame, text="Remove Device", command=self.remove_device)
#         self.remove_device_button.pack(side="left", padx=(0, 10))

#         # Save Data 버튼
#         self.save_button = tk.Button(top_frame, text="Save Data", command=self.save_all_data, state=tk.DISABLED)
#         self.save_button.pack(side="left", padx=(20, 10))

#     def add_device(self):
#         """
#         사용자가 디바이스를 추가 (새 Frame). 최대 10개까지만.
#         """
#         device_index = len(self.device_frames)
#         if device_index >= 10:
#             messagebox.showwarning("Limit Reached", "Cannot add more than 10 devices.")
#             return

#         device_label = f"장치{device_index + 1}"
#         frame = SerialDeviceFrame(self.devices_container, self, device_label)

#         # 2행 × 5열 배치
#         row = device_index // 5
#         col = device_index % 5
#         frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

#         self.device_frames.append(frame)

#     def remove_device(self):
#         """
#         사용자가 마지막 디바이스를 제거
#         """
#         if not self.device_frames:
#             return
#         frame = self.device_frames.pop()
#         frame.close()
#         frame.destroy()

#         # Save 버튼 상태 갱신
#         self.update_save_button_state()

#     def set_baud_rate(self):
#         """
#         상단에 입력된 Baud Rate를 global_baud_rate에 반영
#         """
#         val = self.baud_entry_var.get()
#         try:
#             new_baud = int(val)
#             self.global_baud_rate = new_baud
#             messagebox.showinfo("Baud Rate", f"Global Baud Rate set to {new_baud}")
#         except ValueError:
#             messagebox.showwarning("Invalid Value", "Please enter a valid integer for Baud Rate.")

#     def connect_all(self):
#         """모든 Frame에 대해 connect_serial() 호출"""
#         for frame in self.device_frames:
#             if frame.com_port_var.get():
#                 frame.connect_serial()

#     def measure_all(self):
#         """모든 Frame에 대해 measure() 호출"""
#         for frame in self.device_frames:
#             frame.measure()

#     def refresh_all_ports(self):
#         """모든 Frame의 포트 목록을 갱신"""
#         for frame in self.device_frames:
#             frame.refresh_port_list()

#     def is_any_device_connected(self):
#         """하나라도 연결된 장치가 있는지 확인"""
#         return any(frame.is_connected() for frame in self.device_frames)

#     def update_save_button_state(self):
#         """
#         어떤 장치라도 연결 중이면 Save 버튼 활성화,
#         아니면 비활성화
#         """
#         if self.is_any_device_connected():
#             self.save_button.config(state=tk.NORMAL)
#         else:
#             self.save_button.config(state=tk.DISABLED)

#     def save_all_data(self):
#         """
#         현재까지 각 장치에 기록된 측정 이력을
#         한꺼번에 텍스트 파일(타임스탬프 기반 이름)로 저장
#         """
#         if not self.is_any_device_connected():
#             messagebox.showwarning("No Device Connected", "No devices are currently connected.")
#             return

#         # 파일명: YYYYMMDD_HHMMSS.txt
#         now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = f"{now_str}.txt"

#         # 1) 헤더 구성
#         # 예:  측정횟수  장치1ID  장치1ID2  장치1CH1  장치1CH2  장치2ID  장치2ID2 ...
#         header_cols = ["측정횟수"]  # 맨 첫 컬럼: 측정횟수
#         for frame in self.device_frames:
#             header_cols.append(f"{frame.device_label}ID")
#             header_cols.append(f"{frame.device_label}ID2")
#             header_cols.append(f"{frame.device_label}CH1")
#             header_cols.append(f"{frame.device_label}CH2")

#         # 2) 가장 많이 측정된 장치의 측정 개수
#         histories = [frame.measure_history for frame in self.device_frames]
#         max_rows = max((len(h) for h in histories), default=0)

#         # 3) 실제 데이터 행 구성
#         lines = []
#         # 헤더 한 줄
#         lines.append("\t".join(header_cols))

#         # row_idx번째 행에 대하여, 각 장치의 row_idx번째 기록을 가져온다
#         for row_idx in range(max_rows):
#             row_data = []

#             # 첫 컬럼: 측정횟수 (여기서는 row_idx+1)
#             measure_count_str = str(row_idx + 1)
#             row_data.append(measure_count_str)

#             for frame in self.device_frames:
#                 if len(frame.measure_history) > row_idx:
#                     (mcount, dev_id, dev_id2, ch1, ch2) = frame.measure_history[row_idx]
#                     row_data.append(dev_id)   # ID
#                     row_data.append(dev_id2)  # ID2
#                     row_data.append(ch1)
#                     row_data.append(ch2)
#                 else:
#                     # 이 장치는 row_idx번째 측정 기록이 없음 -> 공백
#                     row_data.append("")  
#                     row_data.append("")  
#                     row_data.append("")  
#                     row_data.append("")  

#             lines.append("\t".join(row_data))

#         # 4) 파일에 쓰기
#         try:
#             with open(filename, "w", encoding="utf-8") as f:
#                 for line in lines:
#                     f.write(line + "\n")

#             messagebox.showinfo("Save Complete", f"Data saved to {filename}")
#         except OSError as e:
#             messagebox.showerror("Save Error", f"Failed to save data.\nError: {e}")

#     def on_closing(self):
#         """창이 닫힐 때 모든 장치 Disconnect -> 스레드 종료 -> 창 파괴"""
#         for frame in self.device_frames:
#             frame.close()
#         self.destroy()


# if __name__ == "__main__":
#     app = MultiSerialMonitorApp()
#     app.mainloop()


# import tkinter as tk
# from tkinter import scrolledtext, messagebox
# import serial
# import serial.tools.list_ports
# import threading
# from queue import Queue
# import datetime
# from tkinter.filedialog import asksaveasfilename

# class SerialDeviceFrame(tk.Frame):
#     """
#     단일 시리얼 장치를 위한 Frame.
#     - 포트 선택, 연결/해제
#     - 명령 전송, 측정(l\n) 전송
#     - ID / ID2 인디케이터
#     - 수신 데이터(백그라운드 스레드) -> Queue -> GUI 업데이트
#     - 측정 기록(measure_history)에 (측정번호, CH1, CH2) 저장 (ID2는 별도 last_known_id2에 저장)
#     """
#     def __init__(self, parent, app_reference, device_label):
#         super().__init__(parent)
#         self.app = app_reference
#         self.device_label = device_label  # 예: "장치1", "장치2" 등

#         # 시리얼 관련
#         self.ser = None
#         self.is_reading = False
#         self.read_thread = None
#         self.data_queue = Queue()

#         # 현재 연결된 포트 (ex: "COM5")
#         self.current_port = None

#         # 사용자 입력 ID (데이터 파싱 시 함께 표시)
#         self.id_var = tk.StringVar(value="")

#         # ID2(장치에서 수신된 값), 측정 기록
#         self.last_known_id2 = ""   # "00009" 등
#         self.measure_count = 0
#         # 측정 이력: [( 측정번호, CH1, CH2 ), … ]
#         self.measure_history = []

#         self.init_ui()

#     def init_ui(self):
#         # 상단 라벨
#         title_label = tk.Label(self, text=f"[{self.device_label}]",
#                                font=('Arial', 12, 'bold'))
#         title_label.pack(pady=(5, 2), anchor='w')

#         # ID 입력
#         id_frame = tk.Frame(self)
#         id_frame.pack(fill='x')
#         tk.Label(id_frame, text="Device ID:").pack(side='left')
#         tk.Entry(id_frame, textvariable=self.id_var, width=10).pack(side='left', padx=(5, 10))

#         # 포트 선택
#         tk.Label(self, text="Select COM Port:").pack(anchor='w')
#         self.com_port_var = tk.StringVar(value="")
#         ports = self.get_com_ports()
#         if ports:
#             self.com_port_var.set(ports[0])
#         self.com_port_menu = tk.OptionMenu(self, self.com_port_var, *ports)
#         self.com_port_menu.pack(fill='x')

#         # Connect / Disconnect
#         button_frame = tk.Frame(self)
#         button_frame.pack(fill='x', pady=2)
#         self.connect_button = tk.Button(button_frame, text="Connect", width=8, command=self.connect_serial)
#         self.connect_button.pack(side='left', padx=(0, 5))
#         self.disconnect_button = tk.Button(button_frame, text="Disconnect", width=10,
#                                            command=self.disconnect_serial, state=tk.DISABLED)
#         self.disconnect_button.pack(side='left')

#         # 명령 전송
#         tk.Label(self, text="Enter command:").pack(anchor='w', pady=(5, 0))
#         self.entry = tk.Entry(self, width=30)
#         self.entry.pack()
#         self.send_button = tk.Button(self, text="Send", command=self.send_command, state=tk.DISABLED)
#         self.send_button.pack(pady=2)

#         # 측정 버튼
#         self.measure_button = tk.Button(self, text="Measure", command=self.measure, state=tk.DISABLED)
#         self.measure_button.pack(pady=2)

#         # ID / ID2 / CH1 / CH2 라벨
#         self.id_label = tk.Label(self, text="ID: ---")
#         self.id_label.pack()
#         self.id2_label = tk.Label(self, text="ID2: ---")
#         self.id2_label.pack()
#         self.ch1_label = tk.Label(self, text="CH1: ---")
#         self.ch1_label.pack()
#         self.ch2_label = tk.Label(self, text="CH2: ---")
#         self.ch2_label.pack()

#         # 출력 창
#         self.output = scrolledtext.ScrolledText(self, width=70, height=8)
#         self.output.pack(pady=5)

#     def get_com_ports(self):
#         """현재 PC에서 사용 가능한 COM 포트 목록 반환"""
#         ports = serial.tools.list_ports.comports()
#         return [p.device for p in ports]

#     def refresh_port_list(self):
#         """포트 목록 갱신 시"""
#         new_ports = self.get_com_ports()
#         menu = self.com_port_menu["menu"]
#         menu.delete(0, "end")
#         for p in new_ports:
#             menu.add_command(label=p, command=lambda value=p: self.com_port_var.set(value))

#         if self.com_port_var.get() not in new_ports:
#             self.com_port_var.set(new_ports[0] if new_ports else "")

#     def connect_serial(self):
#         """Connect 버튼 동작: 글로벌 Baud Rate로 포트 연결, 중복 연결 방지"""
#         port = self.com_port_var.get()
#         if not port:
#             messagebox.showwarning("No Port Selected", f"[{self.device_label}] Please select a COM port.")
#             return

#         if port in self.app.used_ports:
#             messagebox.showwarning("Port In Use", f"Port {port} is already connected by another device.")
#             return

#         try:
#             baud_rate = self.app.global_baud_rate
#             self.ser = serial.Serial(port, baud_rate, timeout=1)
#             self.is_reading = True
#             self.connect_button.config(state=tk.DISABLED)
#             self.disconnect_button.config(state=tk.NORMAL)
#             self.send_button.config(state=tk.NORMAL)
#             self.measure_button.config(state=tk.NORMAL)

#             self.current_port = port
#             self.app.used_ports.add(port)

#             self.output.insert(tk.END, f"Connected to {port} (Baud: {baud_rate})\n")
#             self.output.see(tk.END)

#             # 장치 연결 후 Save 버튼 상태 갱신
#             self.app.update_save_button_state()

#             # 수신 스레드 시작
#             self.read_thread = threading.Thread(target=self.read_from_serial, daemon=True)
#             self.read_thread.start()
#             self.after(50, self.update_gui)

#         except serial.SerialException as e:
#             messagebox.showerror("Serial Port Error", f"Failed to open {port}\nError: {e}")

#     def disconnect_serial(self):
#         """Disconnect 버튼"""
#         if self.ser and self.ser.is_open:
#             self.close()
#             self.output.insert(tk.END, "Disconnected.\n")
#             self.output.see(tk.END)

#         self.connect_button.config(state=tk.NORMAL)
#         self.disconnect_button.config(state=tk.DISABLED)
#         self.send_button.config(state=tk.DISABLED)
#         self.measure_button.config(state=tk.DISABLED)

#         # 연결 해제 후 Save 버튼 상태 갱신
#         self.app.update_save_button_state()

#     def send_command(self):
#         """Send 버튼: 입력 명령어 전송"""
#         if not self.is_connected():
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return

#         cmd = self.entry.get()
#         if cmd:
#             try:
#                 self.ser.write(cmd.encode('utf-8') + b'\n')
#                 self.output.insert(tk.END, f"Sent: {cmd}\n")
#                 self.entry.delete(0, tk.END)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Failed to send command: {e}\n")
#             self.output.see(tk.END)

#     def measure(self):
#         """Measure 버튼: 'l\\n' 전송"""
#         if not self.is_connected():
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return
#         try:
#             self.ser.write(b'l\n')
#             self.output.insert(tk.END, "Sent: l\n")
#         except serial.SerialException as e:
#             self.output.insert(tk.END, f"Failed to send measure command: {e}\n")
#         self.output.see(tk.END)

#     def read_from_serial(self):
#         """백그라운드 스레드: 시리얼 데이터를 읽어서 Queue에 저장"""
#         while self.is_reading:
#             try:
#                 line = self.ser.readline().decode('utf-8', errors='replace').strip()
#                 if line:
#                     self.data_queue.put(line)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Serial read error: {e}\n")
#                 self.output.see(tk.END)
#                 self.is_reading = False
#                 break

#     def update_gui(self):
#         """Queue의 데이터를 꺼내 파싱 & 화면/측정이력 업데이트"""
#         while not self.data_queue.empty():
#             data = self.data_queue.get()
#             self.output.insert(tk.END, f"{data}\n")

#             # ID2 파싱: "ID=...."
#             parsed_id2 = None
#             if "ID=" in data:
#                 try:
#                     start_idx = data.index("ID=") + len("ID=")
#                     parsed_id2 = data[start_idx:].split(",")[0].strip()
#                     self.last_known_id2 = parsed_id2
#                     self.id2_label.config(text=f"ID2: {parsed_id2}")
#                     self.output.insert(tk.END, f"Parsed => ID2={parsed_id2}\n")
#                 except Exception as ex:
#                     self.output.insert(tk.END, f"Error parsing ID2: {ex}\n")

#             # CH1/CH2 파싱: "FastCH:Standard format"
#             if "FastCH:Standard format" in data:
#                 try:
#                     parts = data.split(",")
#                     ch1 = parts[1].strip()
#                     ch2 = parts[2].strip()

#                     current_id = self.id_var.get()
#                     self.id_label.config(text=f"ID: {current_id}")
#                     self.ch1_label.config(text=f"CH1: {ch1}")
#                     self.ch2_label.config(text=f"CH2: {ch2}")

#                     self.measure_count += 1
#                     # 측정 이력: (측정번호, CH1, CH2)
#                     self.measure_history.append((self.measure_count, ch1, ch2))

#                     self.output.insert(
#                         tk.END,
#                         f"Parsed => ID={current_id}, CH1={ch1}, CH2={ch2}, measure_count={self.measure_count}\n"
#                     )
#                 except Exception as e:
#                     self.output.insert(tk.END, f"Error parsing CH1/CH2: {e}\n")

#             self.output.see(tk.END)

#         if self.is_reading:
#             self.after(50, self.update_gui)

#     def is_connected(self):
#         """장치가 연결 중인지 여부"""
#         return (self.ser is not None) and self.ser.is_open

#     def close(self):
#         """이 프레임(장치) Disconnect"""
#         self.is_reading = False
#         if self.ser and self.ser.is_open:
#             try:
#                 self.ser.close()
#             except:
#                 pass
#         if self.current_port in self.app.used_ports:
#             self.app.used_ports.remove(self.current_port)
#         self.current_port = None


# class MultiSerialMonitorApp(tk.Tk):
#     """
#     2행×5열로 최대 10개의 장치를 배치하고,
#     하나 이상 연결되면 Save Data 버튼 활성화,
#     Save Data 버튼을 누르면 파일 대화상자를 띄워서
#     (1행) 각 장치 포트번호 / ID2
#     (2행) 측정횟수 / CH1 / CH2
#     (이후) 실제 측정 기록
#     형태로 저장
#     """
#     def __init__(self):
#         super().__init__()
#         self.title("Multi Serial Monitor (2x5 Grid + Save)")
#         self.geometry("1300x600")

#         # 포트 중복 연결 방지
#         self.used_ports = set()

#         # 글로벌 Baud Rate
#         self.global_baud_rate = 460800

#         # 디바이스 리스트
#         self.device_frames = []

#         # 상단 컨트롤
#         self.init_top_controls()

#         # 2행×5열 컨테이너
#         self.devices_container = tk.Frame(self)
#         self.devices_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)

#         for r in range(2):
#             self.devices_container.rowconfigure(r, weight=1)
#         for c in range(5):
#             self.devices_container.columnconfigure(c, weight=1)

#         self.protocol("WM_DELETE_WINDOW", self.on_closing)

#     def init_top_controls(self):
#         top_frame = tk.Frame(self)
#         top_frame.pack(side="top", fill="x", padx=5, pady=5)

#         tk.Label(top_frame, text="Global Baud Rate:").pack(side='left', padx=(0, 5))
#         self.baud_entry_var = tk.StringVar(value=str(self.global_baud_rate))
#         self.baud_entry = tk.Entry(top_frame, width=10, textvariable=self.baud_entry_var)
#         self.baud_entry.pack(side='left', padx=(0, 10))

#         self.set_baud_button = tk.Button(top_frame, text="Set Baud Rate", command=self.set_baud_rate)
#         self.set_baud_button.pack(side='left', padx=(0, 15))

#         # Connect All
#         self.connect_all_button = tk.Button(top_frame, text="Connect All", command=self.connect_all)
#         self.connect_all_button.pack(side="left", padx=(0, 10))

#         # Measure All
#         self.measure_all_button = tk.Button(top_frame, text="Measure All", command=self.measure_all)
#         self.measure_all_button.pack(side="left", padx=(0, 10))

#         # Refresh Ports
#         self.refresh_ports_button = tk.Button(top_frame, text="Refresh Ports", command=self.refresh_all_ports)
#         self.refresh_ports_button.pack(side="left", padx=(0, 10))

#         # Add / Remove Device
#         self.add_device_button = tk.Button(top_frame, text="Add Device", command=self.add_device)
#         self.add_device_button.pack(side="left", padx=(20, 10))

#         self.remove_device_button = tk.Button(top_frame, text="Remove Device", command=self.remove_device)
#         self.remove_device_button.pack(side="left", padx=(0, 10))

#         # Save Data
#         self.save_button = tk.Button(top_frame, text="Save Data", command=self.save_all_data, state=tk.DISABLED)
#         self.save_button.pack(side="left", padx=(20, 10))

#     def add_device(self):
#         """디바이스 추가 (최대 10개)"""
#         device_index = len(self.device_frames)
#         if device_index >= 10:
#             messagebox.showwarning("Limit Reached", "Cannot add more than 10 devices.")
#             return

#         device_label = f"장치{device_index + 1}"
#         frame = SerialDeviceFrame(self.devices_container, self, device_label)

#         row = device_index // 5
#         col = device_index % 5
#         frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

#         self.device_frames.append(frame)

#     def remove_device(self):
#         """마지막 디바이스를 제거"""
#         if not self.device_frames:
#             return
#         frame = self.device_frames.pop()
#         frame.close()
#         frame.destroy()

#         self.update_save_button_state()

#     def set_baud_rate(self):
#         """Baud Rate 설정"""
#         val = self.baud_entry_var.get()
#         try:
#             new_baud = int(val)
#             self.global_baud_rate = new_baud
#             messagebox.showinfo("Baud Rate", f"Global Baud Rate set to {new_baud}")
#         except ValueError:
#             messagebox.showwarning("Invalid Value", "Please enter a valid integer for Baud Rate.")

#     def connect_all(self):
#         """모든 장치 Connect 시도"""
#         for frame in self.device_frames:
#             if frame.com_port_var.get():
#                 frame.connect_serial()

#     def measure_all(self):
#         """모든 장치 Measure"""
#         for frame in self.device_frames:
#             frame.measure()

#     def refresh_all_ports(self):
#         """모든 장치 포트 목록 갱신"""
#         for frame in self.device_frames:
#             frame.refresh_port_list()

#     def is_any_device_connected(self):
#         """하나라도 연결된 장치가 있는지"""
#         return any(frame.is_connected() for frame in self.device_frames)

#     def update_save_button_state(self):
#         """Save 버튼 활성/비활성 업데이트"""
#         if self.is_any_device_connected():
#             self.save_button.config(state=tk.NORMAL)
#         else:
#             self.save_button.config(state=tk.DISABLED)

#     def save_all_data(self):
#         """
#         사용자가 Save 버튼을 누르면:
#         1) 파일 대화창에서 경로/파일명 선택
#         2) 연결된 장치들만 모아서 아래 형식으로 저장
#            - 1행: ["", 장치1포트, 장치1ID2, 장치2포트, 장치2ID2, ...]
#            - 2행: ["측정횟수", "CH1", "CH2", "CH1", "CH2", ...]
#            - 3행~: 측정 번호별 데이터
#         """
#         connected_devs = [f for f in self.device_frames if f.is_connected()]
#         if not connected_devs:
#             messagebox.showwarning("No Device Connected", "No devices are currently connected.")
#             return

#         # 파일 대화창으로 경로/이름 선택
#         filepath = asksaveasfilename(
#             defaultextension=".txt",
#             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
#         )
#         if not filepath:  # 사용자가 취소
#             return

#         # 1행: "", dev1포트, dev1ID2, dev2포트, dev2ID2, ...
#         header_line1 = [""]
#         for dev in connected_devs:
#             header_line1.append(dev.current_port if dev.current_port else "")
#             header_line1.append(dev.last_known_id2)

#         # 2행: "측정횟수", "CH1", "CH2", "CH1", "CH2", ...
#         header_line2 = ["측정횟수"]
#         for _ in connected_devs:
#             header_line2.append("CH1")
#             header_line2.append("CH2")

#         # 가장 많이 측정된 장치의 측정 횟수
#         max_rows = max((len(dev.measure_history) for dev in connected_devs), default=0)

#         # 실제 데이터
#         data_lines = []
#         for row_idx in range(max_rows):
#             row_data = [str(row_idx + 1)]  # 측정횟수 (1-based)
#             for dev in connected_devs:
#                 if row_idx < len(dev.measure_history):
#                     # (count, ch1, ch2)
#                     _, ch1, ch2 = dev.measure_history[row_idx]
#                     row_data.append(ch1)
#                     row_data.append(ch2)
#                 else:
#                     # 해당 장치는 이 측정 횟수에 데이터 없음
#                     row_data.append("")
#                     row_data.append("")
#             data_lines.append(row_data)

#         # 파일 저장
#         try:
#             with open(filepath, "w", encoding="utf-8") as f:
#                 # 1행
#                 f.write("\t".join(header_line1) + "\n")
#                 # 2행
#                 f.write("\t".join(header_line2) + "\n")
#                 # 3행~
#                 for row_data in data_lines:
#                     f.write("\t".join(row_data) + "\n")

#             messagebox.showinfo("Save Complete", f"Data saved to:\n{filepath}")
#         except OSError as e:
#             messagebox.showerror("Save Error", f"Failed to save data.\nError: {e}")

#     def on_closing(self):
#         """창 종료 시 모든 장치 Disconnect"""
#         for frame in self.device_frames:
#             frame.close()
#         self.destroy()


# if __name__ == "__main__":
#     app = MultiSerialMonitorApp()
#     app.mainloop()



# ## 레코딩 모드 적용
# ##

# import tkinter as tk
# from tkinter import scrolledtext, messagebox
# import serial
# import serial.tools.list_ports
# import threading
# from queue import Queue
# import datetime
# from tkinter.filedialog import asksaveasfilename

# class SerialDeviceFrame(tk.Frame):
#     """
#     단일 시리얼 장치를 위한 Frame.
#     - 포트 선택, 연결/해제
#     - 명령 전송, 측정(l\n) 전송
#     - ID / ID2 인디케이터
#     - 측정 기록(measure_history)에 (측정번호, CH1, CH2) 저장
#     """
#     def __init__(self, parent, app_reference, device_label):
#         super().__init__(parent)
#         self.app = app_reference
#         self.device_label = device_label  # 예: "장치1", "장치2"
        
#         # 시리얼 관련
#         self.ser = None
#         self.is_reading = False
#         self.read_thread = None
#         self.data_queue = Queue()
#         self.current_port = None  # 예: "COM5"

#         # 사용자 입력 ID
#         self.id_var = tk.StringVar(value="")

#         # ID2(장치에서 수신된 값), 측정 기록
#         self.last_known_id2 = ""
#         self.measure_count = 0
#         self.measure_history = []  # [(measure_count, CH1, CH2), ...]

#         self.init_ui()

#     def init_ui(self):
#         # 라벨
#         title_label = tk.Label(self, text=f"[{self.device_label}]", font=('Arial', 12, 'bold'))
#         title_label.pack(pady=(5, 2), anchor='w')

#         # ID 입력
#         id_frame = tk.Frame(self)
#         id_frame.pack(fill='x')
#         tk.Label(id_frame, text="Device ID:").pack(side='left')
#         tk.Entry(id_frame, textvariable=self.id_var, width=10).pack(side='left', padx=(5, 10))

#         # 포트 선택
#         tk.Label(self, text="Select COM Port:").pack(anchor='w')
#         self.com_port_var = tk.StringVar(value="")
#         ports = self.get_com_ports()
#         if ports:
#             self.com_port_var.set(ports[0])
#         self.com_port_menu = tk.OptionMenu(self, self.com_port_var, *ports)
#         self.com_port_menu.pack(fill='x')

#         # Connect / Disconnect
#         button_frame = tk.Frame(self)
#         button_frame.pack(fill='x', pady=2)
#         self.connect_button = tk.Button(button_frame, text="Connect", width=8, command=self.connect_serial)
#         self.connect_button.pack(side='left', padx=(0, 5))
#         self.disconnect_button = tk.Button(button_frame, text="Disconnect", width=10,
#                                            command=self.disconnect_serial, state=tk.DISABLED)
#         self.disconnect_button.pack(side='left')

#         # 명령 전송
#         tk.Label(self, text="Enter command:").pack(anchor='w', pady=(5, 0))
#         self.entry = tk.Entry(self, width=30)
#         self.entry.pack()
#         self.send_button = tk.Button(self, text="Send", command=self.send_command, state=tk.DISABLED)
#         self.send_button.pack(pady=2)

#         # 측정
#         self.measure_button = tk.Button(self, text="Measure", command=self.measure, state=tk.DISABLED)
#         self.measure_button.pack(pady=2)

#         # ID/ID2/CH1/CH2 라벨
#         self.id_label = tk.Label(self, text="ID: ---")
#         self.id_label.pack()
#         self.id2_label = tk.Label(self, text="ID2: ---")
#         self.id2_label.pack()
#         self.ch1_label = tk.Label(self, text="CH1: ---")
#         self.ch1_label.pack()
#         self.ch2_label = tk.Label(self, text="CH2: ---")
#         self.ch2_label.pack()

#         # 출력 창
#         self.output = scrolledtext.ScrolledText(self, width=70, height=8)
#         self.output.pack(pady=5)

#     def get_com_ports(self):
#         ports = serial.tools.list_ports.comports()
#         return [p.device for p in ports]

#     def refresh_port_list(self):
#         """포트 목록 갱신"""
#         new_ports = self.get_com_ports()
#         menu = self.com_port_menu["menu"]
#         menu.delete(0, "end")
#         for p in new_ports:
#             menu.add_command(label=p, command=lambda value=p: self.com_port_var.set(value))

#         if self.com_port_var.get() not in new_ports:
#             self.com_port_var.set(new_ports[0] if new_ports else "")

#     def connect_serial(self):
#         """Connect 버튼: 포트 오픈"""
#         port = self.com_port_var.get()
#         if not port:
#             messagebox.showwarning("No Port Selected", f"[{self.device_label}] Please select a COM port.")
#             return

#         if port in self.app.used_ports:
#             messagebox.showwarning("Port In Use", f"Port {port} is already connected by another device.")
#             return
        
#         try:
#             baud_rate = self.app.global_baud_rate
#             self.ser = serial.Serial(port, baud_rate, timeout=1)
#             self.is_reading = True
#             self.connect_button.config(state=tk.DISABLED)
#             self.disconnect_button.config(state=tk.NORMAL)
#             self.send_button.config(state=tk.NORMAL)
#             self.measure_button.config(state=tk.NORMAL)

#             self.current_port = port
#             self.app.used_ports.add(port)

#             self.output.insert(tk.END, f"Connected to {port} (Baud: {baud_rate})\n")
#             self.output.see(tk.END)

#             # 연결된 뒤, Recoding 버튼 상태 갱신
#             self.app.update_record_button_state()

#             # 수신 스레드 시작
#             self.read_thread = threading.Thread(target=self.read_from_serial, daemon=True)
#             self.read_thread.start()
#             self.after(50, self.update_gui)

#         except serial.SerialException as e:
#             messagebox.showerror("Serial Port Error", f"Failed to open {port}\nError: {e}")

#     def disconnect_serial(self):
#         """Disconnect 버튼"""
#         if self.ser and self.ser.is_open:
#             self.close()
#             self.output.insert(tk.END, "Disconnected.\n")
#             self.output.see(tk.END)

#         self.connect_button.config(state=tk.NORMAL)
#         self.disconnect_button.config(state=tk.DISABLED)
#         self.send_button.config(state=tk.DISABLED)
#         self.measure_button.config(state=tk.DISABLED)

#         # 연결 해제 후, Recoding 버튼 상태 갱신
#         self.app.update_record_button_state()

#     def send_command(self):
#         """Send 버튼"""
#         if not self.is_connected():
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return
#         cmd = self.entry.get()
#         if cmd:
#             try:
#                 self.ser.write(cmd.encode('utf-8') + b'\n')
#                 self.output.insert(tk.END, f"Sent: {cmd}\n")
#                 self.entry.delete(0, tk.END)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Failed to send command: {e}\n")
#             self.output.see(tk.END)

#     def measure(self):
#         """Measure 버튼: 'l\n'"""
#         if not self.is_connected():
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return
#         try:
#             self.ser.write(b'l\n')
#             self.output.insert(tk.END, "Sent: l\n")
#         except serial.SerialException as e:
#             self.output.insert(tk.END, f"Failed to send measure command: {e}\n")
#         self.output.see(tk.END)

#     def read_from_serial(self):
#         """백그라운드 스레드: 시리얼 읽기"""
#         while self.is_reading:
#             try:
#                 line = self.ser.readline().decode('utf-8', errors='replace').strip()
#                 if line:
#                     self.data_queue.put(line)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Serial read error: {e}\n")
#                 self.output.see(tk.END)
#                 self.is_reading = False
#                 break

#     def update_gui(self):
#         """Queue 데이터를 꺼내 파싱, 기록"""
#         while not self.data_queue.empty():
#             data = self.data_queue.get()
#             self.output.insert(tk.END, f"{data}\n")

#             # ID2 파싱
#             if "ID=" in data:
#                 try:
#                     idx = data.index("ID=") + len("ID=")
#                     parsed_id2 = data[idx:].split(",")[0].strip()
#                     self.last_known_id2 = parsed_id2
#                     self.id2_label.config(text=f"ID2: {parsed_id2}")
#                     self.output.insert(tk.END, f"Parsed => ID2={parsed_id2}\n")
#                 except Exception as ex:
#                     self.output.insert(tk.END, f"Error parsing ID2: {ex}\n")

#             # CH1/CH2 파싱
#             if "FastCH:Standard format" in data:
#                 try:
#                     parts = data.split(",")
#                     ch1 = parts[1].strip()
#                     ch2 = parts[2].strip()

#                     current_id = self.id_var.get()
#                     self.id_label.config(text=f"ID: {current_id}")
#                     self.ch1_label.config(text=f"CH1: {ch1}")
#                     self.ch2_label.config(text=f"CH2: {ch2}")

#                     self.measure_count += 1
#                     self.measure_history.append((self.measure_count, ch1, ch2))

#                     self.output.insert(
#                         tk.END,
#                         f"Parsed => ID={current_id}, CH1={ch1}, CH2={ch2}, measure_count={self.measure_count}\n"
#                     )
#                 except Exception as e:
#                     self.output.insert(tk.END, f"Error parsing CH1/CH2: {e}\n")

#             self.output.see(tk.END)

#         if self.is_reading:
#             self.after(50, self.update_gui)

#     def is_connected(self):
#         """연결 여부"""
#         return (self.ser is not None) and self.ser.is_open

#     def close(self):
#         """Disconnect 처리"""
#         self.is_reading = False
#         if self.ser and self.ser.is_open:
#             try:
#                 self.ser.close()
#             except:
#                 pass
#         if self.current_port in self.app.used_ports:
#             self.app.used_ports.remove(self.current_port)
#         self.current_port = None

#     def clear_measure_history(self):
#         """녹화(Record) 시작 시 기존 누적값 초기화"""
#         self.measure_count = 0
#         self.measure_history.clear()


# class MultiSerialMonitorApp(tk.Tk):
#     """
#     2행×5열로 최대 10개의 장치를 배치.
#     'Save Data' 버튼 -> 파일 지정 + 모든 장치 측정기록 초기화 -> 버튼이 'Recording' 으로 바뀜
#     'Recording' 버튼 -> 현재 측정된 값들을 파일로 저장 -> 버튼 'Save Data'로 복귀
#     """
#     def __init__(self):
#         super().__init__()
#         self.title("Multi Serial Monitor (Recording Mode)")
#         self.geometry("1300x600")

#         # 포트 중복 체크
#         self.used_ports = set()
#         # Baud rate
#         self.global_baud_rate = 460800
#         # 장치 목록
#         self.device_frames = []

#         # 'Recording' 모드 상태 플래그
#         self.is_recording = False
#         # 현재 녹화 중인 파일 경로(없으면 None)
#         self.recording_filepath = None

#         self.init_top_controls()

#         # 컨테이너 (2행×5열)
#         self.devices_container = tk.Frame(self)
#         self.devices_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)
#         for r in range(2):
#             self.devices_container.rowconfigure(r, weight=1)
#         for c in range(5):
#             self.devices_container.columnconfigure(c, weight=1)

#         self.protocol("WM_DELETE_WINDOW", self.on_closing)

#     def init_top_controls(self):
#         top_frame = tk.Frame(self)
#         top_frame.pack(side="top", fill="x", padx=5, pady=5)

#         # Baud
#         tk.Label(top_frame, text="Global Baud Rate:").pack(side='left', padx=(0, 5))
#         self.baud_entry_var = tk.StringVar(value=str(self.global_baud_rate))
#         self.baud_entry = tk.Entry(top_frame, width=10, textvariable=self.baud_entry_var)
#         self.baud_entry.pack(side='left', padx=(0, 10))

#         self.set_baud_button = tk.Button(top_frame, text="Set Baud Rate", command=self.set_baud_rate)
#         self.set_baud_button.pack(side='left', padx=(0, 15))

#         # Connect All
#         self.connect_all_button = tk.Button(top_frame, text="Connect All", command=self.connect_all)
#         self.connect_all_button.pack(side="left", padx=(0, 10))

#         # Measure All
#         self.measure_all_button = tk.Button(top_frame, text="Measure All", command=self.measure_all)
#         self.measure_all_button.pack(side="left", padx=(0, 10))

#         # Refresh Ports
#         self.refresh_ports_button = tk.Button(top_frame, text="Refresh Ports", command=self.refresh_all_ports)
#         self.refresh_ports_button.pack(side="left", padx=(0, 10))

#         # Add / Remove
#         self.add_device_button = tk.Button(top_frame, text="Add Device", command=self.add_device)
#         self.add_device_button.pack(side="left", padx=(20, 10))

#         self.remove_device_button = tk.Button(top_frame, text="Remove Device", command=self.remove_device)
#         self.remove_device_button.pack(side="left", padx=(0, 10))

#         # Save Data (or Recording) 버튼
#         self.record_button = tk.Button(top_frame, text="Save Data", command=self.toggle_recording, state=tk.DISABLED)
#         self.record_button.pack(side="left", padx=(20, 10))

#     def add_device(self):
#         device_index = len(self.device_frames)
#         if device_index >= 10:
#             messagebox.showwarning("Limit Reached", "Cannot add more than 10 devices.")
#             return

#         device_label = f"장치{device_index + 1}"
#         frame = SerialDeviceFrame(self.devices_container, self, device_label)

#         row = device_index // 5
#         col = device_index % 5
#         frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

#         self.device_frames.append(frame)
#         # 새로 장치 추가해도 연결되기 전까지는 영향 없음

#     def remove_device(self):
#         if not self.device_frames:
#             return
#         frame = self.device_frames.pop()
#         frame.close()
#         frame.destroy()
#         self.update_record_button_state()

#     def set_baud_rate(self):
#         val = self.baud_entry_var.get()
#         try:
#             new_baud = int(val)
#             self.global_baud_rate = new_baud
#             messagebox.showinfo("Baud Rate", f"Global Baud Rate set to {new_baud}")
#         except ValueError:
#             messagebox.showwarning("Invalid Value", "Please enter a valid integer for Baud Rate.")

#     def connect_all(self):
#         for frame in self.device_frames:
#             if frame.com_port_var.get():
#                 frame.connect_serial()

#     def measure_all(self):
#         for frame in self.device_frames:
#             frame.measure()

#     def refresh_all_ports(self):
#         for frame in self.device_frames:
#             frame.refresh_port_list()

#     def is_any_device_connected(self):
#         """연결된 장치가 하나라도 있는지"""
#         return any(f.is_connected() for f in self.device_frames)

#     def update_record_button_state(self):
#         """
#         녹화 버튼 상태 갱신:
#         - 하나라도 연결된 장치가 있으면 활성화
#         - 그렇지 않으면 비활성화 & 녹화 중이라면 종료?
#         """
#         if self.is_any_device_connected():
#             self.record_button.config(state=tk.NORMAL)
#         else:
#             self.record_button.config(state=tk.DISABLED)

#     def toggle_recording(self):
#         """
#         Save Data(녹화 시작) → 파일 지정 → measure_history 모두 초기화 → 버튼 "Recording"
#         Recording(녹화 종료) → 파일에 기록 → 버튼 "Save Data"
#         """
#         if not self.is_recording:
#             # 현재 'Save Data' 상태
#             # 파일 대화창
#             filepath = asksaveasfilename(
#                 defaultextension=".txt",
#                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
#             )
#             if not filepath:
#                 return  # 취소
#             self.recording_filepath = filepath

#             # 측정 기록 초기화
#             for frame in self.device_frames:
#                 frame.clear_measure_history()

#             self.is_recording = True
#             self.record_button.config(text="Recording")
#         else:
#             # 현재 'Recording' 상태 -> 파일에 저장 후 종료
#             self.finalize_recording()
#             # 다시 'Save Data' 상태로
#             self.is_recording = False
#             self.recording_filepath = None
#             self.record_button.config(text="Save Data")

#     def finalize_recording(self):
#         """녹화 종료 시점에, 지금까지 측정된 값들을 recording_filepath에 저장"""
#         connected_devs = [f for f in self.device_frames if f.is_connected()]
#         if not connected_devs:
#             messagebox.showwarning("No Device Connected", "No devices are currently connected.")
#             return

#         if not self.recording_filepath:
#             return  # 파일 지정 안 되어 있으면 무시

#         # 헤더 구성
#         # 1행: ["", 포트, ID2, ...]
#         line1 = [""]
#         for dev in connected_devs:
#             line1.append(dev.current_port if dev.current_port else "")
#             line1.append(dev.last_known_id2)

#         # 2행: ["측정횟수", "CH1","CH2", "CH1","CH2", ...]
#         line2 = ["Count"]
#         for _ in connected_devs:
#             line2.append("CH1")
#             line2.append("CH2")

#         # 가장 많이 측정된 개수
#         max_rows = max(len(dev.measure_history) for dev in connected_devs)

#         # 데이터 라인
#         data_lines = []
#         for row_idx in range(max_rows):
#             row_data = [str(row_idx + 1)]
#             for dev in connected_devs:
#                 if row_idx < len(dev.measure_history):
#                     mcount, ch1, ch2 = dev.measure_history[row_idx]
#                     row_data.append(ch1)
#                     row_data.append(ch2)
#                 else:
#                     row_data.append("")
#                     row_data.append("")
#             data_lines.append(row_data)

#         # 파일 쓰기
#         try:
#             with open(self.recording_filepath, "w", encoding="utf-8") as f:
#                 f.write("\t".join(line1) + "\n")
#                 f.write("\t".join(line2) + "\n")
#                 for row_data in data_lines:
#                     f.write("\t".join(row_data) + "\n")

#             messagebox.showinfo("Save Complete", f"Data saved to:\n{self.recording_filepath}")
#         except OSError as e:
#             messagebox.showerror("Save Error", f"Failed to save data.\nError: {e}")

#     def on_closing(self):
#         for frame in self.device_frames:
#             frame.close()
#         self.destroy()


# if __name__ == "__main__":
#     app = MultiSerialMonitorApp()
#     app.mainloop()





# 측정값 입력열 추가 ,  사용자가 직접 입력

# measure ALL 버튼 적용

# import tkinter as tk
# from tkinter import scrolledtext, messagebox
# import serial
# import serial.tools.list_ports
# import threading
# from queue import Queue
# from tkinter.filedialog import asksaveasfilename

# class SerialDeviceFrame(tk.Frame):
#     """
#     단일 시리얼 장치를 위한 Frame.
#     - 포트 선택, 연결/해제
#     - ID/ID2 표시
#     - measure_history[count] = (ch1, ch2)
#     - pending_measure_count: Measure All에서 전달받은 측정 횟수(응답 매칭용)
#     """
#     def __init__(self, parent, app_reference, device_label):
#         super().__init__(parent)
#         self.app = app_reference
#         self.device_label = device_label  # 예: "장치1", "장치2", ...

#         # 시리얼 관련
#         self.ser = None
#         self.is_reading = False
#         self.read_thread = None
#         self.data_queue = Queue()
#         self.current_port = None  # 예: "COM5"

#         # 사용자 입력 ID
#         self.id_var = tk.StringVar(value="")

#         # 수신된 ID2
#         self.last_known_id2 = ""

#         # 측정 이력: { measure_count(int): (ch1, ch2) }
#         self.measure_history = {}

#         # Measure All 시 전달받은 측정 횟수를 저장하여, FastCH 응답 때 매칭
#         self.pending_measure_count = None

#         self.init_ui()

#     def init_ui(self):
#         # 상단 라벨 (장치명)
#         label_title = tk.Label(self, text=f"[{self.device_label}]", font=('Arial', 12, 'bold'))
#         label_title.pack(pady=(5, 2), anchor='w')

#         # ID 입력
#         id_frame = tk.Frame(self)
#         id_frame.pack(fill='x')
#         tk.Label(id_frame, text="Device ID:").pack(side='left')
#         tk.Entry(id_frame, textvariable=self.id_var, width=10).pack(side='left', padx=(5, 10))

#         # 포트 선택
#         tk.Label(self, text="Select COM Port:").pack(anchor='w')
#         self.com_port_var = tk.StringVar(value="")
#         ports = self.get_com_ports()
#         if ports:
#             self.com_port_var.set(ports[0])
#         self.com_port_menu = tk.OptionMenu(self, self.com_port_var, *ports)
#         self.com_port_menu.pack(fill='x')

#         # Connect / Disconnect
#         btn_frame = tk.Frame(self)
#         btn_frame.pack(fill='x', pady=2)
#         self.connect_button = tk.Button(btn_frame, text="Connect", width=8, command=self.connect_serial)
#         self.connect_button.pack(side='left', padx=(0, 5))
#         self.disconnect_button = tk.Button(btn_frame, text="Disconnect", width=10,
#                                            command=self.disconnect_serial, state=tk.DISABLED)
#         self.disconnect_button.pack(side='left')

#         # 명령 전송
#         tk.Label(self, text="Enter command:").pack(anchor='w', pady=(5, 0))
#         self.entry = tk.Entry(self, width=30)
#         self.entry.pack()
#         self.send_button = tk.Button(self, text="Send", command=self.send_command, state=tk.DISABLED)
#         self.send_button.pack(pady=2)

#         # 측정 버튼 (개별)
#         self.measure_button = tk.Button(self, text="Measure", command=self.measure, state=tk.DISABLED)
#         self.measure_button.pack(pady=2)

#         # ID/ID2/CH1/CH2 라벨
#         self.id_label = tk.Label(self, text="ID: ---")
#         self.id_label.pack()
#         self.id2_label = tk.Label(self, text="ID2: ---")
#         self.id2_label.pack()
#         self.ch1_label = tk.Label(self, text="CH1: ---")
#         self.ch1_label.pack()
#         self.ch2_label = tk.Label(self, text="CH2: ---")
#         self.ch2_label.pack()

#         # 출력창
#         self.output = scrolledtext.ScrolledText(self, width=70, height=8)
#         self.output.pack(pady=5)

#     def get_com_ports(self):
#         ports = serial.tools.list_ports.comports()
#         return [p.device for p in ports]

#     def refresh_port_list(self):
#         """포트 목록 갱신"""
#         new_ports = self.get_com_ports()
#         menu = self.com_port_menu["menu"]
#         menu.delete(0, "end")
#         for p in new_ports:
#             menu.add_command(label=p, command=lambda v=p: self.com_port_var.set(v))
#         if self.com_port_var.get() not in new_ports:
#             self.com_port_var.set(new_ports[0] if new_ports else "")

#     def connect_serial(self):
#         port = self.com_port_var.get()
#         if not port:
#             messagebox.showwarning("No Port Selected", f"[{self.device_label}] Please select a COM port.")
#             return

#         # 중복 연결 방지
#         if port in self.app.used_ports:
#             messagebox.showwarning("Port In Use", f"Port {port} is already connected by another device.")
#             return

#         try:
#             baud_rate = self.app.global_baud_rate
#             self.ser = serial.Serial(port, baud_rate, timeout=1)
#             self.is_reading = True

#             self.connect_button.config(state=tk.DISABLED)
#             self.disconnect_button.config(state=tk.NORMAL)
#             self.send_button.config(state=tk.NORMAL)
#             self.measure_button.config(state=tk.NORMAL)

#             self.current_port = port
#             self.app.used_ports.add(port)

#             self.output.insert(tk.END, f"Connected to {port} (Baud: {baud_rate})\n")
#             self.output.see(tk.END)

#             # 연결 후 Record 버튼 상태 갱신
#             self.app.update_record_button_state()

#             # 수신 스레드 시작
#             self.read_thread = threading.Thread(target=self.read_from_serial, daemon=True)
#             self.read_thread.start()
#             self.after(50, self.update_gui)

#         except serial.SerialException as e:
#             messagebox.showerror("Serial Port Error", f"Failed to open {port}\nError: {e}")

#     def disconnect_serial(self):
#         if self.ser and self.ser.is_open:
#             self.close()
#             self.output.insert(tk.END, "Disconnected.\n")
#             self.output.see(tk.END)

#         self.connect_button.config(state=tk.NORMAL)
#         self.disconnect_button.config(state=tk.DISABLED)
#         self.send_button.config(state=tk.DISABLED)
#         self.measure_button.config(state=tk.DISABLED)

#         self.app.update_record_button_state()

#     def send_command(self):
#         if not self.is_connected():
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return
#         cmd = self.entry.get()
#         if cmd:
#             try:
#                 self.ser.write(cmd.encode('utf-8') + b'\n')
#                 self.output.insert(tk.END, f"Sent: {cmd}\n")
#                 self.entry.delete(0, tk.END)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Failed to send command: {e}\n")
#             self.output.see(tk.END)

#     def measure(self):
#         """개별 측정: l\n 전송"""
#         if not self.is_connected():
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return
#         try:
#             self.ser.write(b'l\n')
#             self.output.insert(tk.END, "Sent: l\n")
#         except serial.SerialException as e:
#             self.output.insert(tk.END, f"Failed to send measure command: {e}\n")
#         self.output.see(tk.END)

#     def do_measure_with_count(self, measure_count):
#         """
#         Measure All에서 호출.
#         이 측정에 대응하는 measure_count를 pending으로 저장 -> 다음 FastCH 응답에 매칭
#         """
#         if not self.is_connected():
#             return
#         self.pending_measure_count = measure_count
#         try:
#             self.ser.write(b'l\n')
#             self.output.insert(tk.END, f"Sent measure command (count={measure_count})\n")
#             self.output.see(tk.END)
#         except serial.SerialException as e:
#             self.output.insert(tk.END, f"Failed to send measure command: {e}\n")
#             self.output.see(tk.END)

#     def read_from_serial(self):
#         while self.is_reading:
#             try:
#                 line = self.ser.readline().decode('utf-8', errors='replace').strip()
#                 if line:
#                     self.data_queue.put(line)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Serial read error: {e}\n")
#                 self.output.see(tk.END)
#                 self.is_reading = False
#                 break

#     def update_gui(self):
#         while not self.data_queue.empty():
#             data = self.data_queue.get()
#             self.output.insert(tk.END, f"{data}\n")

#             # ID2 파싱
#             if "ID=" in data:
#                 try:
#                     idx = data.index("ID=") + len("ID=")
#                     parsed_id2 = data[idx:].split(",")[0].strip()
#                     self.last_known_id2 = parsed_id2
#                     self.id2_label.config(text=f"ID2: {parsed_id2}")
#                     self.output.insert(tk.END, f"Parsed => ID2={parsed_id2}\n")
#                 except Exception as ex:
#                     self.output.insert(tk.END, f"Error parsing ID2: {ex}\n")

#             # CH1/CH2 파싱
#             if "FastCH:Standard format" in data:
#                 try:
#                     parts = data.split(",")
#                     ch1 = parts[1].strip()
#                     ch2 = parts[2].strip()

#                     current_id = self.id_var.get()
#                     self.id_label.config(text=f"ID: {current_id}")
#                     self.ch1_label.config(text=f"CH1: {ch1}")
#                     self.ch2_label.config(text=f"CH2: {ch2}")

#                     # Measure All에서 전달받은 count와 매칭
#                     if self.pending_measure_count is not None:
#                         ckey = self.pending_measure_count
#                         self.measure_history[ckey] = (ch1, ch2)
#                         self.output.insert(
#                             tk.END,
#                             f"Parsed => ID={current_id}, CH1={ch1}, CH2={ch2}, measure_count={ckey}\n"
#                         )
#                         self.pending_measure_count = None
#                     else:
#                         # 개별 Measure 등
#                         new_index = len(self.measure_history) + 1
#                         self.measure_history[new_index] = (ch1, ch2)
#                         self.output.insert(
#                             tk.END,
#                             f"(No pending) => ID={current_id}, measure_index={new_index}\n"
#                         )
#                 except Exception as e:
#                     self.output.insert(tk.END, f"Error parsing CH1/CH2: {e}\n")

#             self.output.see(tk.END)

#         if self.is_reading:
#             self.after(50, self.update_gui)

#     def is_connected(self):
#         return (self.ser is not None) and self.ser.is_open

#     def close(self):
#         self.is_reading = False
#         if self.ser and self.ser.is_open:
#             try:
#                 self.ser.close()
#             except:
#                 pass
#         if self.current_port in self.app.used_ports:
#             self.app.used_ports.remove(self.current_port)
#         self.current_port = None

#     def clear_measure_history(self):
#         self.measure_history.clear()
#         self.pending_measure_count = None


# class MultiSerialMonitorApp(tk.Tk):
#     """
#     2행×5열로 최대 10개 장치.
#     - Save Data → 파일 지정 & 모든 기록 초기화 → 버튼 "Recording"
#     - Recording → 지금까지의 데이터 파일로 저장 → 버튼 "Save Data"

#     [파일 저장 형식]
#       1행: ["", ""] + (port, ID2)*N
#       2행: ["Count", "Condition"] + (CH1, CH2)*N
#       3행 이후: count, condition, dev1(CH1,CH2), dev2(CH1,CH2)...

#     - measure_all() 시 전역 measure_count 증가 + Condition값 저장 + 각 장치에 do_measure_with_count(count)
#     - 장치는 FastCH 응답 시 measure_history[count] = (ch1, ch2)
#     """
#     def __init__(self):
#         super().__init__()
#         self.title("Multi Serial Monitor (Condition + fix measure_count mismatch)")
#         self.geometry("1300x700")

#         self.used_ports = set()
#         self.global_baud_rate = 460800

#         # 여러 장치 목록
#         self.device_frames = []

#         # 녹화 모드
#         self.is_recording = False
#         self.recording_filepath = None

#         # Condition 리스트
#         self.condition_values = []
#         # 전역 측정 횟수
#         self.global_measure_count = 0

#         self.init_top_controls()

#         # 2행×5열 컨테이너
#         self.devices_container = tk.Frame(self)
#         self.devices_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)
#         for r in range(2):
#             self.devices_container.rowconfigure(r, weight=1)
#         for c in range(5):
#             self.devices_container.columnconfigure(c, weight=1)

#         self.protocol("WM_DELETE_WINDOW", self.on_closing)

#     def init_top_controls(self):
#         top_frame = tk.Frame(self)
#         top_frame.pack(side="top", fill="x", padx=5, pady=5)

#         # Baud
#         tk.Label(top_frame, text="Global Baud Rate:").pack(side='left', padx=(0, 5))
#         self.baud_var = tk.StringVar(value=str(self.global_baud_rate))
#         baud_entry = tk.Entry(top_frame, width=10, textvariable=self.baud_var)
#         baud_entry.pack(side='left', padx=(0, 10))

#         btn_baud = tk.Button(top_frame, text="Set Baud Rate", command=self.set_baud_rate)
#         btn_baud.pack(side='left', padx=(0, 15))

#         # Condition + Measure All
#         self.condition_var = tk.StringVar()
#         tk.Label(top_frame, text="Condition:").pack(side='left', padx=(10, 5))
#         condition_entry = tk.Entry(top_frame, textvariable=self.condition_var, width=20)
#         condition_entry.pack(side='left', padx=(0, 10))

#         btn_measure_all = tk.Button(top_frame, text="Measure All", command=self.measure_all)
#         btn_measure_all.pack(side="left", padx=(0, 15))

#         # Refresh Ports
#         btn_refresh = tk.Button(top_frame, text="Refresh Ports", command=self.refresh_all_ports)
#         btn_refresh.pack(side="left", padx=(0, 10))

#         # Add / Remove
#         btn_add = tk.Button(top_frame, text="Add Device", command=self.add_device)
#         btn_add.pack(side='left', padx=(20, 10))
#         btn_remove = tk.Button(top_frame, text="Remove Device", command=self.remove_device)
#         btn_remove.pack(side='left', padx=(0, 10))

#         # Save/Recording 버튼
#         self.record_button = tk.Button(top_frame, text="Save Data", command=self.toggle_recording, state=tk.DISABLED)
#         self.record_button.pack(side="left", padx=(20, 10))

#     def add_device(self):
#         idx = len(self.device_frames)
#         if idx >= 10:
#             messagebox.showwarning("Limit Reached", "Cannot add more than 10 devices.")
#             return
#         label = f"장치{idx + 1}"
#         frame = SerialDeviceFrame(self.devices_container, self, label)
#         row = idx // 5
#         col = idx % 5
#         frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
#         self.device_frames.append(frame)

#     def remove_device(self):
#         if not self.device_frames:
#             return
#         frame = self.device_frames.pop()
#         frame.close()
#         frame.destroy()
#         self.update_record_button_state()

#     def set_baud_rate(self):
#         val = self.baud_var.get()
#         try:
#             new_baud = int(val)
#             self.global_baud_rate = new_baud
#             messagebox.showinfo("Baud Rate", f"Global Baud Rate set to {new_baud}")
#         except ValueError:
#             messagebox.showwarning("Invalid Value", "Please enter a valid integer for Baud Rate.")

#     def measure_all(self):
#         """
#         1) global_measure_count += 1
#         2) condition_var.get() -> condition_values
#         3) 연결된 장치: do_measure_with_count( measure_count )
#         """
#         connected = [f for f in self.device_frames if f.is_connected()]
#         if not connected:
#             messagebox.showwarning("No Device Connected", "No devices are currently connected.")
#             return

#         self.global_measure_count += 1
#         cond = self.condition_var.get()
#         self.condition_values.append(cond)

#         for dev in connected:
#             dev.do_measure_with_count(self.global_measure_count)

#     def refresh_all_ports(self):
#         for f in self.device_frames:
#             f.refresh_port_list()

#     def is_any_device_connected(self):
#         return any(f.is_connected() for f in self.device_frames)

#     def update_record_button_state(self):
#         """Save Data/Recording 버튼 활성/비활성"""
#         if self.is_any_device_connected():
#             self.record_button.config(state=tk.NORMAL)
#         else:
#             self.record_button.config(state=tk.DISABLED)

#     def toggle_recording(self):
#         """
#         Save Data -> 파일 지정 + 측정 기록 초기화 -> 버튼 "Recording"
#         Recording -> 지금까지 데이터 파일로 저장 -> 버튼 "Save Data"
#         """
#         if not self.is_recording:
#             # 현재 'Save Data' 상태
#             filepath = asksaveasfilename(
#                 defaultextension=".txt",
#                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
#             )
#             if not filepath:
#                 return
#             self.recording_filepath = filepath

#             # 기존 기록 삭제
#             for f in self.device_frames:
#                 f.clear_measure_history()
#             self.condition_values.clear()
#             self.global_measure_count = 0

#             self.is_recording = True
#             self.record_button.config(text="Recording")
#         else:
#             # 'Recording' 상태 -> finalize
#             self.finalize_recording()
#             self.is_recording = False
#             self.recording_filepath = None
#             self.record_button.config(text="Save Data")

#     def finalize_recording(self):
#         connected = [f for f in self.device_frames if f.is_connected()]
#         if not connected:
#             messagebox.showwarning("No Device Connected", "No devices are currently connected.")
#             return
#         if not self.recording_filepath:
#             return

#         # 1행
#         line1 = ["", ""]
#         for dev in connected:
#             line1.append(dev.current_port if dev.current_port else "")
#             line1.append(dev.last_known_id2)

#         # 2행
#         line2 = ["Count", "Condition"]
#         for _ in connected:
#             line2.append("CH1")
#             line2.append("CH2")

#         # 데이터
#         data_lines = []
#         for idx in range(self.global_measure_count):
#             row_data = []
#             # Count
#             row_data.append(str(idx + 1))
#             # Condition
#             cond_val = self.condition_values[idx] if idx < len(self.condition_values) else ""
#             row_data.append(cond_val)

#             for dev in connected:
#                 key = idx + 1
#                 if key in dev.measure_history:
#                     ch1, ch2 = dev.measure_history[key]
#                     row_data.append(ch1)
#                     row_data.append(ch2)
#                 else:
#                     row_data.append("")
#                     row_data.append("")
#             data_lines.append(row_data)

#         # 파일 쓰기
#         try:
#             with open(self.recording_filepath, "w", encoding="utf-8") as f:
#                 f.write("\t".join(line1) + "\n")
#                 f.write("\t".join(line2) + "\n")
#                 for row_data in data_lines:
#                     f.write("\t".join(row_data) + "\n")

#             messagebox.showinfo("Save Complete", f"Data saved to:\n{self.recording_filepath}")
#         except OSError as e:
#             messagebox.showerror("Save Error", f"Failed to save data.\nError: {e}")

#     def on_closing(self):
#         for f in self.device_frames:
#             f.close()
#         self.destroy()


# if __name__ == "__main__":
#     app = MultiSerialMonitorApp()
#     app.mainloop()




##########################

#### 12/24 현재 특성 평가용 프로그램 
#### 장치 연결시, save data 활성화

# import tkinter as tk
# from tkinter import scrolledtext, messagebox
# import serial
# import serial.tools.list_ports
# import threading
# from queue import Queue
# from tkinter.filedialog import asksaveasfilename

# class SerialDeviceFrame(tk.Frame):
#     """
#     단일 시리얼 장치를 위한 Frame.
#     - 포트 선택, 연결/해제
#     - ID, ID2 표시
#     - measure_history[count] = (ch1, ch2)
#     - pending_measure_count: Measure All에서 전달받은 측정 횟수(응답 매칭)
#     """
#     def __init__(self, parent, app_reference, device_label, available_ports):
#         """
#         :param available_ports: 이미 연결된 포트를 제외한 목록 (OptionMenu에 표시)
#         """
#         super().__init__(parent)
#         self.app = app_reference
#         self.device_label = device_label

#         # 시리얼 관련
#         self.ser = None
#         self.is_reading = False
#         self.read_thread = None
#         self.data_queue = Queue()
#         self.current_port = None  # 예: "COM5"

#         # 사용자 입력 ID
#         self.id_var = tk.StringVar(value="")

#         # 수신된 ID2
#         self.last_known_id2 = ""

#         # 측정 이력: measure_history[count] = (ch1, ch2)
#         self.measure_history = {}

#         # Measure All 시 "이번 측정 번호"를 임시 저장
#         self.pending_measure_count = None

#         self.init_ui(available_ports)

#     def init_ui(self, available_ports):
#         # 프레임 라벨 (장치명)
#         label_title = tk.Label(self, text=f"[{self.device_label}]", font=('Arial', 12, 'bold'))
#         label_title.pack(pady=(5, 2), anchor='w')

#         # ID 입력
#         id_frame = tk.Frame(self)
#         id_frame.pack(fill='x')
#         tk.Label(id_frame, text="Device ID:").pack(side='left')
#         tk.Entry(id_frame, textvariable=self.id_var, width=10).pack(side='left', padx=(5, 10))

#         # 포트 선택
#         tk.Label(self, text="Select COM Port:").pack(anchor='w')
#         self.com_port_var = tk.StringVar(value="")
#         # available_ports는 이미 "사용 중인 포트"가 제외된 목록
#         if available_ports:
#             self.com_port_var.set(available_ports[0])  
#         self.com_port_menu = tk.OptionMenu(self, self.com_port_var, *available_ports)
#         self.com_port_menu.pack(fill='x')

#         # Connect / Disconnect
#         btn_frame = tk.Frame(self)
#         btn_frame.pack(fill='x', pady=2)
#         self.connect_button = tk.Button(btn_frame, text="Connect", width=8, command=self.connect_serial)
#         self.connect_button.pack(side='left', padx=(0, 5))
#         self.disconnect_button = tk.Button(btn_frame, text="Disconnect", width=10,
#                                            command=self.disconnect_serial, state=tk.DISABLED)
#         self.disconnect_button.pack(side='left')

#         # 명령 전송
#         tk.Label(self, text="Enter command:").pack(anchor='w', pady=(5, 0))
#         self.entry = tk.Entry(self, width=30)
#         self.entry.pack()
#         self.send_button = tk.Button(self, text="Send", command=self.send_command, state=tk.DISABLED)
#         self.send_button.pack(pady=2)

#         # (개별) 측정 버튼
#         self.measure_button = tk.Button(self, text="Measure", command=self.measure, state=tk.DISABLED)
#         self.measure_button.pack(pady=2)

#         # ID / ID2 / CH1 / CH2 라벨
#         self.id_label = tk.Label(self, text="ID: ---")
#         self.id_label.pack()
#         self.id2_label = tk.Label(self, text="ID2: ---")
#         self.id2_label.pack()
#         self.ch1_label = tk.Label(self, text="CH1: ---")
#         self.ch1_label.pack()
#         self.ch2_label = tk.Label(self, text="CH2: ---")
#         self.ch2_label.pack()

#         # 출력창
#         self.output = scrolledtext.ScrolledText(self, width=70, height=8)
#         self.output.pack(pady=5)

#     def get_com_ports(self):
#         """현재 PC에서 사용 가능한 전체 포트 목록(실제 하드웨어)"""
#         return [p.device for p in serial.tools.list_ports.comports()]

#     def connect_serial(self):
#         """
#         Connect 버튼:
#          - self.com_port_var.get() 포트를 오픈
#          - 열리면 메인 앱 used_ports에 추가
#         """
#         port = self.com_port_var.get()
#         if not port:
#             messagebox.showwarning("No Port Selected", f"[{self.device_label}] Please select a COM port.")
#             return

#         # 이미 다른 장치가 connect 중인 포트인지 다시 확인
#         if port in self.app.used_ports:
#             messagebox.showwarning("Port In Use", f"Port {port} is already connected by another device.")
#             return

#         try:
#             baud_rate = self.app.global_baud_rate
#             self.ser = serial.Serial(port, baud_rate, timeout=1)
#             self.is_reading = True

#             self.connect_button.config(state=tk.DISABLED)
#             self.disconnect_button.config(state=tk.NORMAL)
#             self.send_button.config(state=tk.NORMAL)
#             self.measure_button.config(state=tk.NORMAL)

#             self.current_port = port
#             self.app.used_ports.add(port)

#             self.output.insert(tk.END, f"Connected to {port} (Baud: {baud_rate})\n")
#             self.output.see(tk.END)

#             # *** 중요: 연결 성공 후 메인 앱에 알려 Save Data 버튼 활성화 가능하도록 함 ***
#             self.app.update_record_button_state()

#             # 수신 스레드
#             self.read_thread = threading.Thread(target=self.read_from_serial, daemon=True)
#             self.read_thread.start()
#             self.after(50, self.update_gui)

#         except serial.SerialException as e:
#             messagebox.showerror("Serial Port Error", f"Failed to open {port}\nError: {e}")

#     def disconnect_serial(self):
#         """
#         Disconnect 버튼:
#          - 포트 닫고 used_ports에서 제거
#         """
#         if self.ser and self.ser.is_open:
#             self.close()
#             self.output.insert(tk.END, "Disconnected.\n")
#             self.output.see(tk.END)

#         self.connect_button.config(state=tk.NORMAL)
#         self.disconnect_button.config(state=tk.DISABLED)
#         self.send_button.config(state=tk.DISABLED)
#         self.measure_button.config(state=tk.DISABLED)

#     def send_command(self):
#         """개별 명령 전송"""
#         if not self.is_connected():
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return
#         cmd = self.entry.get()
#         if cmd:
#             try:
#                 self.ser.write(cmd.encode('utf-8') + b'\n')
#                 self.output.insert(tk.END, f"Sent: {cmd}\n")
#                 self.entry.delete(0, tk.END)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Failed to send command: {e}\n")
#             self.output.see(tk.END)

#     def measure(self):
#         """개별 측정 버튼 -> 'l\n'"""
#         if not self.is_connected():
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return
#         try:
#             self.ser.write(b'l\n')
#             self.output.insert(tk.END, "Sent: l\n")
#         except serial.SerialException as e:
#             self.output.insert(tk.END, f"Failed to send measure command: {e}\n")
#         self.output.see(tk.END)

#     def do_measure_with_count(self, measure_count):
#         """
#         Measure All 시 호출:
#          - measure_count 저장 -> 다음 FastCH 응답이 들어오면 해당 count 키로 기록
#         """
#         if not self.is_connected():
#             return
#         self.pending_measure_count = measure_count
#         try:
#             self.ser.write(b'l\n')
#             self.output.insert(tk.END, f"Sent measure command (count={measure_count})\n")
#             self.output.see(tk.END)
#         except serial.SerialException as e:
#             self.output.insert(tk.END, f"Failed to send measure command: {e}\n")
#             self.output.see(tk.END)

#     def read_from_serial(self):
#         while self.is_reading:
#             try:
#                 line = self.ser.readline().decode('utf-8', errors='replace').strip()
#                 if line:
#                     self.data_queue.put(line)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Serial read error: {e}\n")
#                 self.output.see(tk.END)
#                 self.is_reading = False
#                 break

#     def update_gui(self):
#         """Queue에서 데이터 꺼내 파싱 -> measure_history에 기록"""
#         while not self.data_queue.empty():
#             data = self.data_queue.get()
#             self.output.insert(tk.END, f"{data}\n")

#             # ID2 파싱
#             if "ID=" in data:
#                 try:
#                     idx = data.index("ID=") + len("ID=")
#                     parsed_id2 = data[idx:].split(",")[0].strip()
#                     self.last_known_id2 = parsed_id2
#                     self.id2_label.config(text=f"ID2: {parsed_id2}")
#                     self.output.insert(tk.END, f"Parsed => ID2={parsed_id2}\n")
#                 except Exception as ex:
#                     self.output.insert(tk.END, f"Error parsing ID2: {ex}\n")

#             # CH1/CH2 파싱
#             if "FastCH:Standard format" in data:
#                 try:
#                     parts = data.split(",")
#                     ch1 = parts[1].strip()
#                     ch2 = parts[2].strip()

#                     current_id = self.id_var.get()
#                     self.id_label.config(text=f"ID: {current_id}")
#                     self.ch1_label.config(text=f"CH1: {ch1}")
#                     self.ch2_label.config(text=f"CH2: {ch2}")

#                     if self.pending_measure_count is not None:
#                         count_key = self.pending_measure_count
#                         self.measure_history[count_key] = (ch1, ch2)

#                         self.output.insert(
#                             tk.END,
#                             f"Parsed => ID={current_id}, CH1={ch1}, CH2={ch2}, measure_count={count_key}\n"
#                         )
#                         # 다음 응답은 새 측정 번호로 사용
#                         self.pending_measure_count = None
#                     else:
#                         # 만약 개별 Measure에서 들어온 응답
#                         new_index = len(self.measure_history) + 1
#                         self.measure_history[new_index] = (ch1, ch2)
#                         self.output.insert(
#                             tk.END,
#                             f"(No pending) => ID={current_id}, measure_index={new_index}\n"
#                         )
#                 except Exception as e:
#                     self.output.insert(tk.END, f"Error parsing CH1/CH2: {e}\n")

#             self.output.see(tk.END)

#         if self.is_reading:
#             self.after(50, self.update_gui)

#     def is_connected(self):
#         return (self.ser is not None) and self.ser.is_open

#     def close(self):
#         """Disconnect 처리"""
#         self.is_reading = False
#         if self.ser and self.ser.is_open:
#             try:
#                 self.ser.close()
#             except:
#                 pass

#         # used_ports에서 제거
#         if self.current_port in self.app.used_ports:
#             self.app.used_ports.remove(self.current_port)
#         self.current_port = None

#     def clear_measure_history(self):
#         """녹화(Record) 시작 시 측정 기록 초기화"""
#         self.measure_history.clear()
#         self.pending_measure_count = None


# class MultiSerialMonitorApp(tk.Tk):
#     """
#     메인 앱
#     - 2행×5열 최대 10개 장치
#     - Measure All, Save Data(Recording), Condition, etc.
#     - Connect All / Disconnect All 추가
#     - 장치 추가 시, 현재 연결된 포트를 제외한 목록만 OptionMenu에 표시
#     """
#     def __init__(self):
#         super().__init__()
#         self.title("Multi Serial Monitor (ConnectAll & DisconnectAll)")
#         self.geometry("1300x700")

#         # 현재 사용 중인 포트
#         self.used_ports = set()

#         self.global_baud_rate = 460800

#         # 장치들
#         self.device_frames = []

#         # 녹화 모드
#         self.is_recording = False
#         self.recording_filepath = None

#         # Condition 값들 (Measure All 시 기록)
#         self.condition_values = []
#         self.global_measure_count = 0

#         self.init_top_controls()

#         # 메인 컨테이너 (2행×5열)
#         self.devices_container = tk.Frame(self)
#         self.devices_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)
#         for r in range(2):
#             self.devices_container.rowconfigure(r, weight=1)
#         for c in range(5):
#             self.devices_container.columnconfigure(c, weight=1)

#         self.protocol("WM_DELETE_WINDOW", self.on_closing)

#     def init_top_controls(self):
#         top_frame = tk.Frame(self)
#         top_frame.pack(side="top", fill="x", padx=5, pady=5)

#         # Baud
#         tk.Label(top_frame, text="Global Baud Rate:").pack(side='left', padx=(0, 5))
#         self.baud_var = tk.StringVar(value=str(self.global_baud_rate))
#         baud_entry = tk.Entry(top_frame, width=10, textvariable=self.baud_var)
#         baud_entry.pack(side='left', padx=(0, 10))

#         btn_baud = tk.Button(top_frame, text="Set Baud Rate", command=self.set_baud_rate)
#         btn_baud.pack(side='left', padx=(0, 15))

#         # Condition
#         self.condition_var = tk.StringVar()
#         tk.Label(top_frame, text="Condition:").pack(side='left', padx=(10, 5))
#         condition_entry = tk.Entry(top_frame, textvariable=self.condition_var, width=20)
#         condition_entry.pack(side='left', padx=(0, 10))

#         # Measure All
#         measure_all_btn = tk.Button(top_frame, text="Measure All", command=self.measure_all)
#         measure_all_btn.pack(side="left", padx=(0, 15))

#         # Connect All
#         connect_all_btn = tk.Button(top_frame, text="Connect All", command=self.connect_all_devices)
#         connect_all_btn.pack(side="left", padx=(0, 10))

#         # Disconnect All
#         disconnect_all_btn = tk.Button(top_frame, text="Disconnect All", command=self.disconnect_all_devices)
#         disconnect_all_btn.pack(side="left", padx=(0, 10))

#         # Refresh
#         refresh_ports_btn = tk.Button(top_frame, text="Refresh Ports", command=self.refresh_all_ports)
#         refresh_ports_btn.pack(side='left', padx=(0, 10))

#         # Add / Remove
#         add_device_btn = tk.Button(top_frame, text="Add Device", command=self.add_device)
#         add_device_btn.pack(side='left', padx=(20, 10))

#         remove_device_btn = tk.Button(top_frame, text="Remove Device", command=self.remove_device)
#         remove_device_btn.pack(side='left', padx=(0, 10))

#         # Save/Recording
#         self.record_button = tk.Button(top_frame, text="Save Data", command=self.toggle_recording, state=tk.DISABLED)
#         self.record_button.pack(side="left", padx=(20, 10))

#     def get_all_com_ports(self):
#         """현재 PC에 물리적으로 존재하는 모든 포트"""
#         return [p.device for p in serial.tools.list_ports.comports()]

#     def get_available_ports_for_new_device(self):
#         """
#         새 장치를 추가할 때 사용 가능한(OptionMenu에 표시할) 포트 목록:
#         - PC에 물리적으로 연결된 전체 포트 중
#         - self.used_ports에 없는 것만
#         """
#         all_ports = self.get_all_com_ports()
#         # 이미 사용 중인(Connect 된) 포트를 제외
#         available = [p for p in all_ports if p not in self.used_ports]
#         return available

#     def add_device(self):
#         """
#         장치 추가:
#         - 10개까지만
#         - 이미 connected 상태인 포트를 제외한 목록을 frame에 전달
#         """
#         if len(self.device_frames) >= 10:
#             messagebox.showwarning("Limit Reached", "Cannot add more than 10 devices.")
#             return

#         device_index = len(self.device_frames)
#         device_label = f"장치{device_index + 1}"
#         available_ports = self.get_available_ports_for_new_device()

#         frame = SerialDeviceFrame(self.devices_container, self, device_label, available_ports)
#         row = device_index // 5
#         col = device_index % 5
#         frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

#         self.device_frames.append(frame)

#     def remove_device(self):
#         """마지막 장치 제거"""
#         if not self.device_frames:
#             return
#         frame = self.device_frames.pop()
#         frame.close()  # 연결되어 있으면 Disconnect
#         frame.destroy()

#         self.update_record_button_state()

#     def connect_all_devices(self):
#         """
#         'Connect All' 버튼: 아직 연결되지 않은 장치에 대해 connect_serial() 시도
#         - 이미 connected 상태라면 패스
#         """
#         for frame in self.device_frames:
#             if not frame.is_connected():
#                 frame.connect_serial()

#     def disconnect_all_devices(self):
#         """
#         'Disconnect All' 버튼: 모든 장치 disconnect
#         """
#         for frame in self.device_frames:
#             if frame.is_connected():
#                 frame.disconnect_serial()

#     def set_baud_rate(self):
#         val = self.baud_var.get()
#         try:
#             new_baud = int(val)
#             self.global_baud_rate = new_baud
#             messagebox.showinfo("Baud Rate", f"Global Baud Rate set to {new_baud}")
#         except ValueError:
#             messagebox.showwarning("Invalid Value", "Please enter a valid integer for Baud Rate.")

#     def measure_all(self):
#         """
#         - global_measure_count += 1
#         - condition_var를 condition_values에 저장
#         - 연결된 장치마다 do_measure_with_count(count)
#         """
#         connected = [f for f in self.device_frames if f.is_connected()]
#         if not connected:
#             messagebox.showwarning("No Device Connected", "No devices are currently connected.")
#             return

#         self.global_measure_count += 1
#         cond = self.condition_var.get()
#         self.condition_values.append(cond)

#         for dev in connected:
#             dev.do_measure_with_count(self.global_measure_count)

#     def refresh_all_ports(self):
#         """각 장치 프레임에서 포트 OptionMenu를 '실제 PC에 연결된 모든 포트' 기준으로 갱신"""
#         all_ports = self.get_all_com_ports()
#         for frame in self.device_frames:
#             # 만약 frame이 연결 안 된 상태라면 used_ports를 제외해야 하나,
#             # 여기선 단순히 UI 리스트만 갱신 (실제 connect 시 중복 체킹)
#             menu = frame.com_port_menu["menu"]
#             menu.delete(0, "end")
#             for p in all_ports:
#                 menu.add_command(label=p, command=lambda v=p: frame.com_port_var.set(v))

#     def is_any_device_connected(self):
#         return any(f.is_connected() for f in self.device_frames)

#     def update_record_button_state(self):
#         """Save Data / Recording 버튼 활성화 여부"""
#         if self.is_any_device_connected():
#             self.record_button.config(state=tk.NORMAL)
#         else:
#             self.record_button.config(state=tk.DISABLED)

#     def toggle_recording(self):
#         """
#         Save Data -> 파일 지정 & 이력 초기화 -> Recording
#         Recording -> 파일 저장 -> Save Data
#         """
#         if not self.is_recording:
#             filepath = asksaveasfilename(
#                 defaultextension=".txt",
#                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
#             )
#             if not filepath:
#                 return
#             self.recording_filepath = filepath

#             # 기존 기록 초기화
#             for f in self.device_frames:
#                 f.clear_measure_history()
#             self.condition_values.clear()
#             self.global_measure_count = 0

#             self.is_recording = True
#             self.record_button.config(text="Recording")
#         else:
#             self.finalize_recording()
#             self.is_recording = False
#             self.recording_filepath = None
#             self.record_button.config(text="Save Data")

#     def finalize_recording(self):
#         """
#         녹화 종료 -> 파일 저장
#         (기존 코드와 동일, 1행 ["", ""], 2행 ["Count","Condition"], 3행 이후 count, cond, ch1,ch2,...)
#         """
#         connected = [f for f in self.device_frames if f.is_connected()]
#         if not connected:
#             messagebox.showwarning("No Device Connected", "No devices are currently connected.")
#             return
#         if not self.recording_filepath:
#             return

#         # 1행
#         line1 = ["", ""]
#         for dev in connected:
#             line1.append(dev.current_port if dev.current_port else "")
#             line1.append(dev.last_known_id2)

#         # 2행
#         line2 = ["Count", "Condition"]
#         for _ in connected:
#             line2.append("CH1")
#             line2.append("CH2")

#         data_lines = []
#         for idx in range(self.global_measure_count):
#             row_data = []
#             row_data.append(str(idx + 1))  # Count
#             cond_val = self.condition_values[idx] if idx < len(self.condition_values) else ""
#             row_data.append(cond_val)

#             for dev in connected:
#                 key = idx + 1
#                 if key in dev.measure_history:
#                     ch1, ch2 = dev.measure_history[key]
#                     row_data.append(ch1)
#                     row_data.append(ch2)
#                 else:
#                     row_data.append("")
#                     row_data.append("")
#             data_lines.append(row_data)

#         try:
#             with open(self.recording_filepath, "w", encoding="utf-8") as f:
#                 f.write("\t".join(line1) + "\n")
#                 f.write("\t".join(line2) + "\n")
#                 for row_data in data_lines:
#                     f.write("\t".join(row_data) + "\n")

#             messagebox.showinfo("Save Complete", f"Data saved to:\n{self.recording_filepath}")
#         except OSError as e:
#             messagebox.showerror("Save Error", f"Failed to save data.\nError: {e}")

#     def on_closing(self):
#         """창 종료 시 모든 장치 disconnect"""
#         for f in self.device_frames:
#             f.close()
#         self.destroy()


# if __name__ == "__main__":
#     app = MultiSerialMonitorApp()
#     app.mainloop()



## 위 코드기능 +  에러 처리/예외 상황 로직이 포함된 코드
## 12/24 .exe 파일 배포 버전   
## 터미널 창에서 명령어 입력시, .py 파일이 있는 폴더에서 진행해야 한다.
## C:\Users\ksu07\OneDrive\문서\PythonWorkspace\sent_serial_record> pyinstaller --onefile -w  sent_serial_record.py


# import tkinter as tk
# from tkinter import scrolledtext, messagebox
# import serial
# import serial.tools.list_ports
# import threading
# from queue import Queue
# from tkinter.filedialog import asksaveasfilename
# import time

# MAX_RETRY = 3        # 포트 끊김 시 재시도 횟수 예시
# MEASURE_TIMEOUT = 5  # 응답 대기 타임아웃 (초)

# class SerialDeviceFrame(tk.Frame):
#     """
#     단일 시리얼 장치를 위한 Frame.
#     - 포트 선택, 연결/해제
#     - ID/ID2 표시
#     - measure_history[count] = (ch1, ch2) or ("No response", "")
#     - pending_measure_count: Measure All에서 전달받은 측정 횟수
#     - measure_request_time: 측정 명령 전송 시각(타임아웃 체크)
#     """
#     def __init__(self, parent, app_reference, device_label, available_ports):
#         super().__init__(parent)
#         self.app = app_reference
#         self.device_label = device_label

#         # 시리얼 관련
#         self.ser = None
#         self.is_reading = False
#         self.read_thread = None
#         self.data_queue = Queue()
#         self.current_port = None

#         # 사용자 입력 ID
#         self.id_var = tk.StringVar(value="")

#         # 최근 수신한 ID2
#         self.last_known_id2 = ""

#         # 측정 이력: { measure_count(int): (ch1, ch2) }
#         self.measure_history = {}

#         # Measure All 시, "이번 측정 번호"를 임시 저장
#         self.pending_measure_count = None
#         # 측정 명령을 전송한 시각
#         self.measure_request_time = 0.0
#         # 포트 끊김 시 재시도 횟수
#         self.port_retry_count = 0

#         self.init_ui(available_ports)

#     def init_ui(self, available_ports):
#         label_title = tk.Label(self, text=f"[{self.device_label}]", font=('Arial', 12, 'bold'))
#         label_title.pack(pady=(5, 2), anchor='w')

#         # ID 입력
#         id_frame = tk.Frame(self)
#         id_frame.pack(fill='x')
#         tk.Label(id_frame, text="Device ID:").pack(side='left')
#         tk.Entry(id_frame, textvariable=self.id_var, width=10).pack(side='left', padx=(5, 10))

#         # 포트 선택
#         tk.Label(self, text="Select COM Port:").pack(anchor='w')
#         self.com_port_var = tk.StringVar(value="")
#         if available_ports:
#             self.com_port_var.set(available_ports[0])
#         self.com_port_menu = tk.OptionMenu(self, self.com_port_var, *available_ports)
#         self.com_port_menu.pack(fill='x')

#         # Connect / Disconnect 버튼
#         btn_frame = tk.Frame(self)
#         btn_frame.pack(fill='x', pady=2)
#         self.connect_button = tk.Button(btn_frame, text="Connect", width=8, command=self.connect_serial)
#         self.connect_button.pack(side='left', padx=(0, 5))
#         self.disconnect_button = tk.Button(btn_frame, text="Disconnect", width=10,
#                                            command=self.disconnect_serial, state=tk.DISABLED)
#         self.disconnect_button.pack(side='left')

#         # 명령 전송
#         tk.Label(self, text="Enter command:").pack(anchor='w', pady=(5, 0))
#         self.entry = tk.Entry(self, width=30)
#         self.entry.pack()
#         self.send_button = tk.Button(self, text="Send", command=self.send_command, state=tk.DISABLED)
#         self.send_button.pack(pady=2)

#         # 측정 버튼(개별)
#         self.measure_button = tk.Button(self, text="Measure", command=self.measure, state=tk.DISABLED)
#         self.measure_button.pack(pady=2)

#         # ID / ID2 / CH1 / CH2 라벨
#         self.id_label = tk.Label(self, text="ID: ---")
#         self.id_label.pack()
#         self.id2_label = tk.Label(self, text="ID2: ---")
#         self.id2_label.pack()
#         self.ch1_label = tk.Label(self, text="CH1: ---")
#         self.ch1_label.pack()
#         self.ch2_label = tk.Label(self, text="CH2: ---")
#         self.ch2_label.pack()

#         # 출력창
#         self.output = scrolledtext.ScrolledText(self, width=70, height=8)
#         self.output.pack(pady=5)

#     def get_com_ports(self):
#         """현재 PC에서 사용 가능한 전체 포트 목록"""
#         return [p.device for p in serial.tools.list_ports.comports()]

#     def connect_serial(self):
#         """Connect 버튼 동작"""
#         port = self.com_port_var.get()
#         if not port:
#             messagebox.showwarning("No Port Selected",
#                                    f"[{self.device_label}] Please select a COM port.")
#             return
#         if port in self.app.used_ports:
#             messagebox.showwarning("Port In Use", f"Port {port} is already connected by another device.")
#             return

#         try:
#             baud_rate = self.app.global_baud_rate
#             self.ser = serial.Serial(port, baud_rate, timeout=1)
#             self.is_reading = True
#             self.port_retry_count = 0  # 재시도 카운트 초기화

#             self.connect_button.config(state=tk.DISABLED)
#             self.disconnect_button.config(state=tk.NORMAL)
#             self.send_button.config(state=tk.NORMAL)
#             self.measure_button.config(state=tk.NORMAL)

#             self.current_port = port
#             self.app.used_ports.add(port)

#             self.output.insert(tk.END, f"Connected to {port} (Baud: {baud_rate})\n")
#             self.output.see(tk.END)

#             # 연결됨 -> Save Data 버튼 활성화 가능
#             self.app.update_record_button_state()

#             # 수신 스레드
#             self.read_thread = threading.Thread(target=self.read_from_serial, daemon=True)
#             self.read_thread.start()
#             self.after(50, self.update_gui)

#         except serial.SerialException as e:
#             messagebox.showerror("Serial Port Error", f"Failed to open {port}\nError: {e}")

#     def disconnect_serial(self):
#         """Disconnect 버튼"""
#         if self.ser and self.ser.is_open:
#             self.close()
#             self.output.insert(tk.END, "Disconnected.\n")
#             self.output.see(tk.END)

#         self.connect_button.config(state=tk.NORMAL)
#         self.disconnect_button.config(state=tk.DISABLED)
#         self.send_button.config(state=tk.DISABLED)
#         self.measure_button.config(state=tk.DISABLED)

#         # Disconnect 후 -> Save Data 버튼 상태 갱신
#         self.app.update_record_button_state()

#     def send_command(self):
#         """Send 버튼"""
#         if not self.is_connected():
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return
#         cmd = self.entry.get()
#         if cmd:
#             try:
#                 self.ser.write(cmd.encode('utf-8') + b'\n')
#                 self.output.insert(tk.END, f"Sent: {cmd}\n")
#                 self.entry.delete(0, tk.END)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Failed to send command: {e}\n")
#             self.output.see(tk.END)

#     def measure(self):
#         """개별 Measure 버튼"""
#         if not self.is_connected():
#             self.output.insert(tk.END, "Not connected.\n")
#             self.output.see(tk.END)
#             return
#         try:
#             self.ser.write(b'l\n')
#             self.output.insert(tk.END, "Sent: l\n")
#         except serial.SerialException as e:
#             self.output.insert(tk.END, f"Failed to send measure command: {e}\n")
#         self.output.see(tk.END)

#     def do_measure_with_count(self, measure_count):
#         """
#         Measure All에서 호출:
#           - measure_count 기억 (pending_measure_count)
#           - 타임스탬프 기록 -> 응답 없으면 타임아웃
#         """
#         if not self.is_connected():
#             return
#         self.pending_measure_count = measure_count
#         self.measure_request_time = time.time()
#         try:
#             self.ser.write(b'l\n')
#             self.output.insert(tk.END, f"Sent measure command (count={measure_count})\n")
#         except serial.SerialException as e:
#             self.output.insert(tk.END, f"Failed to send measure command: {e}\n")

#     def read_from_serial(self):
#         """
#         백그라운드 스레드:
#          - 라인단위로 읽어서 data_queue에 넣음
#          - 포트 끊김 시 재시도
#         """
#         while self.is_reading:
#             try:
#                 line = self.ser.readline().decode('utf-8', errors='replace').rstrip('\r\n')
#                 if line:
#                     self.data_queue.put(line)
#             except serial.SerialException as e:
#                 self.output.insert(tk.END, f"Serial read error: {e}\n")
#                 self.output.see(tk.END)
#                 self.port_retry_count += 1
#                 if self.port_retry_count <= MAX_RETRY:
#                     self.output.insert(tk.END,
#                                        f"Retry {self.port_retry_count}/{MAX_RETRY} for port {self.current_port}...\n")
#                     time.sleep(1)
#                     continue
#                 else:
#                     self.output.insert(tk.END, f"Port {self.current_port} lost, disconnecting.\n")
#                     self.is_reading = False
#                     self.after(0, self.close)
#                 break
#             except Exception as ex:
#                 self.output.insert(tk.END, f"Unexpected error: {ex}\n")
#                 self.output.see(tk.END)
#                 self.is_reading = False
#                 self.after(0, self.close)
#                 break

#     def update_gui(self):
#         """
#         메인 스레드(주기적 after 호출):
#         - data_queue 처리, 응답 타임아웃 체크
#         """
#         # 타임아웃 체크
#         if (self.pending_measure_count is not None) and (time.time() - self.measure_request_time > MEASURE_TIMEOUT):
#             # 응답이 없으면 "No response" 처리
#             count_key = self.pending_measure_count
#             self.measure_history[count_key] = ("No response", "")  #
#             self.output.insert(tk.END, f"Timeout: No response for measure_count={count_key}\n")
#             self.pending_measure_count = None

#         # 큐에 쌓인 데이터 파싱
#         while not self.data_queue.empty():
#             data = self.data_queue.get()
#             self.output.insert(tk.END, f"{data}\n")

#             # ID2 파싱
#             if "ID=" in data:
#                 try:
#                     idx = data.index("ID=") + len("ID=")
#                     parsed_id2 = data[idx:].split(",")[0].strip()
#                     self.last_known_id2 = parsed_id2
#                     self.id2_label.config(text=f"ID2: {parsed_id2}")
#                     self.output.insert(tk.END, f"Parsed => ID2={parsed_id2}\n")
#                 except Exception as ex:
#                     self.output.insert(tk.END, f"Error parsing ID2: {ex}\n")

#             # CH1/CH2 파싱
#             if "FastCH:Standard format" in data:
#                 try:
#                     parts = data.split(",")
#                     ch1 = parts[1].strip()
#                     ch2 = parts[2].strip()

#                     current_id = self.id_var.get()
#                     self.id_label.config(text=f"ID: {current_id}")
#                     self.ch1_label.config(text=f"CH1: {ch1}")
#                     self.ch2_label.config(text=f"CH2: {ch2}")

#                     if self.pending_measure_count is not None:
#                         count_key = self.pending_measure_count
#                         self.measure_history[count_key] = (ch1, ch2)
#                         self.output.insert(
#                             tk.END,
#                             f"Parsed => ID={current_id}, CH1={ch1}, CH2={ch2}, measure_count={count_key}\n"
#                         )
#                         self.pending_measure_count = None
#                     else:
#                         new_index = len(self.measure_history) + 1
#                         self.measure_history[new_index] = (ch1, ch2)
#                         self.output.insert(
#                             tk.END,
#                             f"(No pending) => ID={current_id}, measure_index={new_index}\n"
#                         )
#                 except Exception as e:
#                     self.output.insert(tk.END, f"Error parsing CH1/CH2: {e}\n")

#             self.output.see(tk.END)

#         if self.is_reading:
#             self.after(50, self.update_gui)

#     def is_connected(self):
#         return (self.ser is not None) and self.ser.is_open

#     def close(self):
#         """Disconnect 처리"""
#         self.is_reading = False
#         if self.ser and self.ser.is_open:
#             try:
#                 self.ser.close()
#             except:
#                 pass
#         if self.current_port in self.app.used_ports:
#             self.app.used_ports.remove(self.current_port)
#         self.current_port = None

#         self.connect_button.config(state=tk.NORMAL)
#         self.disconnect_button.config(state=tk.DISABLED)
#         self.send_button.config(state=tk.DISABLED)
#         self.measure_button.config(state=tk.DISABLED)

#     def clear_measure_history(self):
#         """
#         Save Data(Recording) 시작 시, 기존 누적되어 있는 측정 이력 등을 초기화.
#         """
#         self.measure_history.clear()
#         self.pending_measure_count = None


# class MultiSerialMonitorApp(tk.Tk):
#     """
#     메인 앱
#     - Connect All / Disconnect All
#     - Measure All + Condition
#     - Save Data(Recording) with error/timeout handling
#     """
#     def __init__(self):
#         super().__init__()
#         self.title("Multi Serial Monitor (Fixed clear_measure_history)")
#         self.geometry("1300x700")

#         self.used_ports = set()
#         self.global_baud_rate = 460800

#         # 장치 목록
#         self.device_frames = []

#         # 녹화(Recording)
#         self.is_recording = False
#         self.recording_filepath = None

#         # Condition값들
#         self.condition_values = []
#         self.global_measure_count = 0

#         self.init_top_controls()

#         # 2행×5열 컨테이너
#         self.devices_container = tk.Frame(self)
#         self.devices_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)
#         for r in range(2):
#             self.devices_container.rowconfigure(r, weight=1)
#         for c in range(5):
#             self.devices_container.columnconfigure(c, weight=1)

#         self.protocol("WM_DELETE_WINDOW", self.on_closing)

#     def init_top_controls(self):
#         top_frame = tk.Frame(self)
#         top_frame.pack(side="top", fill="x", padx=5, pady=5)

#         tk.Label(top_frame, text="Global Baud Rate:").pack(side='left', padx=(0, 5))
#         self.baud_var = tk.StringVar(value=str(self.global_baud_rate))
#         baud_entry = tk.Entry(top_frame, width=10, textvariable=self.baud_var)
#         baud_entry.pack(side='left', padx=(0, 10))

#         btn_baud = tk.Button(top_frame, text="Set Baud Rate", command=self.set_baud_rate)
#         btn_baud.pack(side='left', padx=(0, 15))

#         # Condition + Measure All
#         self.condition_var = tk.StringVar()
#         tk.Label(top_frame, text="Condition:").pack(side='left', padx=(10, 5))
#         condition_entry = tk.Entry(top_frame, textvariable=self.condition_var, width=20)
#         condition_entry.pack(side='left', padx=(0, 10))

#         measure_all_btn = tk.Button(top_frame, text="Measure All", command=self.measure_all)
#         measure_all_btn.pack(side="left", padx=(0, 15))

#         # Connect All / Disconnect All
#         connect_all_btn = tk.Button(top_frame, text="Connect All", command=self.connect_all_devices)
#         connect_all_btn.pack(side='left', padx=(0, 10))
#         disconnect_all_btn = tk.Button(top_frame, text="Disconnect All", command=self.disconnect_all_devices)
#         disconnect_all_btn.pack(side='left', padx=(0, 10))

#         # Add / Remove Device
#         add_device_btn = tk.Button(top_frame, text="Add Device", command=self.add_device)
#         add_device_btn.pack(side='left', padx=(20, 10))
#         remove_device_btn = tk.Button(top_frame, text="Remove Device", command=self.remove_device)
#         remove_device_btn.pack(side='left', padx=(0, 10))

#         # Save Data
#         self.record_button = tk.Button(top_frame, text="Save Data",
#                                        command=self.toggle_recording, state=tk.DISABLED)
#         self.record_button.pack(side="left", padx=(20, 10))

#     def get_all_com_ports(self):
#         return [p.device for p in serial.tools.list_ports.comports()]

#     def get_available_ports_for_new_device(self):
#         """
#         새 장치 추가 시: 실제 PC에 연결된 포트 중 used_ports에 없는 것
#         """
#         all_ports = self.get_all_com_ports()
#         available = [p for p in all_ports if p not in self.used_ports]
#         return available

#     def add_device(self):
#         if len(self.device_frames) >= 10:
#             messagebox.showwarning("Limit Reached", "Cannot add more than 10 devices.")
#             return
#         device_index = len(self.device_frames)
#         device_label = f"장치{device_index + 1}"
#         available_ports = self.get_available_ports_for_new_device()

#         frame = SerialDeviceFrame(self.devices_container, self, device_label, available_ports)
#         row = device_index // 5
#         col = device_index % 5
#         frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

#         self.device_frames.append(frame)

#     def remove_device(self):
#         if not self.device_frames:
#             return
#         frame = self.device_frames.pop()
#         frame.close()
#         frame.destroy()
#         self.update_record_button_state()

#     def connect_all_devices(self):
#         for frame in self.device_frames:
#             if not frame.is_connected():
#                 frame.connect_serial()

#     def disconnect_all_devices(self):
#         for frame in self.device_frames:
#             if frame.is_connected():
#                 frame.disconnect_serial()

#     def set_baud_rate(self):
#         val = self.baud_var.get()
#         try:
#             new_baud = int(val)
#             self.global_baud_rate = new_baud
#             messagebox.showinfo("Baud Rate", f"Global Baud Rate set to {new_baud}")
#         except ValueError:
#             messagebox.showwarning("Invalid Value", "Please enter a valid integer for Baud Rate.")

#     def measure_all(self):
#         connected = [f for f in self.device_frames if f.is_connected()]
#         if not connected:
#             messagebox.showwarning("No Device Connected", "No devices are currently connected.")
#             return

#         self.global_measure_count += 1
#         cond = self.condition_var.get()
#         self.condition_values.append(cond)

#         for dev in connected:
#             dev.do_measure_with_count(self.global_measure_count)

#     def is_any_device_connected(self):
#         return any(f.is_connected() for f in self.device_frames)

#     def update_record_button_state(self):
#         if self.is_any_device_connected():
#             self.record_button.config(state=tk.NORMAL)
#         else:
#             self.record_button.config(state=tk.DISABLED)

#     def toggle_recording(self):
#         if not self.is_recording:
#             filepath = asksaveasfilename(
#                 defaultextension=".txt",
#                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
#             )
#             if not filepath:
#                 return
#             self.recording_filepath = filepath

#             # 기존 기록 초기화
#             for f in self.device_frames:
#                 f.clear_measure_history()
#             self.condition_values.clear()
#             self.global_measure_count = 0

#             self.is_recording = True
#             self.record_button.config(text="Recording")
#         else:
#             self.finalize_recording()
#             self.is_recording = False
#             self.recording_filepath = None
#             self.record_button.config(text="Save Data")

#     def finalize_recording(self):
#         connected = [f for f in self.device_frames if f.is_connected()]
#         if not connected:
#             messagebox.showwarning("No Device Connected", "No devices are currently connected.")
#             return
#         if not self.recording_filepath:
#             return

#         # 1행
#         line1 = ["", ""]
#         for dev in connected:
#             line1.append(dev.current_port if dev.current_port else "")
#             line1.append(dev.last_known_id2)

#         # 2행
#         line2 = ["Count", "Condition"]
#         for _ in connected:
#             line2.append("CH1")
#             line2.append("CH2")

#         data_lines = []
#         for idx in range(self.global_measure_count):
#             row_data = []
#             row_data.append(str(idx + 1))  # Count
#             cond_val = self.condition_values[idx] if idx < len(self.condition_values) else ""
#             row_data.append(cond_val)

#             for dev in connected:
#                 key = idx + 1
#                 if key in dev.measure_history:
#                     ch1, ch2 = dev.measure_history[key]
#                     row_data.append(ch1)
#                     row_data.append(ch2)
#                 else:
#                     # 응답이 없거나 포트 끊김이면 "No response"
#                     row_data.append("No response")  # "No response"  -> ""
#                     row_data.append("")
#             data_lines.append(row_data)

#         try:
#             with open(self.recording_filepath, "w", encoding="utf-8") as f:
#                 f.write("\t".join(line1) + "\n")
#                 f.write("\t".join(line2) + "\n")
#                 for row_data in data_lines:
#                     f.write("\t".join(row_data) + "\n")

#             messagebox.showinfo("Save Complete", f"Data saved to:\n{self.recording_filepath}")
#         except OSError as e:
#             messagebox.showerror("Save Error", f"Failed to save data.\nError: {e}")

#     def on_closing(self):
#         for f in self.device_frames:
#             f.close()
#         self.destroy()


# if __name__ == "__main__":
#     app = MultiSerialMonitorApp()
#     app.mainloop()

#################################################################   

## 지정된 PC에서 사용하도록 수정
## 장치 연결 없을시, add device 에러 처리

## 동작 검증증

import tkinter as tk
from tkinter import scrolledtext, messagebox
import serial
import serial.tools.list_ports
import threading
from queue import Queue
from tkinter.filedialog import asksaveasfilename
import time

import subprocess
import re
import sys
# 허용된 MAC 주소 목록
ALLOWED_MACS = [
    "68-7A-64-E8-10-11",  # PC 1의 MAC 주소
    "68-7A-64-E8-10-11",  # PC 2의 MAC 주소
    "68:7A:64:E8:10:11"   # PC 3의 MAC 주소
]

def get_mac_addresses_from_ipconfig():
    """
    Windows 명령어 'ipconfig /all'을 실행하여 MAC 주소(물리적 주소)를 추출합니다.
    """
    try:
        # ipconfig /all 명령 실행
        result = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True, check=True)
        output = result.stdout

        # 물리적 주소(MAC 주소) 찾기
        mac_addresses = re.findall(r"물리적 주소[.\s]*:\s*([0-9A-Fa-f-]+)", output)
        mac_addresses = [mac.upper() for mac in mac_addresses]  # 모두 대문자로 변환
        return mac_addresses
    except subprocess.CalledProcessError as e:
        print(f"Error executing ipconfig: {e}")
        return []

def verify_mac_address():
    """
    허용된 MAC 주소 목록(ALLOWED_MACS)과 현재 PC의 MAC 주소를 비교합니다.
    """
    mac_addresses = get_mac_addresses_from_ipconfig()
    for mac in mac_addresses:
        if mac in ALLOWED_MACS:
            return True
    messagebox.showerror(
        "Access Denied",
        #f"Unauthorized device.\nAllowed MACs: {', '.join(ALLOWED_MACS)}\nCurrent MACs: {', '.join(mac_addresses)}"
    )
    return False

MAX_RETRY = 3        # 포트 끊김 시 재시도 횟수 예시
MEASURE_TIMEOUT = 5  # 응답 대기 타임아웃 (초)

class SerialDeviceFrame(tk.Frame):
    """
    단일 시리얼 장치를 위한 Frame.
    - 포트 선택, 연결/해제
    - ID/ID2 표시
    - measure_history[count] = (ch1, ch2) or ("No response", "")
    - pending_measure_count: Measure All에서 전달받은 측정 횟수
    - measure_request_time: 측정 명령 전송 시각(타임아웃 체크)
    """
    def __init__(self, parent, app_reference, device_label, available_ports):
        super().__init__(parent)
        self.app = app_reference
        self.device_label = device_label

        # 시리얼 관련
        self.ser = None
        self.is_reading = False
        self.read_thread = None
        self.data_queue = Queue()
        self.current_port = None

        # 사용자 입력 ID
        self.id_var = tk.StringVar(value="")

        # 최근 수신한 ID2
        self.last_known_id2 = ""

        # 측정 이력: { measure_count(int): (ch1, ch2) }
        self.measure_history = {}

        # Measure All 시, "이번 측정 번호"를 임시 저장
        self.pending_measure_count = None
        # 측정 명령을 전송한 시각
        self.measure_request_time = 0.0
        # 포트 끊김 시 재시도 횟수
        self.port_retry_count = 0

        self.init_ui(available_ports)

    def init_ui(self, available_ports):
        label_title = tk.Label(self, text=f"[{self.device_label}]", font=('Arial', 12, 'bold'))
        label_title.pack(pady=(5, 2), anchor='w')

        # ID 입력
        id_frame = tk.Frame(self)
        id_frame.pack(fill='x')
        tk.Label(id_frame, text="Device ID:").pack(side='left')
        tk.Entry(id_frame, textvariable=self.id_var, width=10).pack(side='left', padx=(5, 10))

        # 포트 선택
        tk.Label(self, text="Select COM Port:").pack(anchor='w')
        self.com_port_var = tk.StringVar(value="")
        if available_ports:
            self.com_port_var.set(available_ports[0])
        self.com_port_menu = tk.OptionMenu(self, self.com_port_var, *available_ports)
        self.com_port_menu.pack(fill='x')

        # Connect / Disconnect 버튼
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill='x', pady=2)
        self.connect_button = tk.Button(btn_frame, text="Connect", width=8, command=self.connect_serial)
        self.connect_button.pack(side='left', padx=(0, 5))
        self.disconnect_button = tk.Button(btn_frame, text="Disconnect", width=10,
                                           command=self.disconnect_serial, state=tk.DISABLED)
        self.disconnect_button.pack(side='left')

        # 명령 전송
        tk.Label(self, text="Enter command:").pack(anchor='w', pady=(5, 0))
        self.entry = tk.Entry(self, width=30)
        self.entry.pack()
        self.send_button = tk.Button(self, text="Send", command=self.send_command, state=tk.DISABLED)
        self.send_button.pack(pady=2)

        # 측정 버튼(개별)
        self.measure_button = tk.Button(self, text="Measure", command=self.measure, state=tk.DISABLED)
        self.measure_button.pack(pady=2)

        # ID / ID2 / CH1 / CH2 라벨
        self.id_label = tk.Label(self, text="ID: ---")
        self.id_label.pack()
        self.id2_label = tk.Label(self, text="ID2: ---")
        self.id2_label.pack()
        self.ch1_label = tk.Label(self, text="CH1: ---")
        self.ch1_label.pack()
        self.ch2_label = tk.Label(self, text="CH2: ---")
        self.ch2_label.pack()

        # 출력창
        self.output = scrolledtext.ScrolledText(self, width=70, height=8)
        self.output.pack(pady=5)

    def get_com_ports(self):
        """현재 PC에서 사용 가능한 전체 포트 목록"""
        return [p.device for p in serial.tools.list_ports.comports()]

    def connect_serial(self):
        """Connect 버튼 동작"""
        port = self.com_port_var.get()
        if not port:
            messagebox.showwarning("No Port Selected",
                                   f"[{self.device_label}] Please select a COM port.")
            return
        if port in self.app.used_ports:
            messagebox.showwarning("Port In Use", f"Port {port} is already connected by another device.")
            return

        try:
            baud_rate = self.app.global_baud_rate
            self.ser = serial.Serial(port, baud_rate, timeout=1)
            self.is_reading = True
            self.port_retry_count = 0  # 재시도 카운트 초기화

            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
            self.send_button.config(state=tk.NORMAL)
            self.measure_button.config(state=tk.NORMAL)

            self.current_port = port
            self.app.used_ports.add(port)

            self.output.insert(tk.END, f"Connected to {port} (Baud: {baud_rate})\n")
            self.output.see(tk.END)

            # 연결됨 -> Save Data 버튼 활성화 가능
            self.app.update_record_button_state()

            # 수신 스레드
            self.read_thread = threading.Thread(target=self.read_from_serial, daemon=True)
            self.read_thread.start()
            self.after(50, self.update_gui)

        except serial.SerialException as e:
            messagebox.showerror("Serial Port Error", f"Failed to open {port}\nError: {e}")

    def disconnect_serial(self):
        """Disconnect 버튼"""
        if self.ser and self.ser.is_open:
            self.close()
            self.output.insert(tk.END, "Disconnected.\n")
            self.output.see(tk.END)

        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        self.measure_button.config(state=tk.DISABLED)

        # Disconnect 후 -> Save Data 버튼 상태 갱신
        self.app.update_record_button_state()

    def send_command(self):
        """Send 버튼"""
        if not self.is_connected():
            self.output.insert(tk.END, "Not connected.\n")
            self.output.see(tk.END)
            return
        cmd = self.entry.get()
        if cmd:
            try:
                self.ser.write(cmd.encode('utf-8') + b'\n')
                self.output.insert(tk.END, f"Sent: {cmd}\n")
                self.entry.delete(0, tk.END)
            except serial.SerialException as e:
                self.output.insert(tk.END, f"Failed to send command: {e}\n")
            self.output.see(tk.END)

    def measure(self):
        """개별 Measure 버튼"""
        if not self.is_connected():
            self.output.insert(tk.END, "Not connected.\n")
            self.output.see(tk.END)
            return
        try:
            self.ser.write(b'l\n')
            self.output.insert(tk.END, "Sent: l\n")
        except serial.SerialException as e:
            self.output.insert(tk.END, f"Failed to send measure command: {e}\n")
        self.output.see(tk.END)

    def do_measure_with_count(self, measure_count):
        """
        Measure All에서 호출:
          - measure_count 기억 (pending_measure_count)
          - 타임스탬프 기록 -> 응답 없으면 타임아웃
        """
        if not self.is_connected():
            return
        self.pending_measure_count = measure_count
        self.measure_request_time = time.time()
        try:
            self.ser.write(b'l\n')
            self.output.insert(tk.END, f"Sent measure command (count={measure_count})\n")
        except serial.SerialException as e:
            self.output.insert(tk.END, f"Failed to send measure command: {e}\n")

    def read_from_serial(self):
        """
        백그라운드 스레드:
         - 라인단위로 읽어서 data_queue에 넣음
         - 포트 끊김 시 재시도
        """
        while self.is_reading:
            try:
                line = self.ser.readline().decode('utf-8', errors='replace').rstrip('\r\n')
                if line:
                    self.data_queue.put(line)
            except serial.SerialException as e:
                self.output.insert(tk.END, f"Serial read error: {e}\n")
                self.output.see(tk.END)
                self.port_retry_count += 1
                if self.port_retry_count <= MAX_RETRY:
                    self.output.insert(tk.END,
                                       f"Retry {self.port_retry_count}/{MAX_RETRY} for port {self.current_port}...\n")
                    time.sleep(1)
                    continue
                else:
                    self.output.insert(tk.END, f"Port {self.current_port} lost, disconnecting.\n")
                    self.is_reading = False
                    self.after(0, self.close)
                break
            except Exception as ex:
                self.output.insert(tk.END, f"Unexpected error: {ex}\n")
                self.output.see(tk.END)
                self.is_reading = False
                self.after(0, self.close)
                break

    def update_gui(self):
        """
        메인 스레드(주기적 after 호출):
        - data_queue 처리, 응답 타임아웃 체크
        """
        # 타임아웃 체크
        if (self.pending_measure_count is not None) and (time.time() - self.measure_request_time > MEASURE_TIMEOUT):
            # 응답이 없으면 "No response" 처리
            count_key = self.pending_measure_count
            self.measure_history[count_key] = ("No response", "")  #
            self.output.insert(tk.END, f"Timeout: No response for measure_count={count_key}\n")
            self.pending_measure_count = None

        # 큐에 쌓인 데이터 파싱
        while not self.data_queue.empty():
            data = self.data_queue.get()
            self.output.insert(tk.END, f"{data}\n")

            # ID2 파싱
            if "ID=" in data:
                try:
                    idx = data.index("ID=") + len("ID=")
                    parsed_id2 = data[idx:].split(",")[0].strip()
                    self.last_known_id2 = parsed_id2
                    self.id2_label.config(text=f"ID2: {parsed_id2}")
                    self.output.insert(tk.END, f"Parsed => ID2={parsed_id2}\n")
                except Exception as ex:
                    self.output.insert(tk.END, f"Error parsing ID2: {ex}\n")

            # CH1/CH2 파싱
            if "FastCH:Standard format" in data:
                try:
                    parts = data.split(",")
                    ch1 = parts[1].strip()
                    ch2 = parts[2].strip()

                    current_id = self.id_var.get()
                    self.id_label.config(text=f"ID: {current_id}")
                    self.ch1_label.config(text=f"CH1: {ch1}")
                    self.ch2_label.config(text=f"CH2: {ch2}")

                    if self.pending_measure_count is not None:
                        count_key = self.pending_measure_count
                        self.measure_history[count_key] = (ch1, ch2)
                        self.output.insert(
                            tk.END,
                            f"Parsed => ID={current_id}, CH1={ch1}, CH2={ch2}, measure_count={count_key}\n"
                        )
                        self.pending_measure_count = None
                    else:
                        new_index = len(self.measure_history) + 1
                        self.measure_history[new_index] = (ch1, ch2)
                        self.output.insert(
                            tk.END,
                            f"(No pending) => ID={current_id}, measure_index={new_index}\n"
                        )
                except Exception as e:
                    self.output.insert(tk.END, f"Error parsing CH1/CH2: {e}\n")

            self.output.see(tk.END)

        if self.is_reading:
            self.after(50, self.update_gui)

    def is_connected(self):
        return (self.ser is not None) and self.ser.is_open

    def close(self):
        """Disconnect 처리"""
        self.is_reading = False
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
            except:
                pass
        if self.current_port in self.app.used_ports:
            self.app.used_ports.remove(self.current_port)
        self.current_port = None

        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        self.measure_button.config(state=tk.DISABLED)

    def clear_measure_history(self):
        """
        Save Data(Recording) 시작 시, 기존 누적되어 있는 측정 이력 등을 초기화.
        """
        self.measure_history.clear()
        self.pending_measure_count = None


class MultiSerialMonitorApp(tk.Tk):
    """
    메인 앱
    - Connect All / Disconnect All
    - Measure All + Condition
    - Save Data(Recording) with error/timeout handling
    """
    def __init__(self):
        super().__init__()
        self.title("Multi Serial Monitor (Fixed clear_measure_history)")
        self.geometry("1300x700")

        self.used_ports = set()
        self.global_baud_rate = 460800

        # 장치 목록
        self.device_frames = []

        # 녹화(Recording)
        self.is_recording = False
        self.recording_filepath = None

        # Condition값들
        self.condition_values = []
        self.global_measure_count = 0

        self.init_top_controls()

        # 2행×5열 컨테이너
        self.devices_container = tk.Frame(self)
        self.devices_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        for r in range(2):
            self.devices_container.rowconfigure(r, weight=1)
        for c in range(5):
            self.devices_container.columnconfigure(c, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def init_top_controls(self):
        top_frame = tk.Frame(self)
        top_frame.pack(side="top", fill="x", padx=5, pady=5)

        tk.Label(top_frame, text="Global Baud Rate:").pack(side='left', padx=(0, 5))
        self.baud_var = tk.StringVar(value=str(self.global_baud_rate))
        baud_entry = tk.Entry(top_frame, width=10, textvariable=self.baud_var)
        baud_entry.pack(side='left', padx=(0, 10))

        btn_baud = tk.Button(top_frame, text="Set Baud Rate", command=self.set_baud_rate)
        btn_baud.pack(side='left', padx=(0, 15))

        # Condition + Measure All
        self.condition_var = tk.StringVar()
        tk.Label(top_frame, text="Condition:").pack(side='left', padx=(10, 5))
        condition_entry = tk.Entry(top_frame, textvariable=self.condition_var, width=20)
        condition_entry.pack(side='left', padx=(0, 10))

        measure_all_btn = tk.Button(top_frame, text="Measure All", command=self.measure_all)
        measure_all_btn.pack(side="left", padx=(0, 15))

        # Connect All / Disconnect All
        connect_all_btn = tk.Button(top_frame, text="Connect All", command=self.connect_all_devices)
        connect_all_btn.pack(side='left', padx=(0, 10))
        disconnect_all_btn = tk.Button(top_frame, text="Disconnect All", command=self.disconnect_all_devices)
        disconnect_all_btn.pack(side='left', padx=(0, 10))

        # Add / Remove Device
        add_device_btn = tk.Button(top_frame, text="Add Device", command=self.add_device)
        add_device_btn.pack(side='left', padx=(20, 10))
        remove_device_btn = tk.Button(top_frame, text="Remove Device", command=self.remove_device)
        remove_device_btn.pack(side='left', padx=(0, 10))

        # Save Data
        self.record_button = tk.Button(top_frame, text="Save Data",
                                       command=self.toggle_recording, state=tk.DISABLED)
        self.record_button.pack(side="left", padx=(20, 10))

    def get_all_com_ports(self):
        return [p.device for p in serial.tools.list_ports.comports()]

    def get_available_ports_for_new_device(self):
        """
        새 장치 추가 시: 실제 PC에 연결된 포트 중 used_ports에 없는 것
        """
        all_ports = self.get_all_com_ports()
        available = [p for p in all_ports if p not in self.used_ports]
        return available

    def add_device(self):
        if len(self.device_frames) >= 10:
            messagebox.showwarning("Limit Reached", "Cannot add more than 10 devices.")
            return
        device_index = len(self.device_frames)
        device_label = f"장치{device_index + 1}"
        available_ports = self.get_available_ports_for_new_device()
        if not available_ports:
            messagebox.showwarning("No Devices", "연결된 장치가 없습니다.")
            return

        frame = SerialDeviceFrame(self.devices_container, self, device_label, available_ports)
        row = device_index // 5
        col = device_index % 5
        frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        self.device_frames.append(frame)

    def remove_device(self):
        if not self.device_frames:
            return
        frame = self.device_frames.pop()
        frame.close()
        frame.destroy()
        self.update_record_button_state()

    def connect_all_devices(self):
        for frame in self.device_frames:
            if not frame.is_connected():
                frame.connect_serial()

    def disconnect_all_devices(self):
        for frame in self.device_frames:
            if frame.is_connected():
                frame.disconnect_serial()

    def set_baud_rate(self):
        val = self.baud_var.get()
        try:
            new_baud = int(val)
            self.global_baud_rate = new_baud
            messagebox.showinfo("Baud Rate", f"Global Baud Rate set to {new_baud}")
        except ValueError:
            messagebox.showwarning("Invalid Value", "Please enter a valid integer for Baud Rate.")

    def measure_all(self):
        connected = [f for f in self.device_frames if f.is_connected()]
        if not connected:
            messagebox.showwarning("No Device Connected", "No devices are currently connected.")
            return

        self.global_measure_count += 1
        cond = self.condition_var.get()
        self.condition_values.append(cond)

        for dev in connected:
            dev.do_measure_with_count(self.global_measure_count)

    def is_any_device_connected(self):
        return any(f.is_connected() for f in self.device_frames)

    def update_record_button_state(self):
        if self.is_any_device_connected():
            self.record_button.config(state=tk.NORMAL)
        else:
            self.record_button.config(state=tk.DISABLED)

    def toggle_recording(self):
        if not self.is_recording:
            filepath = asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if not filepath:
                return
            self.recording_filepath = filepath

            # 기존 기록 초기화
            for f in self.device_frames:
                f.clear_measure_history()
            self.condition_values.clear()
            self.global_measure_count = 0

            self.is_recording = True
            self.record_button.config(text="Recording")
        else:
            self.finalize_recording()
            self.is_recording = False
            self.recording_filepath = None
            self.record_button.config(text="Save Data")

    def finalize_recording(self):
        connected = [f for f in self.device_frames if f.is_connected()]
        if not connected:
            messagebox.showwarning("No Device Connected", "No devices are currently connected.")
            return
        if not self.recording_filepath:
            return

        # 1행
        line1 = ["", ""]
        for dev in connected:
            line1.append(dev.current_port if dev.current_port else "")
            line1.append(dev.last_known_id2)

        # 2행
        line2 = ["Count", "Condition"]
        for _ in connected:
            line2.append("CH1")
            line2.append("CH2")

        data_lines = []
        for idx in range(self.global_measure_count):
            row_data = []
            row_data.append(str(idx + 1))  # Count
            cond_val = self.condition_values[idx] if idx < len(self.condition_values) else ""
            row_data.append(cond_val)

            for dev in connected:
                key = idx + 1
                if key in dev.measure_history:
                    ch1, ch2 = dev.measure_history[key]
                    row_data.append(ch1)
                    row_data.append(ch2)
                else:
                    # 응답이 없거나 포트 끊김이면 "No response"
                    row_data.append("No response")  # "No response"  -> ""
                    row_data.append("")
            data_lines.append(row_data)

        try:
            with open(self.recording_filepath, "w", encoding="utf-8") as f:
                f.write("\t".join(line1) + "\n")
                f.write("\t".join(line2) + "\n")
                for row_data in data_lines:
                    f.write("\t".join(row_data) + "\n")

            messagebox.showinfo("Save Complete", f"Data saved to:\n{self.recording_filepath}")
        except OSError as e:
            messagebox.showerror("Save Error", f"Failed to save data.\nError: {e}")

    def on_closing(self):
        for f in self.device_frames:
            f.close()
        self.destroy()


if __name__ == "__main__":
    # 프로그램 시작 전에 MAC 주소 확인
    if not verify_mac_address():
        sys.exit()

    app = MultiSerialMonitorApp()
    app.mainloop()


