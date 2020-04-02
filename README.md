# Dino_Game
*   Using pygame to program the google dinosaur. The game allows for two types of configurations.
    Currently, tensorflow has been deactivated for performance with CPU. Option 1 is to play the 
    game as a human, controls are the arrow keys.
    Option 2 is using the in game artificial intelligence. This is implemented with manual numpy
    neural networks with a genetic algorithm to adjust the weights for individual dinosaurs.

# Background
*   Genetic Algorithms
*   Neural Networks

# Set Up:
    `virtualenv -p python3 env`
    `source env/bin/activate`
    `pip install pygame`
    `pip install numpy`
    `pip install pandas`
    `pip install keras`
    `pip install tensorflow==2.0`
    `pip install matplotlib`
    `pip install seaborn`
    `pip install sklearn`
    `pip install os`

# Configurations:
* All configurations to game display and uses can be made in the config.py file.
  Look for the `MODIFIABLE GLOBAL CONFIGS` comment.
    * Global Configuration Variables
        * `VIEW_TRAINING` - Set `True` if want to see the game in action
        * `VIEW_GRAPHING` - Set `True` if want to see dynamic graphing per game
        * `HUMAN` - Set `True` if want to play the game with arrow keys
        * `SHOW_BOXES` - Set `True` if want to see boundary boxes around dinos and enemies
    
    * Genetic algorithm specific
        * `GA_POP` - Integer for population for genetic algorithm if in use
        * `MAX_GAMES` - Integer number of games/generations to play
        * `USE_PREV_GEN` - Set `True` to use previous generation dinos
        * `REC_CUT_OFF` - Integer recommended cutoff point to start saving weights

# How to Run:
    `python gen_dino_game.py`

    
# File Functionality:
* collect_states.py
    - Collect states from dino in game and post game.
    - Saves state data to csv files for machine learning training later on.
    - Also has a read in function to look at collected data.
* configs.py
    - Contains all the global configuration for all other files. Contains a series of flags.
* enemy_class.py
    - File that contains enemy class functionality.
* gen_alg.py
    - Genetic Algorithm to manage dino neural network weights.
    - This is borrowed from my genetic algorithm tuning directory with some modification.
* gen_dino_game.py
    - The main function to run. This contains the game that the users will play as well as the state collection.
    - Run this file when ready to play/train dino.
* manual_nn.py
    - Manual implementation of neural networks using numpy. References provided below for inspiration.
* player_class.py
    - File that contains player class functionality. Allows for multiple players.
* user_active.py
    - File for user controls with the gen_dino_game.
    
* Experimental/Deep_Q_Learning.py
    - Currently not in use - may delete this.
* Experimental/dino_game.py
    - Old version of dino game, currently not in use.
    - Used for experimenting with new gameplay features. Not updated.
* Experimental/train_nn.py
    - File specifically designed to train dino on user collected data and produce a model to play game.
    - Also provides dino with a single state to see what it predicts.


# Weight Files:
    "Dino[13]_Gen[21]_record[940].csv"      # Heads towards the front *
    "Dino[10]_Gen[13]_record[1000].csv"     # Heads towards the front *
    "Dino[16]_Gen[18]_record[1410].csv"     # Stays in the middle *
    "Dino[13]_Gen[14]_record[1270].csv"     # *
    "Dino[43]_Gen[19]_record[1170].csv"     # Stays towards back *
    "Dino[49]_Gen[19]_record[1000].csv"     # Stays towards the back
        
# References:
* Image tint
    * https://stackoverflow.com/questions/12251896/colorize-image-while-preserving-transparency-with-pil
* Pil to Pygame images:
    * https://stackoverflow.com/questions/25202092/pil-and-pygame-image    
* Where to get the color codes:
    * https://htmlcolorcodes.com/
* Random Color generation:
    * https://stackoverflow.com/questions/28999287/generate-random-colors-rgb
* Manual implementation of Neural network:
    * https://github.com/TheAILearner/Training-Snake-Game-With-Genetic-Algorithm
* Remove leading Zeros:
    * https://docs.scipy.org/doc/numpy/reference/generated/numpy.trim_zeros.html
* Numpy Neural Network Example Article:
    * https://towardsdatascience.com/lets-code-a-neural-network-in-plain-numpy-ae7e74410795
* Numpy Random Choice:
    * https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.random.choice.html
* Get files from Directories:
    * https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
* AI theory:
    * https://medium.com/ai%C2%B3-theory-practice-business/a-beginners-guide-to-numpy-with-sigmoid-relu-and-softmax-activation-functions-25b840a9a272
* Color Change Matplotlib:
    * https://www.codespeedy.com/how-to-change-line-color-in-matplotlib/
* Informational resource on neural networks:
    * https://ml4a.github.io/ml4a/neural_networks/

    
    
    