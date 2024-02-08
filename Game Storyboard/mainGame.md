<h1>Main game screen</h1>
<h2>First game concept visual</h2>
<img src="src/image.png" alt= "first game concept visual"></img>
Here you see a first simple concept of how the main screen will look like. All the parts are explained below.

<h2>Game flow, target, end, ...</h2>

- What kind of game is this?
    This is in fact a citybuilder game, the player has to buy things in the shop with ingame coins. The more houses and places there are, the more people live in the city. Coins can be earned by having houses etc in the city. Sometimes, a main character gives the player trivia about the climate, depending on the decisions the player made. <br></br>

- The game has a few elements that depend if the player is playing good or bad.
1)  The main element is an <b>eco-score</b>, which can go lower or higher, depending on the deciscions the player makes. For example, if there aren't much trees in the city, the score goes lower.
When this score is 0, the game is over. This is the only way the player can 'die' in the game. It is displayed on 
a progress bar in the right upper corner.

2)  In the game there are <b>coins</b> that can be earned. With this coins, assets can be bought in the shop. The amount of coins the player earns depend on the aumont of people in the city (explained below). They are auto-collected, so the player does not have to click on things to earn them. At the beginning of the game, the player already has 500 coins so he/she can start playing and building.

3) Another element is the amount of <b>people</b> in the city. To have more people, the player has to build more houses. People do jobs, so more people results in more coins. People can move away too if the eco-score lowers too much. Then a small pop-up (like "- 10 people" in a red color) appears on the screen.

- Shop and assets

When clicking the shop button, the shop appears at the at the bottom of the screen, first showing the categories. 

When a category is clicked, the category icon and name move to the left side and all the assets from that category are shown (so their icon and price). 

When the player select and item from the shop, all the other elements(coins, score, ...) disappear until a place for the object is chosen on the grid. After that, they appear again, but if the placed item is on the same place as an elements, the element is placed above the item. The reason for this is that we can have a bigger grid to place the assets in. 

All the assets are visualised here:
<table border="1">
  <thead>
    <tr>
      <th>Category</th>
      <th>Asset</th>
      <th>Price</th>
      <th>Eco-Score Effect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
    </tr>
    <tr>
      <td rowspan="4">Buildings</td>
      <td>House</td>
      <td>$50</td>
      <td>todo</td>
    </tr>
    <tr>
      <td>Apartment Building</td>
      <td>$150</td>
      <td>todo</td>
    </tr>
    <tr>
      <td>Office Building</td>
      <td>$250</td>
      <td>todo</td>
    </tr>
    <tr>
      <td>Shop</td>
      <td>$400</td>
      <td>todo</td>
    </tr>
    <tr>
      <td rowspan="4">Energy Sources</td>
      <td>Solar Panel</td>
      <td>$100</td>
      <td>todo</td>
    </tr>
    <tr>
      <td>Wind Turbine</td>
      <td>$150</td>
      <td>todo</td>
    </tr>
    <tr>
      <td>Coal Power Plant</td>
      <td>$300</td>
      <td>todo</td>
    </tr>
    <tr>
      <td>Nuclear Power Plant</td>
      <td>$500</td>
      <td>todo</td>
    </tr>
    <tr>
      <td rowspan="4">Nature Objects</td>
      <td>Trees</td>
      <td>$10</td>
      <td>todo</td>
    </tr>
    <tr>
      <td>Bushes</td>
      <td>$5</td>
      <td>todo</td>
    </tr>
    <tr>
      <td>Park</td>
      <td>$1000</td>
      <td>todo</td>
    </tr>
    <tr>
      <td>Gardens</td>
      <td>$100</td>
      <td>todo</td>
    </tr>
    <tr>
    <td rowspan="5">Transportation</td>
      <td>Road</td>
      <td>$10</td>
      <td>If there are too many (a certain amount of the grid, or if more roads than other transport,...) score decrease. Otherwise it doesnt change.</td>
    </tr>
      <td>Bicycle Lane</td>
      <td>$50</td>
      <td>Increase</td>
    </tr>
    <tr>
      <td>Electric Vehicle Charging Station</td>
      <td>$200</td>
      <td>Increase</td>
    </tr>
    <tr>
      <td>Bus Stop</td>
      <td>$100</td>
      <td>Increase</td>
    </tr>
    <tr>
      <td>Highway Expansion</td>
      <td>$300</td>
      <td>Decrease</td>
    </tr>
    <tr>
    <td rowspan="1">More yet to be added...</td>
    </tr>
  </tbody>
</table>

Most of the assets can also be upgraded by clicking them. An upgraded asset results in more money that can be collected.

- Info-button

The info button (the button with the question mark) shows a popup on the screen when it clicked. It explains very briefly what the 3 elements do (eco-score, people and coins) and what the main goal of the game is (so basically what is explained in this file but more briefly).

<h2>Game start</h2>

- Coins at start: $500.

- people at start: 0

- eco-score at start: 50

- The game starts with an empty grid. 

- TODO

<h2>Climate trivia</h2>

All trivia about climate that is showing up (for example when the player made a decision) are listed here, together with the occasion when they can show up.

<table border="1">
  <thead>
    <tr>
      <th>Trivia</th>
      <th>Occasion</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Did you know? Trees absorb carbon dioxide and release oxygen, helping to clean the air we breathe.</td>
      <td>Random event during gameplay</td>
    </tr>
    <tr>
      <td>Fun Fact: Solar panels convert sunlight into electricity without producing harmful emissions.</td>
      <td>After the player constructs a Solar Panel</td>
    </tr>
    <tr>
      <td>Fact: Recycling one aluminum can saves enough energy to power a TV for three hours.</td>
      <td>After the player builds a Recycling Center</td>
    </tr>
    <tr>
      <td>Interesting Fact: Rainforests are home to over half of the world's plant and animal species, despite covering only 6% of Earth's land surface.</td>
      <td>When the player buys a nature object in the shop</td>
    </tr>
    <tr>
      <td>Environmental Tip: Turning off lights and unplugging electronics when not in use can help conserve energy and reduce electricity consumption.</td>
      <td>Random event during gameplay</td>
    </tr>
    <tr>
      <td>Fun Fact: Bees play a crucial role in pollinating many of the fruits and vegetables we eat, contributing to food production and biodiversity.</td>
      <td>After the player constructs a Garden or Park</td>
    </tr>
    <tr>
      <td>Fact: The ozone layer in Earth's atmosphere protects life on the planet by absorbing harmful ultraviolet radiation from the sun.</td>
      <td>Random event during gameplay</td>
    </tr>
    <tr>
      <td>Did you know? Hybrid and electric vehicles produce fewer greenhouse gas emissions than traditional gasoline-powered cars.</td>
      <td>After the player constructs an Electric Vehicle Charging Station</td>
    </tr>
    <tr>
      <td>Interesting Fact: Rainwater harvesting involves collecting and storing rainwater for later use in irrigation, landscaping, and household activities.</td>
      <td>When the player unlocks the Nature Objects category in the shop</td>
    </tr>
    <tr>
      <td>Environmental Tip: Choosing products with minimal packaging and opting for reusable items can help reduce waste and conserve resources.</td>
      <td>Random event during gameplay</td>
    </tr>
    <tr>
      <td>More trivia yet to be added</td>
      <td>TODO</td>
    </tr>
  </tbody>
</table>


<h2>Additional information</h2>
