import tkinter as tk
import yaml
from datetime import datetime, time, timedelta
import os
import sys

class WorkProgressBar:
    def __init__(self, config_path='config.yaml'):
        # Load configuration
        self.load_config(config_path)
        
        # Create root window
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Always on top
        self.root.attributes('-transparentcolor', 'white')  # Make background transparent
        
        # Set window to full screen width, configured height
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f'{screen_width}x{self.config["progress_bar"]["height"]}+0+0')
        
        # Create canvas for progress bar
        self.canvas = tk.Canvas(self.root, width=screen_width, 
                                height=self.config['progress_bar']['height'], 
                                bg='white', highlightthickness=0)
        self.canvas.pack()
        
        # Update progress periodically
        self.update_progress()
        
    def load_config(self, config_path):
        # 尝试多个配置文件路径
        possible_paths = [
            config_path,  # 原始路径
            os.path.join(os.path.dirname(sys.executable), 'config.yaml'),  # 可执行文件目录
            os.path.join(os.path.expanduser('~'), '.work_progress_bar', 'config.yaml'),  # 用户目录
            os.path.join(os.getcwd(), 'config.yaml')  # 当前工作目录
        ]
        
        # 查找存在的配置文件
        existing_config = None
        for path in possible_paths:
            if os.path.exists(path):
                existing_config = path
                break
        
        # 如果没有找到配置文件，创建默认配置
        if existing_config is None:
            # 选择一个默认保存路径
            existing_config = os.path.join(os.path.expanduser('~'), '.work_progress_bar', 'config.yaml')
            
            # 确保目录存在
            os.makedirs(os.path.dirname(existing_config), exist_ok=True)
            
            # 创建默认配置
            default_config = {
                'work_hours': {
                    'start_time': '09:30',
                    'end_time': '18:30'
                },
                'progress_bar': {
                    'height': 2,
                    'completed_color': 'lime',
                    'uncompleted_color': 'gray'
                }
            }
            
            # 写入默认配置文件
            with open(existing_config, 'w') as file:
                yaml.dump(default_config, file, default_flow_style=False)
        
        # 加载配置文件
        with open(existing_config, 'r') as file:
            self.config = yaml.safe_load(file)
        
        # 转换时间字符串为时间对象
        self.work_start_time = datetime.strptime(
            self.config['work_hours']['start_time'], "%H:%M").time()
        self.work_end_time = datetime.strptime(
            self.config['work_hours']['end_time'], "%H:%M").time()
        
    def calculate_progress(self):
        now = datetime.now().time()
        
        # Convert times to datetime for comparison
        today = datetime.today()
        current_datetime = datetime.combine(today, now)
        start_datetime = datetime.combine(today, self.work_start_time)
        end_datetime = datetime.combine(today, self.work_end_time)
        
        # Handle breaks
        total_break_duration = timedelta()
        if 'breaks' in self.config:
            for break_period in self.config['breaks']:
                if break_period.get('exclude_from_progress', False):
                    break_start = datetime.combine(today, 
                        datetime.strptime(break_period['start'], "%H:%M").time())
                    break_end = datetime.combine(today, 
                        datetime.strptime(break_period['end'], "%H:%M").time())
                    
                    # Only count break if it's within work hours
                    if start_datetime <= break_start < end_datetime and \
                       start_datetime < break_end <= end_datetime:
                        total_break_duration += (break_end - break_start)
        
        # Calculate total work duration minus breaks
        total_work_duration = (end_datetime - start_datetime - total_break_duration).total_seconds()
        elapsed_time = max(0, (current_datetime - start_datetime - total_break_duration).total_seconds())
        
        # Calculate progress percentage
        progress = min(1, max(0, elapsed_time / total_work_duration))
        return progress
    
    def update_progress(self):
        # Clear previous drawing
        self.canvas.delete('all')
        
        screen_width = self.root.winfo_screenwidth()
        progress = self.calculate_progress()
        
        # Get colors from config
        completed_color = self.config['progress_bar'].get('completed_color', 'green')
        uncompleted_color = self.config['progress_bar'].get('uncompleted_color', 'gray')
        
        # Draw completed part
        completed_width = int(screen_width * progress)
        self.canvas.create_rectangle(0, 0, completed_width, 
                                     self.config['progress_bar']['height'], 
                                     fill=completed_color, outline='')
        
        # Draw uncompleted part
        self.canvas.create_rectangle(completed_width, 0, screen_width, 
                                     self.config['progress_bar']['height'], 
                                     fill=uncompleted_color, outline='')
        
        # Schedule next update
        self.root.after(60000, self.update_progress)  # Update every minute
        
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    progress_bar = WorkProgressBar()
    progress_bar.run()
