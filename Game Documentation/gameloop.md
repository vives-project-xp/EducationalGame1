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






| Category         | Asset                        | Price | Eco-Score Effect                               |
|------------------|------------------------------|-------|-------------------------------------------------|
| Buildings        | House                        | $1000 | tbd                                             |
| Buildings        | Store                        | $3000 | tbd                                             |
| Special          | Hospital                     | $15000| tbd                                             |
| Nature           | Tree/park                    | $250  | tbd                                             |
| Energy           | Windmill                     | $2000 | tbd                                             |
| Energy           | Factory                      | $10000| tbd                                             |

