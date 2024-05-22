Zie ook, testing documenten.

# Tests to do to debug the game:
### Login Screen:
| Test Name                 | Steps                                                       | Expected Result                                         |
|---------------------------|-------------------------------------------------------------|----------------------------------------------------------|
| No Username Test          | 1. Open the login screen.<br>2. Try to log in without entering a username. | Ensure a warning is displayed indicating that a username is required. |
| Buttons Test              | 1. Check if all buttons on the login screen work correctly. | Ensure each button performs the correct action (e.g., login, register, cancel). |
| Invalid Credentials Test | 1. Enter a valid username but an invalid length or character.<br>2. Attempt to log in. | Ensure a message is displayed indicating incorrect credentials. |

### Roads:
| Test Name                    | Steps                                                       | Expected Result                                         |
|------------------------------|-------------------------------------------------------------|----------------------------------------------------------|
| Multiple Possibilities Test | 1. Test different combinations of roads on the screen.      | Verify that the game runs smoothly with various combinations of roads without crashing or freezing. |
| Intersection Test            | 1. Create intersections between different types of roads.<br>2. Ensure vehicles navigate intersections correctly. | Ensure vehicles follow appropriate paths and traffic rules at intersections. |

### Resize:
| Test Name               | Steps                                                       | Expected Result                                         |
|-------------------------|-------------------------------------------------------------|----------------------------------------------------------|
| Resize Problems Test   | 1. Enlarge and shrink the game window during gameplay.      | Check if the game responds correctly to resizing the window without graphical issues or glitches. |
| Dynamic Resolution Test | 1. Resize the window while playing the game.<br>2. Ensure game elements adjust dynamically to different resolutions. | Verify that game elements scale appropriately without distortion or loss of functionality. |

### Assets:
| Test Name                         | Steps                                                       | Expected Result                                         |
|-----------------------------------|-------------------------------------------------------------|----------------------------------------------------------|
| Crashes or Upgrade Issues Test   | 1. Load all assets in the game.<br>2. Check if there are any assets that cause the game to crash or issues.<br>3. Test if all assets can be upgraded correctly without errors. | Ensure there are no assets causing crashes or upgrade issues. |
| Asset Loading Speed Test         | 1. Measure the time taken to load all assets at startup.<br>2. Ensure assets load within an acceptable timeframe. | Verify that assets load efficiently to prevent long loading times. |

### Trivia Popups:
| Test Name               | Steps                                                       | Expected Result                                         |
|-------------------------|-------------------------------------------------------------|----------------------------------------------------------|
| Clarity Test            | 1. Activate trivia popups while playing the game.           | Ensure all trivia popups are clear and understandable to the player. |
| Enough Trivia Questions Test | 1. Test if there are enough trivia questions available to prevent players from encountering the same questions repeatedly. | Ensure there is a diversity of questions to minimize repetition. |
| Randomization Test      | 1. Trigger trivia popups multiple times.<br>2. Ensure questions appear randomly each time. | Verify that questions are randomly selected to keep the game engaging. |
