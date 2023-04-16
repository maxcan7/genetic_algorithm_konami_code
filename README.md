# **Genetic Algorithm to Learn the Konami Code**  
  
  
## **The Konami Code**  

The Konami Code is a common videogame cheat code:  
`"↑", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "START"`
  
  
## **Inspiration**  

I had wanted to learn how to write Genetic Algorithms for a long time, and I'd casually read some articles or played around with some code but it never quite clicked. I stumbled upon [this video](https://youtu.be/-kpcAa-qKwY) and it finally clicked for me when I started thinking about the genes as videogame controller inputs, and the idea of training a Genetic Algorithm to learn the Konami Code struck me.
  
  
## **Basic Description**  

This is a simple script to train a Genetic Algorithm to solve the Konami Code. This was written and conceived from scratch, for learning and demonstrative purposes.
  
  
### **Dependencies**  

This uses only standard libraries!
  
  
### **How to use**  

The script can be run as-is, or with the following parameters:  
  
**size:** The population size (i.e. playerbase) of "Players" learning the Konami Code. Default 25.  
**fitness_cutoff:** The number of Players selected for crossover in order of highest score. Default 5.  
**mutation_rate:** The percent chance of a given gene (i.e. gamepad input) mutating into any other random gene/input. Default 0.05 (5%).  
**win_percent:** The percentage of Players for a given generation that need to learn the Konami Code before the it is considered a success. Default 0.75 (75%).  
**max_iter:** A failsafe to break if the game exceeds a certain number of generations. Default 1000.  
  
  
### **Detailed Description**  
  
  
#### **Player**  

Each "Player" is represented by the Player class. The key understanding is that each Player is made up of an 11-digit dna strand, where the genes are any of the seven possible inputs:  
`"↑", "↓", "←", "→", "B", "A", "START"`  
  
  
#### **Populate**  

The populate function generates a playerbase of a given size, where dna are randomly selected from that set. For simplicity, mutation and fitness are calculated upon Player generation.
  
  
#### **Fitness**  

The test_fitness method for the fitness function is not the most efficient, but it works the best for the metaphor of being like a set of videogame controller inputs.  
  
Imagine each "gene" in the "dna" is a gamepad input. Each player has 1 Life. From left to right, the gene (the button they pressed) is compared to the Konami Code. If it's correct, their score goes up by one, if it's incorrect, they lose a life and it's game over.
  
  
#### **Selection**  

The players are sorted by highest-scoring, and the top fitness_cutoff players are selected for crossover.
  
  
#### **Crossover and Mutation**  

Among the survivors, we create a new generation of players of the same size as the original population.  
  
We randomly select any two Players and create a new dna strand. For each of the 11-digit sequence, we randomly select the gene from one parent. Since the parents were selected by score, they will be more likely to have correct gamepad inputs, so the offspring Players will be more likely to inherit correct gamepad input genes.  
  
Note that with crossover alone, we could wind up with a fail-state where no generation can possibly produce a Player capable of learning the Konami Code. For instance, if none of our starting population had the START gene, no offspring could inherit START, and therefore the Konami Code could not be learned.  
  
However, when a Player is created, its genes are automatically mutated by mutation_rate with the mutate method, so even in such a case, it is still possible to mutate into a winner. At the same time, mutations can be maladaptive, requiring more generations for the playerbase as a whole to learn the Konami Code.
  
  
#### **Play**  

After the initial population is created, all of the parameters and Player population are passed into the play function. At the beginning of each generation, it checks if win_percent of the Players have learned the Konami Code. If not, it Selects the top fitness_cutoff Players, creates a new playerbase via Crossover and Mutation, iterates the generation, and tries again until it meets the win condition or exceeds max_iter.
  
## **Example**  

This was a real run with the following parameters: `./genetic_algorithm_konami_code.py 25 5 0.05 0.5 1000`

But for simplicity I'll just show the Player_0 through Player_4 (remember these are new players each generation), and I'll also cut a lot of the generations, but keep enough so you can see the progression.  
  
Generation 0, the random initial population, had all scores of 0's so I'm skipping to Generation 1.  
```
Generation: 1
[
        Player_0:
        DNA: ['↑', '↑', '↓', '→', 'A', '↑', '↑', 'A', 'B', '→', 'A']
        SCORE: 3
        WINNER: False
        ,

        Player_1:
        DNA: ['START', '↑', '↓', 'START', '↓', '↑', '↑', 'A', 'B', 'B', 'A']
        SCORE: 0
        WINNER: False
        ,

        Player_2:
        DNA: ['↑', 'B', '↑', '↑', 'B', '←', 'B', '↓', '↓', 'A', '←']
        SCORE: 1
        WINNER: False
        ,

        Player_3:
        DNA: ['↑', 'START', '→', 'B', '↓', 'A', 'START', '↑', '←', 'B', '←']
        SCORE: 1
        WINNER: False
        ,

        Player_4:
        DNA: ['↑', '↑', '↓', '→', 'B', '→', 'B', 'A', '←', 'A', '←']
        SCORE: 3
        WINNER: False
        ]
```
  
Generation 1 has a variety of scores. Player_0 and Player_4 each got the first three inputs correct, player_2 and player_3 got the first input correct, and Player_1 got zero inputs correct. The select function would rank these as Player_0, Player_4, Player_2, Player_3, Player_1. The fact that there are ties doesn't really matter for our purposes.  
  
```
Generation: 2
[
        Player_0:
        DNA: ['↑', '↑', '↓', '→', 'A', '↑', '↑', 'A', '↓', '→', 'A']
        SCORE: 3
        WINNER: False
        ,

        Player_1:
        DNA: ['↑', '↑', '↓', '→', '↓', '→', 'B', 'A', 'B', '→', 'START']
        SCORE: 3
        WINNER: False
        ,

        Player_2:
        DNA: ['↑', '↑', '↓', '→', 'A', '↑', '↑', 'A', 'B', '→', 'B']
        SCORE: 3
        WINNER: False
        ,

        Player_3:
        DNA: ['↑', '↑', '↓', '→', '→', '↑', '↑', '↓', '↓', 'A', 'A']
        SCORE: 3
        WINNER: False
        ,

        Player_4:
        DNA: ['↑', '↑', '↓', '→', 'A', '↑', '↑', 'A', 'B', '→', 'A']
        SCORE: 3
        WINNER: False
        ]
```
  
Even just from the first 5 players, we can already see a pattern of higher scores, learning the left-most correct inputs.
  
```
Generation: 20
[
        Player_0:
        DNA: ['↑', '↓', '↓', '↓', '←', '→', '←', '→', 'B', '→', 'A']
        SCORE: 1
        WINNER: False
        ,

        Player_1:
        DNA: ['↑', '↑', 'B', '↓', '←', '→', '←', '→', 'START', '→', '←']
        SCORE: 2
        WINNER: False
        ,

        Player_2:
        DNA: ['↑', '↑', '↓', '↓', '←', '→', '←', '→', '↑', '→', 'START']
        SCORE: 8
        WINNER: False
        ,

        Player_3:
        DNA: ['←', '↑', '↓', '↓', '←', '→', '←', '→', 'START', '→', 'START']
        SCORE: 0
        WINNER: False
        ,

        Player_4:
        DNA: ['↑', '↑', '↓', '↓', '←', '→', '←', '→', 'B', '→', 'A']
        SCORE: 9
        WINNER: False
        ]
```
  
Skipping to generation 20, while there is still high variability in just these first five players, we can see that the scores are getting much higher. In the full 25 players of this generation it's even more apparent, but remember that mutation, or just random chance of selecting a bad gene during crossover, also reasonably explains this variability.   
  
```
Generation: 46
[
        Player_0:
        DNA: ['→', '↑', '↓', '↓', '←', '→', '↑', '→', 'B', 'A', 'START']
        SCORE: 0
        WINNER: False
        ,

        Player_1:
        DNA: ['↑', '↑', '↓', '↓', '←', '→', '←', '→', 'B', 'A', 'START']
        SCORE: 11
        WINNER: True
        ,

        Player_2:
        DNA: ['↑', '↑', '↓', '↓', '←', '→', '←', '→', 'B', 'A', 'START']
        SCORE: 11
        WINNER: True
        ,

        Player_3:
        DNA: ['↑', '↑', '↓', '↓', '←', 'B', '←', '→', 'B', 'A', 'START']
        SCORE: 5
        WINNER: False
        ,

        Player_4:
        DNA: ['↑', '↑', '↓', 'A', '←', '→', '←', '→', 'B', 'A', 'START']
        SCORE: 3
        WINNER: False
        ]
```
  
By Generation 46 we're starting to see winners, they're learning the Konami Code! This run, Generation 46 we start seeing the winners and then immediately after in Generation 47 it passes the win_percent, but this is not always the case, especially with higher mutation rates and higher win_percents.  
```
Generation: 47
[
        Player_0:
        DNA: ['↑', '↑', '↓', '↓', '←', 'START', 'B', '→', 'B', 'A', 'START']
        SCORE: 5
        WINNER: False
        ,

        Player_1:
        DNA: ['↑', '↑', '↓', '↓', '←', '→', '←', '→', 'B', 'A', 'START']
        SCORE: 11
        WINNER: True
        ,

        Player_2:
        DNA: ['↑', '↑', '↓', '↓', '←', '→', '←', '→', 'B', 'A', 'START']
        SCORE: 11
        WINNER: True
        ,

        Player_3:
        DNA: ['↑', '↑', '↓', '↓', '←', '→', '←', '→', 'B', 'A', 'START']
        SCORE: 11
        WINNER: True
        ,

        Player_4:
        DNA: ['↑', '↑', '↓', '↓', '←', '→', '←', '→', 'B', 'A', 'START']
        SCORE: 11
        WINNER: True
        ]
Generation 47 wins!
```  
  
### **TODOs**
- [ ] Unit Tests
- [ ] Makefile or CLI
- [ ] More efficient (even if less explanatory) fitness functions
- [ ] Better visualization tooling
- [ ] Check for additional code cleanup or optimizations
- [ ] Continue to improve documentation
