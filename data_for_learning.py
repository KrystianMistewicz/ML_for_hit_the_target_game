import math
import numpy as np
import pandas as pd


class HitTargetGame:

    def __init__(self, samples_number: int,
                 target_distance_range: tuple[float],
                 center_height_range: tuple[float],
                 target_diameter_range: tuple[float],
                 initial_height_range: tuple[float],
                 velocity_range: tuple[float],
                 angle_range: tuple[float]):
        self.samples_number = samples_number
        self.target_distance_range = target_distance_range
        self.center_height_range = center_height_range
        self.target_diameter_range = target_diameter_range
        self.initial_height_range = initial_height_range
        self.velocity_range = velocity_range
        self.angle_range = angle_range
    
    def generate_data(self, save_to_csv: bool = False, save_to_xlsx: bool = False):
        """
        Generates data for learning.
        """
        self.target_distance = np.random.uniform(self.target_distance_range[0], self.target_distance_range[1], self.samples_number)
        self.center_height = np.random.uniform(self.center_height_range[0], self.center_height_range[1], self.samples_number)
        self.target_diameter = np.random.uniform(self.target_diameter_range[0], self.target_diameter_range[1], self.samples_number)
        self.initial_height = np.random.uniform(self.initial_height_range[0], self.initial_height_range[1], self.samples_number)
        self.velocity = np.random.uniform(self.velocity_range[0], self.velocity_range[1], self.samples_number)
        self.angle = np.random.uniform(self.angle_range[0], self.angle_range[1], self.samples_number)
        # Create a DataFrame from the generated data
        data_dict = {
            'target distance': self.target_distance,
            'center height': self.center_height,
            'target diameter': self.target_diameter,
            'initial height': self.initial_height,
            'velocity': self.velocity,
            'angle': self.angle
        }
        self.data = pd.DataFrame(data=data_dict)
        self.data['target reached'] = self.data.apply(
            lambda row: self.target_reached(row['target distance'],
                                             row['center height'],
                                             row['target diameter'],
                                             row['initial height'],
                                             row['velocity'],
                                             row['angle']), axis=1)
        if save_to_csv:
            self.data.to_csv('data.csv', index=False)
        if save_to_xlsx:
            self.data.to_excel('data.xlsx', index=False)
        return self.data
    
    @staticmethod
    def target_reached(d, ch, td, h0, V0, alpha):
        """
        Checks if the target is reached.
        If the projectile hits the target, it returns 1.
        If the projectile misses the target, it returns 0.
        """
        g = 9.81
        Vy0 = math.sin(alpha*math.pi/180)*V0
        Vx0 = math.cos(alpha*math.pi/180)*V0
        tf = (Vy0 + math.sqrt(Vy0**2 + 2*g*h0))/g
        xf = Vx0*tf
        if xf < d:
            return 0
        else:
            t = d/Vx0
            y = h0 + Vy0*t - 0.5*g*t**2
            if y >= ch - td/2 and y <= ch + td/2:
                return 1
            else:
                return 0


if __name__ == '__main__':
    htg = HitTargetGame(samples_number=100,
                        target_distance_range=(0, 10),
                        center_height_range=(1, 1.5),
                        target_diameter_range=(0.1, 1),
                        initial_height_range=(1, 2),
                        velocity_range=(0, 30),
                        angle_range=(-90, 90))
    data = htg.generate_data(save_to_csv=True, save_to_xlsx=True)
    print(data)