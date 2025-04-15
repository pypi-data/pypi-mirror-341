# Plot the policy results saved in .csv file

import pandas as pd
import matplotlib.pyplot as plt

class Logger:
    def plot_training(csv_path="log_PPO_Flappers.csv"):
        # Read the CSV file
        df = pd.read_csv(csv_path)

        # Create a figure and axis
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot the mean reward on the first y-axis
        ax1.plot(df['Episode'], df['avg length'], label='Average Length', color='blue')
        ax1.set_xlabel('Timesteps')
        ax1.set_ylabel('Average Length')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Create a second y-axis
        ax2 = ax1.twinx()
        ax2.plot(df['Episode'], df['reward'], label='Reward', color='red')
        ax2.set_ylabel('Reward')
        ax2.tick_params(axis='y', labelcolor='red')

        # Add a title and grid
        plt.title('Training Results')
        ax1.grid()

        # Show the plot
        plt.show()