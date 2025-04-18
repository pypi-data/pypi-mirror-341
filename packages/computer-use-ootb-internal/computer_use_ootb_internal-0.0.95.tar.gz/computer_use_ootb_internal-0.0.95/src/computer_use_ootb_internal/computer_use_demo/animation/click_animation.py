"""
show_click(x, y, duration_ms=800)
 → 在屏幕 (x,y) 显示点击动画，停留 duration_ms 毫秒
依赖: pyside6
确保同目录有 click.gif
"""
import sys, time
from pathlib import Path
from PySide6.QtCore import Qt, QPoint, QTimer, QEventLoop, QSize
from PySide6.QtGui  import QPainter, QPixmap, QMovie
from PySide6.QtWidgets import QApplication, QWidget, QLabel

CLICK_GIF = Path(__file__).with_name("icons8-select-cursor-transparent-96.gif")

class ClickAnimation(QWidget):
    def __init__(self, pos: QPoint, life_ms: int):
        super().__init__(None,
            Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint
            | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        if not CLICK_GIF.exists():
            print(f"Error: click.gif not found at {CLICK_GIF}")
            return
            
        try:
            # 创建标签显示GIF
            self.label = QLabel(self)
            self.movie = QMovie(str(CLICK_GIF))
            
            # 获取原始尺寸并打印（仅供参考）
            self.movie.jumpToFrame(0)
            original_size = self.movie.currentPixmap().size()
            print(f"GIF original size: {original_size.width()}x{original_size.height()}")
            
            # 将GIF缩放到30x30像素
            target_size = QSize(50, 50)
            self.movie.setScaledSize(target_size)
            
            # 设置标签尺寸和GIF
            self.label.setMovie(self.movie)
            self.label.setFixedSize(target_size)
            
            # 设置窗口大小和位置
            self.resize(target_size)
            self.move(pos.x() - 15, pos.y() - 15)  # 居中显示
            
            # 提高播放性能
            self.movie.setCacheMode(QMovie.CacheAll)
            
            # 开始播放动画
            self.movie.start()
            
            # 设置定时器关闭窗口
            QTimer.singleShot(life_ms, self.close)
            
            self.show()
            self.raise_()
            print(f"Click animation created at ({pos.x()}, {pos.y()}), size: 30x30, duration: {life_ms}ms")
        except Exception as e:
            print(f"Error creating click animation: {str(e)}")

# ---------- 外部接口 ----------
_app = None
def _ensure_app():
    global _app
    if _app is None:
        if QApplication.instance() is None:
            print("Creating new QApplication instance")
            _app = QApplication(sys.argv)
        else:
            print("Using existing QApplication instance")
            _app = QApplication.instance()

def show_click(x: int, y: int, duration_ms: int = 2000):  # 增加默认播放时间
    """阻塞式点击动画：调用后必定肉眼可见"""
    print(f"Attempting to show click at ({x}, {y})")
    
    if not CLICK_GIF.exists():
        raise FileNotFoundError(f"click.gif not found at {CLICK_GIF}")
        
    _ensure_app()
    
    try:
        animation = ClickAnimation(QPoint(x, y), duration_ms)

        # 局部事件循环，动画结束后返回
        loop = QEventLoop()
        QTimer.singleShot(duration_ms + 150, loop.quit)  # 增加等待时间
        loop.exec()
        print("Click animation completed")
    except Exception as e:
        print(f"Error during show_click: {str(e)}")


# --- 在原 import 区域追加 ---
from PySide6.QtCore import QEasingCurve, QPropertyAnimation
# --------------------------------------------------------


# ---------- 新增函数 ----------
def show_move_to(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 1200):
    """
    阻塞式移动动画：在 (x1, y1) 处出现光标 GIF，
    并在 duration_ms 毫秒内平滑移动到 (x2, y2)。

    Args:
        x1, y1        : 起点屏幕坐标
        x2, y2        : 终点屏幕坐标
        duration_ms   : 移动总时长
    """
    print(f"Attempting to move click from ({x1}, {y1}) → ({x2}, {y2}) "
          f"in {duration_ms} ms")

    if not CLICK_GIF.exists():
        raise FileNotFoundError(f"click.gif not found at {CLICK_GIF}")

    _ensure_app()

    # 让 widget 的生命周期略长于动画，避免提前销毁
    life_ms = duration_ms + 200
    widget  = ClickAnimation(QPoint(x1, y1), life_ms)

    # 用 QPropertyAnimation 平滑移动窗口
    anim = QPropertyAnimation(widget, b"pos")
    anim.setDuration(duration_ms)
    # ClickAnimation 内部已经向左上偏移了 15px，这里沿用同样的偏移
    anim.setStartValue(QPoint(x1 - 15, y1 - 15))
    anim.setEndValue(QPoint(x2 - 15, y2 - 15))
    anim.setEasingCurve(QEasingCurve.OutQuad)     # 可自行更换缓动曲线
    anim.start()

    # 局部事件循环，直到动画结束
    loop = QEventLoop()
    anim.finished.connect(loop.quit)
    QTimer.singleShot(life_ms, loop.quit)          # 双保险
    loop.exec()

    print("Move‑to animation completed")
# ---------------------------------


# ---------- 命令行测试 ----------
if __name__ == "__main__":
    # 测试点击
    x, y = 500, 500
    print(f"Testing click at ({x}, {y})")
    show_click(x, y)

    # 测试移动
    x1, y1 = 400, 400
    x2, y2 = 800, 600
    print(f"Testing move from ({x1}, {y1}) → ({x2}, {y2})")
    show_move_to(x1, y1, x2, y2, duration_ms=2000)
