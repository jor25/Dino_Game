# Dino_Game
* Using pygame to program the google dinosaur.

# Set Up:
* May just make a makefile for these start up commands.
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

# Modifications:
* Always update the human and neural booleans in gen_dino file,
  these determine whether or not to collect data from human user,
  or use the neural network.

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