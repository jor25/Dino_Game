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
* Deep_Q_Learning.py
    - Currently not in use - may delete this.
* dino_game.py
    - Old version of dino game, currently not in use.
    - Used for experimenting with new gameplay features. Not updated.
* gen_dino_game.py
    - The main function to run. This contains the game that the users will play as well as the state collection.
    - Run this file when ready to play/train dino.
* train_nn.py
    - File specifically designed to train dino on user collected data and produce a model to play game.
    - Also provides dino with a single state to see what it predicts.
* user_active.py
    - File for use controls with the gen_dino_game.

# Modifications:
* Always update the human and neural booleans in gen_dino file,
  these determine whether or not to collect data from human user,
  or use the neural network.


# References:
* Image tint
    * https://stackoverflow.com/questions/12251896/colorize-image-while-preserving-transparency-with-pil
* Pil to Pygame images:
    * https://stackoverflow.com/questions/25202092/pil-and-pygame-image    
    