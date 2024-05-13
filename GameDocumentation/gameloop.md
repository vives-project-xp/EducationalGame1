# Proces
## Goal
The goal of this project is to create a digital or physical game about either climate change or gender equality and teach young people about this subject throughout the game. We decided to go for the subject climate change and tried implementing this into both a board and pc game. This file will provide all information about the PC game. 

## Tools
We decided to use pygame to program our game. Going over our game idea we had a few option. As the game is a 2D game and is not live action we chose pygame. Python is in fact a slower language then for example the c/c++ language. In our game speed is not an important variable. We used VS code as text editor as it's the main tool we use throughout our educational career so far (https://code.visualstudio.com/download). Install python by following the following guide (start of the course: https://www.youtube.com/watch?v=XKHEtdqhLK8&t=178s)

## Steps
### Step 1 - Initializing
Firstly we created a basic pygame window by installing and initializing the libraries. This way we already had some kind of visual building block to rely and base our game on.
This was followed by creating the grid layout for the game. All this started in a single resolution, which couldn't be resized. Combined with the background we already set the visual theme of our game, which we kept all the way till now. 

### Step 2 - Click event
Our game's input heavily involves mouseclicks. Pygame has these events build in, which makes is easier to work with is. We did however have to calculate the mouse position in our grid to match the size of our cells. We then went on with our x and y cell location for the placement of buildings on cells and only used the basic variables for drawing on the screen itself.

### Step 3 - Placing house (buildings)
We went on to add the logic for placing a house on the grid and align it perfectly. Along the way we added upgrade and delete buttons as well as a visual range for some of JOXE's newly added prefabs, like hospitals or fire stations. These interactions logically and visually require a decent amount of code.

### Step 4 - Global variables
Later on we implemented the logic for our basic variables which would track the current counters. We only implemented the citizen happiness near the end of the project, to add another form of depth to the game. Influencing the positioning of buildings for people to think about the climate (score).

### Step 5 - Game save
These variables needed to be loaded in when logging in with a previously used username. We created the code to create the file and load this whenever the correct button was pressed. The most challanging part about this was the rotation of roads and levels of buildings (and versions of houses). After updating our object code for these and trying some things to fix this we came to the correct solution.

### Step 6 - Resolution
We had the idea to make the game resizeable as this is an important feature for any application. This took a lot of time bacause we had to implement the logic everywhere and create the menu to update this and get the value in the correct object, which we then had to pass on to the correct classes. 

### Step 7 - Finalizing game and fixing bugs
We spent some time on testing the project to find bugs and improvement we could add along the way, we set up some tests which we always had to succeed after adding new features.

## Challanges
### Roads
During the entire process the roads where the biggest challange. We started with the same logics as the current buildings by placing one road at a time, but this took to long to build a lengthy road. We then added the functionality to build multiple roads with only a few clicks, which made the placement of roads a lot more bearable. We then programmed the logics to change the image to the correct one whenever roads are besides eachother. Due to the combined placement of objects a lot of issues appeared and the road images didn't change to the wanted image or where placed incorrectly. The roads where also logically located wrong, till we found (after a few lengthy debugging sessions) the problem. In the process we dropped our idea for self driving cars on the placed roads using AI, because the placement was incorrect. After fixing the bug we decided to focus on the core aspects of the game rather then one single feature which we'd like to add. The roads kept forming a challange even after fixing the bug due to the other logics used for them, deleting the roads was a difficult aspect. We have fixed the issues which made this impossiblen but only the edges of a road gets deleted. 

### Resizing
We spend a good amount of time on the resizing menu and logics for location and size of the images. We valued this feature a lot as almost every application has the option to change the resolution window. We had to pass to right variables to the right placed to be able to calculate the resize value as multiple classes where used for this part of code (main.py for the resolution menu, resolution.py was added to have a central place to hold these variables and other classes where the elements were drawn).

### Gamesave
Saving the values to the file was quite easy compared to the challange of loading that information to the game variables. The formatting was quite a challange and changes to the game would go hand in hand with changes to the gamesave methods. The rotation and road types formed the biggest challange as this needed a whole lot of added code to the classes which were already on point by that time.

# Main game screen
## Pre game 
### Title screen
When you first launch the game you will be led to our title screen. We chose to create a simple but vivid image containing our game title and a simple play button which will lead you to the next screen.
On pressing the play button the loading text will appear at the bottom right of the screen. 
![image](https://github.com/vives-project-xp/EducationalGame1/assets/113900803/f1819b8f-bdc4-499a-a533-bec8e118f05c)

### Login screen with username
After loading on to the following screen you will have the option to fill in a username. If you choose a new username which wasn't used before, you will start a new game with the basic settings 
and stats. When you save your game a file with your username as title (username.txt) will be created and will hold all information about your game on that moment. If you then start the game again with
that same username, you will load to the latest status that was saved. 
![image](https://github.com/vives-project-xp/EducationalGame1/assets/113900803/0203596b-0b01-4a31-b792-7359fc4de43f)
![image](https://github.com/vives-project-xp/EducationalGame1/assets/113900803/19654c23-61d3-4d59-ae9e-0fd973603eaa)

## Game
### First view
When loading in, you will see an empty grid and some basic information on the game. From topleft to bottom you will find the following things:
- City/username
- Date (how long has the game lasted)
- Inhabitants (the amount if citizens will impact the amount of money you earn)
- Money (the in game valuta used to place and upgrade buildings)
- City happiness (this is the overall score between 0 and 100 which shows the mood of citizens. This score will boost money gain and slow down eco-score degradation)
- Eco-score (at the top-middle, when reaching 0 the game will end and your city will fall to ashes)
- Tracker (at the bottom-right, this shows the average gain/loss for money and eco-score for the next minute (if the situation does NOT change))
  
![image](https://github.com/vives-project-xp/EducationalGame1/assets/113900803/1274712f-6b84-45bd-89ba-aa7419a8ec8b)

### Placing buildings
If you press any cell on the grid, this cell will be marked with a yellow outline meaning it's selected. At the same time the shop will open at the bottom as shown in the image down below).
The shop has been divided into four categories to keep the prefabs organised and easy to find. We have buildings, roads, energy and nature.
Buildings contain houses (which adds citizens), stores and factories to earn money but lose some eco-score overtime and the hospital/firestation prefab to add happiness score to each house in it's range. They do have a certain upkeep cost. The road category only contains a prefab with the same name: road and will only visually connect and upgrade the city. Each road will also remove 1 eco-score. So placing too many roads at the same time could be detrimental or even unwantedly end your game early, so be CAREFUL! 
As third category there's three prefabs in energy. A windmill, powerplant and solar panel. The powerplant will give money but remove happiness score from each nearby building while the other two will cost you some money as upkeep for a raise in citizen happiness for each building inside it's range. Lastly we have the nature category housing the tree/park prefab. When placed you will get a trivia question. You will earn a small amount of money when answering correct boosting your budget. The tree itself will give you and instant eco-score boost and give a small boost over time. When upgraded the tree will become a park.
![image](https://github.com/vives-project-xp/EducationalGame1/assets/113900803/ddef5ff2-21b1-4fbe-9a2f-521f1e78842b)

| Category         | Asset                        | Price | Instant Eco-Score Effect                        | Money Effect Over Time      | Eco-Score Effect Over Time      |
|------------------|------------------------------|-------|-------------------------------------------------|-----------------------------|---------------------------------|
| Buildings        | House                        | $1000 | n/a                                             | tbd                         | tbd                             |
| Buildings        | Store                        | $3000 | -5                                              | tbd                         | tbd                             |
| Buildings        | Factory                      | $10000| n/a                                             | tbd                         | tbd                             |
| Buildings        | Hospital                     | $15000| -5                                              | tbd                         | tbd                             |
| Buildings        | Fire Station                 | $20000| -5                                              | tbd                         | tbd                             |
| Road             | Road                         | $50   | -1                                              | tbd                         | tbd                             |
| Energy           | Windmill                     | $2000 | +10                                             | tbd                         | tbd                             |
| Energy           | Solar Panel                  | $5000 | +2                                              | tbd                         | tbd                             |
| Energy           | Powerplant                   | $3000 | -5                                              | tbd                         | tbd                             |
| Nature           | Tree/Park                    | $250  | +5                                              | tbd                         | tbd                             |


### Upgrading buildings
After placing buildings you can upgrade them. This can be done by clicking the building you want to upgrade. You will see the cost for doing this. If you have sufficient budget the text will be black. Otherwise it will be red and you know you're unable to upgrade that specific building. In that same menu you will also find a delete button. This will remove the building and their gained benefits or disadvantages, but you will NOT earn back the invested money for that building. So when placing a building, think twice before doing so. You will not be able to replace that building.
![image](https://github.com/vives-project-xp/EducationalGame1/assets/113900803/3250a9fa-4d36-4a73-af30-b278fb91f1ad)


### Resolution
At any point in the game you can change the resolution by pressing the **ESC** key on your keyboard. Make sure to press save to apply the new resolution.
![image](https://github.com/vives-project-xp/EducationalGame1/assets/113900803/861c7afe-ac26-46fb-b8b2-9e2c39cb4806)

### Game over
If you reach an eco-score of 0, the game over screen will be shown and you will have to option to quit or restart from scratch. 
![image](https://github.com/vives-project-xp/EducationalGame1/assets/113900803/d2e8ed67-2000-4e82-b156-e200a4485732)

### Game save
When trying to close the window you will have the choice to quit the game, either with or without saving it or to continue the game.
![image](https://github.com/vives-project-xp/EducationalGame1/assets/113900803/7d3d766e-3cc8-4676-8580-ed8893dbb792)


