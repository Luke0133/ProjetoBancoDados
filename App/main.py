from ui.ui import main_ui
import sys, ctypes, subprocess, platform, psutil

SIZE = 24

def usar_cmd():
    try:
        p = psutil.Process()
        while True:
            parent = p.parent()
            if not parent:
                return None
            name = parent.name().lower()
            if name == "cmd.exe":
                return
            elif name in ["powershell.exe", "pwsh.exe", "windowsterminal.exe"]:
                executar_cmd()
            p = parent
    except psutil.Error:
        return None

def executar_cmd(command="python main.py"):
    system = platform.system()
    if system == "Windows":
        subprocess.Popen(f'start cmd /k {command}', shell=True)
    elif system == "Linux":
        subprocess.Popen(['x-terminal-emulator', '-e', command])
    elif system == "Darwin":  # macOS
        subprocess.Popen(['osascript', '-e', f'tell application "Terminal" to do script "{command}"'])
    sys.exit()

def formatar_ui():
    # Tornando CMD no tamanho máximo
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')

    hWnd = kernel32.GetConsoleWindow()
    user32.ShowWindow(hWnd, 3)
    
    # Ajustando tamanho da fonte
    LF_FACESIZE = 32

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short),
                    ("Y", ctypes.c_short)]

    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

    stdout = ctypes.windll.kernel32.GetStdHandle(-11)
    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.dwFontSize.Y = SIZE
    font.FontFamily = 54      
    font.FaceName = "Consolas"

    ctypes.windll.kernel32.SetCurrentConsoleFontEx(stdout, ctypes.c_long(False), ctypes.byref(font))

if __name__ == "__main__":
    usar_cmd()

    if platform.system() == "Windows":
        formatar_ui()

    main_ui()

