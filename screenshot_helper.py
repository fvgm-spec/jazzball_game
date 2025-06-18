import pygame
import os
import datetime

def take_screenshot(screen, directory="screenshots"):
    """
    Takes a screenshot of the current pygame screen and saves it to the specified directory.
    
    Args:
        screen: The pygame surface to capture
        directory: Directory to save the screenshot (default: "screenshots")
    
    Returns:
        The filename of the saved screenshot
    """
    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{directory}/screenshot_{timestamp}.png"
    
    # Save the screenshot
    pygame.image.save(screen, filename)
    print(f"Screenshot saved: {filename}")
    return filename

# Example usage in your game:
# 
# # Add this to your imports
# from screenshot_helper import take_screenshot
#
# # Add this to your game code where you want to take screenshots (e.g., when F12 is pressed)
# if event.type == KEYDOWN and event.key == K_F12:
#     take_screenshot(self.screen)
