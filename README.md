#COA Maze Escape Game

COA Maze Escape is an educational 2D maze game built using Python and Pygame, designed to help students learn Computer Organization and Architecture (COA) concepts in an interactive way.

Players must navigate through maze rooms, collect keys, and unlock doors by answering COA-related questions correctly.

🎮 Game Features

🧩 Maze-based gameplay
🗝️ Key collection system
🚪 Locked doors with COA questions
📚 Educational focus on COA concepts
🎯 Progressive difficulty levels

Easy
Medium
Hard

🖼️ Custom sprites for player, key, and door

⌨️ Keyboard-controlled movement

🏗️ Game Mechanics
Maze Tiles Representation
Value	Meaning
0	Empty path
1	Wall
2	Player start position
3	Key
4	Door

COA Question Logic
Each room has different types of questions:
Room 1 (Easy)
→ Decimal to Binary conversion

Room 2 (Medium)
→ Binary to Decimal conversion

Room 3 (Hard)
→ Conceptual COA questions (ALU, registers, control unit, etc.)
You must answer correctly to unlock the door and move to the next room.

⌨️ Controls
Key	Action
⬆️	Move Up
⬇️	Move Down
⬅️	Move Left
➡️	Move Right
Enter	Submit answer
Backspace	Delete input

COA-Maze-Escape/
│
├── game.py
├── image.png.png   # Player sprite
├── key.png         # Key sprite
├── door.png        # Door sprite
└── README.md

🛠️ Requirements
Python 3.x
Pygame library

Install Pygame
pip install pygame

▶️ How to Run the Game
Make sure all image files are in the same directory as game.py
Run the game using:
python game.py

🎯 Objective

Navigate the maze
Collect the key 🗝️
Reach the door 🚪
Answer the COA question correctly
Escape all rooms 🎉

🚀 Future Improvements 

Sound effects & background music
Timer-based challenges
More COA question banks
Score system
Random maze generation
Multiplayer mode
