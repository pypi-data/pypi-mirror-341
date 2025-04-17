# Copyright (c) 2025 ByUsi. All rights reserved.

import sys
import time
import shutil
import threading
from dataclasses import dataclass
from typing import Optional, Callable
from math import ceil

class _ColorSystem:
    """私有颜色管理系统"""
    def __init__(self):
        self._truecolor_supported = self._detect_truecolor()
        self._palette = self._build_palette()
        
    @staticmethod
    def _detect_truecolor() -> bool:
        """检测终端真彩色支持"""
        try:
            import colorama
            from colorama.ansitowin32 import winterm
            if winterm.win32:
                return winterm.WinTerm().enable_vt_processing
            return True
        except:
            return False
    
    def _build_palette(self):
        """构建专利调色板"""
        return {
            'byusi_blue': (31, 117, 203),
            'deep_purple': (88, 66, 124),
            'dynamic_gold': (234, 182, 56),
            'terminal_gray': (68, 68, 68)
        }
    
    def resolve_color(self, spec: str) -> str:
        """解析颜色规范"""
        if spec.startswith('gradient('):
            return self._resolve_gradient(spec)
        return self._resolve_single(spec)
    
    def _resolve_single(self, spec: str) -> str:
        """解析单一颜色"""
        if spec in self._palette:
            return self._ansi_truecolor(*self._palette[spec])
        return spec  # 支持直接使用hex代码
    
    def _resolve_gradient(self, spec: str) -> list:
        """解析渐变规范"""
        params = spec[9:-1].split(',')
        start = self._palette.get(params[0], (31, 117, 203))
        end = self._palette.get(params[1], (88, 66, 124))
        steps = int(params[2]) if len(params)>2 else 10
        return [self._interpolate(start, end, steps, i) for i in range(steps)]
    
    @staticmethod
    def _interpolate(start, end, steps, index):
        """颜色插值算法"""
        ratio = index / (steps - 1)
        return (
            int(start[0] + (end[0] - start[0]) * ratio),
            int(start[1] + (end[1] - start[1]) * ratio),
            int(start[2] + (end[2] - start[2]) * ratio)
        )
    
    def _ansi_truecolor(self, r: int, g: int, b: int) -> str:
        """生成真彩色ANSI代码"""
        return f"\033[38;2;{r};{g};{b}m"

@dataclass
class Element:
    """进度条元素组件"""
    char: str
    color: str = "byusi_blue"
    style: str = "normal"

@dataclass
class BarStyle:
    """进度条样式配置"""
    fill: Element
    empty: Element
    edges: tuple
    width: int = 40
    animation_curve: Callable = lambda x: x

PRESET_STYLES = {
    'corporate': BarStyle(
        fill=Element("█", "gradient(byusi_blue,deep_purple,12)"),
        empty=Element("░", "terminal_gray"),
        edges=(Element("▌", "dynamic_gold"), Element("▐", "dynamic_gold"))
}

class ProgressBar:
    """主进度条实现类"""
    
    _SPINNER_FRAMES = ["▰▱▱▱", "▰▰▱▱", "▰▰▰▱", "▰▰▰▰", "▰▰▰▱", "▰▰▱▱", "▰▱▱▱"]
    
    def __init__(
        self,
        total: int,
        label: str = "Operation",
        style: BarStyle = PRESET_STYLES['corporate'],
        update_rate: float = 0.15,
        dynamic_width: bool = True
    ):
        self.total = total
        self.label = label
        self.style = style
        self.current = 0
        self._active = False
        self._color = _ColorSystem()
        self._lock = threading.Lock()
        self._start_time = None
        self._rate_history = []
        self._term_width = shutil.get_terminal_size().columns
        
        # 动画参数
        self.frame_index = 0
        self.update_interval = update_rate
        
    def __enter__(self):
        self.start()
        return self
        
    def __exit__(self, *args):
        self.stop()
        
    def start(self):
        """启动进度条"""
        self._active = True
        self._start_time = time.time()
        self._render_thread = threading.Thread(target=self._render_loop)
        self._render_thread.start()
        
    def _render_loop(self):
        """渲染循环"""
        while self._active:
            with self._lock:
                self._render_frame()
            time.sleep(self.update_interval)
            
    def _calculate_eta(self):
        """计算预计剩余时间"""
        if len(self._rate_history) < 2:
            return 0.0
        avg_rate = sum(self._rate_history) / len(self._rate_history)
        return (self.total - self.current) / avg_rate if avg_rate > 0 else 0
    
    def _get_progress_stats(self):
        """生成统计信息"""
        elapsed = time.time() - self._start_time
        current_rate = self.current / elapsed if elapsed > 0 else 0
        self._rate_history.append(current_rate)
        return (
            f"Elapsed: {elapsed:.1f}s | "
            f"Rate: {current_rate:.1f}/s | "
            f"ETA: {self._calculate_eta():.1f}s"
        )
    
    def _render_frame(self):
        """渲染单个帧"""
        # 动态宽度调整
        if self.style.width == 'auto':
            bar_width = self._term_width - 45
        else:
            bar_width = self.style.width
            
        # 进度计算
        progress = min(self.current / self.total, 1.0)
        filled_width = int(bar_width * progress)
        
        # 构建进度条
        bar_parts = []
        bar_parts.append(self._apply_style(self.style.edges[0]))
        
        # 渐变填充
        if 'gradient' in self.style.fill.color:
            color_steps = self._color.resolve_color(self.style.fill.color)
            for i in range(filled_width):
                bar_parts.append(f"{color_steps[i % len(color_steps)]}{self.style.fill.char}")
        else:
            bar_parts.append(
                self._apply_style(
                    self.style.fill.char * filled_width,
                    self.style.fill
                )
            )
        
        # 剩余部分
        bar_parts.append(
            self._apply_style(
                self.style.empty.char * (bar_width - filled_width),
                self.style.empty
            )
        )
        bar_parts.append(self._apply_style(self.style.edges[1]))
        
        # 组合所有部件
        spinner = self._SPINNER_FRAMES[self.frame_index % len(self._SPINNER_FRAMES)]
        stats = self._get_progress_stats()
        output = (
            f"{spinner} {self.label[:18].ljust(20)} "
            f"{''.join(bar_parts)} "
            f"{self.current}/{self.total} ({progress:.1%}) "
            f"{stats}"
        )
        
        sys.stdout.write(f"\r{output[:self._term_width]}")
        sys.stdout.flush()
        self.frame_index += 1
        
    def _apply_style(self, text: str, element: Element) -> str:
        """应用样式到文本"""
        color_code = self._color.resolve_color(element.color)
        style_code = ""
        if element.style == "bold":
            style_code = "\033[1m"
        return f"{style_code}{color_code}{text}\033[0m"
        
    def update(self, increment: int = 1):
        """更新进度"""
        with self._lock:
            self.current = min(self.current + increment, self.total)
            
    def stop(self):
        """停止进度条"""
        self._active = False
        self._render_thread.join()
        self._render_frame()
        print()