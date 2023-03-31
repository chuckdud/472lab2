cddudley 472 lab2 solution

	usage: $ python3 main.py

	The program will prompt the user to make selections about how each player will select actions. 
	
		There are 3 options:

			USER: the user will manually select x and y coordinates of valid actions
			RANDOM: a valid action will be randomly selected for each state
			SEARCH: a valid action will be selected according to alpha-beta-cutoff search
		
			if user selects SEARCH, they will also be prompted to select a maximum depth
				and an evaluation function to follow.

			Each player can use use different functions to select actions.

			Each player can have different evaluation functions and maximum depths.

	The user will also be prompted to select a number of games to play. 

	The program will print each game state along with each action selected by players.

	Once all games have been completed, a count of wins for each player will be printed.
