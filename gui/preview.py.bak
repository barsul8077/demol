import threading
import tkinter as tk
from tkinter import ttk
from typing import Dict

class PreviewGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title('Instagram Profile Auto Update')
        self._build_widgets()
        self.status_data = {}

    def _build_widgets(self) -> None:
        self.root.geometry('900x640')
        self.profile_frame = ttk.LabelFrame(self.root, text='Current Profile')
        self.profile_frame.pack(fill='x', padx=12, pady=8)

        self.username_var = tk.StringVar(value='N/A')
        self.status_var = tk.StringVar(value='Waiting')
        self.processed_var = tk.StringVar(value='0')
        self.remaining_var = tk.StringVar(value='0')
        self.success_var = tk.StringVar(value='0')
        self.failed_var = tk.StringVar(value='0')
        self.progress_var = tk.DoubleVar(value=0)

        self._widget_row('Username', self.username_var)
        self._widget_row('Status', self.status_var)
        self._widget_row('Processed', self.processed_var)
        self._widget_row('Remaining', self.remaining_var)
        self._widget_row('Success', self.success_var)
        self._widget_row('Failed', self.failed_var)

        self.progress_bar = ttk.Progressbar(self.root, maximum=100, variable=self.progress_var)
        self.progress_bar.pack(fill='x', padx=12, pady=6)

        self.details_frame = ttk.LabelFrame(self.root, text='Profile Details')
        self.details_frame.pack(fill='both', expand=True, padx=12, pady=8)

        self.detail_vars = {
            'followers': tk.StringVar(value='N/A'),
            'following': tk.StringVar(value='N/A'),
            'posts': tk.StringVar(value='N/A'),
            'engagement_rate': tk.StringVar(value='N/A'),
            'average_likes': tk.StringVar(value='N/A'),
            'average_comments': tk.StringVar(value='N/A'),
            'verified': tk.StringVar(value='N/A'),
            'category': tk.StringVar(value='N/A'),
            'bio': tk.StringVar(value='N/A'),
        }

        for label, var in self.detail_vars.items():
            ttk.Label(self.details_frame, text=label.replace('_', ' ').title() + ':').pack(anchor='w', padx=10, pady=2)
            ttk.Label(self.details_frame, textvariable=var, wraplength=860).pack(anchor='w', padx=24)

    def _widget_row(self, label_text: str, variable: tk.StringVar) -> None:
        row = ttk.Frame(self.profile_frame)
        row.pack(fill='x', padx=8, pady=4)
        ttk.Label(row, text=label_text + ':', width=16).pack(side='left')
        ttk.Label(row, textvariable=variable).pack(side='left')

    def update(self, data: Dict[str, any]) -> None:
        self.username_var.set(data.get('username', 'N/A'))
        self.status_var.set(data.get('status', 'N/A'))
        self.processed_var.set(str(data.get('processed', 0)))
        self.remaining_var.set(str(data.get('remaining', 0)))
        self.success_var.set(str(data.get('success', 0)))
        self.failed_var.set(str(data.get('failed', 0)))
        self.progress_var.set(data.get('progress', 0))
        details = data.get('details', {})
        self.detail_vars['followers'].set(str(details.get('followers', 'N/A')))
        self.detail_vars['following'].set(str(details.get('following', 'N/A')))
        self.detail_vars['posts'].set(str(details.get('posts', 'N/A')))
        self.detail_vars['engagement_rate'].set(str(details.get('engagement_rate', 'N/A')))
        self.detail_vars['average_likes'].set(str(details.get('average_likes', 'N/A')))
        self.detail_vars['average_comments'].set(str(details.get('average_comments', 'N/A')))
        self.detail_vars['verified'].set(str(details.get('is_verified', 'N/A')))
        self.detail_vars['category'].set(details.get('category', 'N/A'))
        self.detail_vars['bio'].set(details.get('bio', 'N/A'))
        self.root.update_idletasks()

    def start(self) -> None:
        self.root.mainloop()
