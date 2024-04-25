from cx_Freeze import setup, Executable

# Include any necessary files. 
# The format is a tuple containing the file (or directory) name and the destination directory.
includefiles = [
    ('assets/logo/JOXE.png', 'assets/logo/JOXE.png'),
    ('assets/logo/JOXEC.png', 'assets/logo/JOXEC.png'),
    ('assets/resources/background/bg2.png', 'assets/resources/background/bg2.png'),
    ('assets/resources/background/grass.jpg', 'assets/resources/background/grass.jpg'),
    ('assets/resources/background/grass2.png', 'assets/resources/background/grass2.png'),
    ('assets/resources/background/play.png', 'assets/resources/background/play.png'),

    ('assets/resources/buildings/energy/powergenerate/powerplant-unfinished.png', 'assets/resources/buildings/energy/powergenerate/powerplant-unfinished.png'),
    ('assets/resources/buildings/energy/powergenerate/powerplant1.png', 'assets/resources/buildings/energy/powergenerate/powerplant1.png'),
    ('assets/resources/buildings/energy/powergenerate/powerplantB1.png', 'assets/resources/buildings/energy/powergenerate/powerplantB1.png'),

    ('assets/resources/buildings/energy/solarpanel/singlesolarpanel.png', 'assets/resources/buildings/energy/solarpanel/singlesolarpanel.png'),
    ('assets/resources/buildings/energy/solarpanel/solar.png', 'assets/resources/buildings/energy/solarpanel/solar.png'),

    ('assets/resources/buildings/energy/windmills/windmill.png', 'assets/resources/buildings/energy/windmills/windmill.png'),
    ('assets/resources/buildings/energy/windmills/windmill1.png', 'assets/resources/buildings/energy/windmills/windmill1.png'),
    ('assets/resources/buildings/energy/windmills/windmill2.png', 'assets/resources/buildings/energy/windmills/windmill2.png'),

    ('assets/resources/buildings/factory/tempfac1.png', 'assets/resources/buildings/factory/tempfac1.png'),
    ('assets/resources/buildings/factory/tempfac2.png', 'assets/resources/buildings/factory/tempfac2.png'),
    ('assets/resources/buildings/factory/tempfac3.png', 'assets/resources/buildings/factory/tempfac3.png'),

    ('assets/resources/buildings/firestation/firestation1.png', 'assets/resources/buildings/firestation/firestation1.png'),
    ('assets/resources/buildings/firestation/firestation2.png', 'assets/resources/buildings/firestation/firestation2.png'),
    ('assets/resources/buildings/firestation/firestation3.png', 'assets/resources/buildings/firestation/firestation3.png'),

    ('assets/resources/buildings/hospital/hospital1.png', 'assets/resources/buildings/hospital/hospital1.png'),
    ('assets/resources/buildings/hospital/hospital2.png', 'assets/resources/buildings/hospital/hospital2.png'),
    ('assets/resources/buildings/hospital/hospital3.png', 'assets/resources/buildings/hospital/hospital3.png'),

    ('assets/resources/buildings/statue/statue1.jpg', 'assets/resources/buildings/statue/statue1.jpg'),

    ('assets/resources/buildings/stores/store1.png', 'assets/resources/buildings/stores/store1.png'),
    ('assets/resources/buildings/stores/store2.png', 'assets/resources/buildings/stores/store2.png'),
    ('assets/resources/buildings/stores/store3.png', 'assets/resources/buildings/stores/store3.png'),
    ('assets/resources/buildings/stores/store4.png', 'assets/resources/buildings/stores/store4.png'),

    # cars

    ('assets/resources/characters/Mayor.png', 'assets/resources/characters/Mayor.png'),

    ('assets/resources/emptycell/emptycell.png', 'assets/resources/emptycell/emptycell.png'),

    ('assets/resources/houses/house11.png', 'assets/resources/houses/house11.png'),
    ('assets/resources/houses/house12.png', 'assets/resources/houses/house12.png'),
    ('assets/resources/houses/house13.png', 'assets/resources/houses/house13.png'),
    ('assets/resources/houses/house21.png', 'assets/resources/houses/house21.png'),
    ('assets/resources/houses/house22.png', 'assets/resources/houses/house22.png'),
    ('assets/resources/houses/house31.png', 'assets/resources/houses/house31.png'),
    ('assets/resources/houses/house41.png', 'assets/resources/houses/house41.png'),
    ('assets/resources/houses/newHouse1.png', 'assets/resources/houses/newHouse1.png'),
    ('assets/resources/houses/shop.png', 'assets/resources/houses/shop.png'),

    ('assets/resources/icons/AngryBox.png', 'assets/resources/icons/AngryBox.png'),
    ('assets/resources/icons/box.png', 'assets/resources/icons/box.png'),
    ('assets/resources/icons/box1.png', 'assets/resources/icons/box1.png'),
    ('assets/resources/icons/CityNameBox.png', 'assets/resources/icons/CityNameBox.png'),
    ('assets/resources/icons/climate.png', 'assets/resources/icons/climate.png'),
    ('assets/resources/icons/close.png', 'assets/resources/icons/close.png'),
    ('assets/resources/icons/happy.png', 'assets/resources/icons/happy.png'),
    ('assets/resources/icons/Happybox.png', 'assets/resources/icons/Happybox.png'),
    ('assets/resources/icons/happyhouse.png', 'assets/resources/icons/happyhouse.png'),
    ('assets/resources/icons/house.png', 'assets/resources/icons/house.png'),
    ('assets/resources/icons/money.png', 'assets/resources/icons/money.png'),
    ('assets/resources/icons/Moneybox.png', 'assets/resources/icons/Moneybox.png'),
    ('assets/resources/icons/name.png', 'assets/resources/icons/name.png'),
    ('assets/resources/icons/NotHappyBox.png', 'assets/resources/icons/NotHappyBox.png'),
    ('assets/resources/icons/person.png', 'assets/resources/icons/person.png'),
    ('assets/resources/icons/remove.png', 'assets/resources/icons/remove.png'),
    ('assets/resources/icons/sadhouse.png', 'assets/resources/icons/sadhouse.png'),
    ('assets/resources/icons/shop.png', 'assets/resources/icons/shop.png'),
    ('assets/resources/icons/upgrade.png', 'assets/resources/icons/upgrade.png'),

    ('assets/resources/nature/fire.png', 'assets/resources/nature/fire.png'),
    ('assets/resources/nature/tree/tree1.png', 'assets/resources/nature/tree/tree1.png'),
    ('assets/resources/nature/tree/tree2.png', 'assets/resources/nature/tree/tree2.png'),
    ('assets/resources/nature/tree/tree3.png', 'assets/resources/nature/tree/tree3.png'),
    ('assets/resources/nature/trees.jpg', 'assets/resources/nature/trees.jpg'),
    ('assets/resources/nature/treesgrow.jpg', 'assets/resources/nature/treesgrow.jpg'),

    ('assets/resources/road/+-road.png', 'assets/resources/road/+-road.png'),
    ('assets/resources/road/cornerroad.png', 'assets/resources/road/cornerroad.png'),
    ('assets/resources/road/endroad.png', 'assets/resources/road/endroad.png'),
    ('assets/resources/road/road.png', 'assets/resources/road/road.png'),
    ('assets/resources/road/t-road.png', 'assets/resources/road/t-road.png'),
    ('assets/resources/road/v-road.png', 'assets/resources/road/v-road.png'),

    ('assets/tutorial/tut1.png', 'assets/tutorial/tut1.png'),
    ('assets/tutorial/tut2.png', 'assets/tutorial/tut2.png'),
    ('assets/underconstruct.png', 'assets/underconstruct.png'),

    ('gamesave/dev123.txt', 'gamesave/dev123.txt'),

    ('Sounds/AmbientLoop1.mp3', 'Sounds/AmbientLoop1.mp3'),
    ('Sounds/Placing house SFX.mp3', 'Sounds/Placing house SFX.mp3'),
    ('Sounds/Placing Tree SFX.mp3', 'Sounds/Placing Tree SFX.mp3'),

    ('src/trivia1.json', 'src/trivia1.json'),
    ('src/trivia.json', 'src/trivia.json'),
    ('src/Grand9K Pixel.ttf', 'src/Grand9K Pixel.ttf'),
    # Include more files here...
]

build_exe_options = {
    "packages": ["os"], "excludes": ["tkinter"], "include_files": includefiles}

setup(
    name="Joxe",
    version="1.0",
    description="as above",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py")]
)