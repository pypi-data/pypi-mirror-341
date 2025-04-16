import os
import time
import subprocess
import pyautogui

def open_star_rail():
    """
    Open Edge browser and navigate to Star Rail website,
    then click at position (1014, 620)
    """
    print("Preparing Star Rail environment...")
    
    # Open Edge browser with Star Rail URL
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['start', 'msedge', 'https://sr.mihoyo.com/cloud/#/'], shell=True)
        else:
            print("Star Rail preparation is designed for Windows only")
            return False
        
        # Wait for the page to load
        time.sleep(5)
        
        # Click at the specified position
        pyautogui.click(1014, 620)
        
        print("Star Rail environment prepared successfully")
        return True
        
    except Exception as e:
        print(f"Error preparing Star Rail environment: {str(e)}")
        return False

if __name__ == "__main__":
    open_star_rail() 