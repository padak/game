I want to make a "math crossword" game. It should have levels depending by math skills. When you chose level (easy, medium, hard), system will generate "crossword" which can fit to display of mobile phone. There has to be some numbers already filled, to guid you. bellow the crossword, there will be numbers which can be used for the blank places to finish the math equations. numbers bellow has to be complete - all numbers should fit to crossword. When you place number which doesn't bellow to crossword, system will color it by green or red, but not by if it fitst there but only if the math equation doesn't make sense. 
my goal is to run the game on my computer and let my daughter to connect to my computer where the game will run on the server (react web for instance).

ask me clarifying questions and make a description for the developer.

---

1. Clarifying Questions
	1.	Arithmetic scope
	•	Which operations must be supported (e.g. +, -, ×, ÷)?
	•	Are negative or fractional results allowed, or should all results be positive integers?
	2.	Puzzle constraints & difficulty
	•	How do you want to differentiate the easy/medium/hard levels?
	•	For instance, do you want simpler or fewer equations in the easy level, and more complex equations (or more squares) in the hard level?
	•	Do you have specific constraints on the size or shape of the crossword for each difficulty level?
	3.	Puzzle generation vs. fixed puzzles
	•	Do you want to generate these crosswords randomly on the fly, or do you plan to store pre-made puzzles and just show them based on difficulty?
	•	If random generation is desired, do you have a method/algorithm in mind?
	4.	Display and user interaction
	•	Will users drag and drop numbers from a “bank” of numbers below the crossword, or will they tap on a blank cell and choose from a set of numbers?
	•	Do you want immediate feedback as soon as a number is placed (red/green) or only when the user requests validation?
	5.	Validation rules
	•	You mentioned you want the game to color a placed number red or green “not by if it fits but only if the math equation doesn’t make sense.” Could you clarify the exact logic?
	•	Should the game check the arithmetic for each row/column in real time, or only the specific cell’s equation?
	6.	Completion logic
	•	How should the game confirm when the crossword is fully correct?
	•	Do you want partial credit or partial checks (e.g., a “you have X squares correct so far”)?
	7.	Data and state management
	•	Should progress be saved (i.e., so you can leave a puzzle and come back later)?
	•	Will there be a scoreboard or timer?
	8.	Multiplayer or single-user
	•	Is this purely single-player for your daughter, or do you imagine multiple users could connect simultaneously in the future?
	9.	Technical setup
	•	You mentioned “React web” and running on your computer. Will you be using Node.js for the server?
	•	Do you already have a hosting environment in mind, or will you run it locally with something like npm start or Docker?
	10.	Mobile layout

	•	Do you want a fully responsive design that automatically shrinks or rearranges the crossword puzzle to fit phone screens?
	•	Any specific device constraints?

----


1. yes, +,-,* and / (results should be whole numbers without decimals and all positive, no negative results
2. levels will differs by amount of prefiled numbers and complexity of equations
3. generata puzzle on the fly, no specific algorithm in my mind
4. user will drag and drop or click to number (select it) and click to place where number should be placed, if placed number finished equation, it should be immediately validated. equations should be only done by "X (math operation) Y = Z" - no "a + b + c = d", so two numbers and third is result
5. validation: I'll have puzzle " X + Z = 5" and if I place X=2, it will make it green (it is - as of now - ok) and once I place Z = 3, whole equation will be green. If I place Z = 2, Z will be RED
6. final confirmation is done by popup with congratulation
7. no state and no scoreboard - keep it simple in version 1
8. yes, two players can join the game. "server" will only play one game and up to two players should be able to play together
9. react was just idea - design best technology for me, I'm not an expert, it will run only on my computer
10. crossword should not rearrange during the game - it will piss off players

update the description for developer if you have no more questions. make the description as a markdown file