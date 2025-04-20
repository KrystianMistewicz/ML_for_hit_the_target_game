from projectile_motion import ProjectileMotion
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from PIL import Image


class Graph():

    def __init__(self, target_distance, center_height, target_diameter, projectile_motion, palette='tab10', **kwargs):
        self.target_distance = target_distance
        self.center_height = center_height
        self.target_diameter = target_diameter
        self.projectile_motion = projectile_motion
        self.palette = palette
        self.kwargs = kwargs
        self.hue = 'attempt number'
        if type(self.projectile_motion) == ProjectileMotion:
            self.projectile_motion = [self.projectile_motion]
        self.data_list = []
        for number, pm in enumerate(self.projectile_motion):
            pm.data[self.hue] = number+1
            self.data_list.append(pm.data)
        self.data = pd.concat(self.data_list)
    
    def make_plot(self):
        sns.set_theme()
        fig, ax = plt.subplots()
        if 'title' in self.kwargs:
            plt.suptitle(self.kwargs['title'])
        self.x_max = self.target_distance
        self.y_max = max(2*self.center_height, self.data['y [m]'].max())
        try:
            path = os.path.join('images', 'player.png')
            with Image.open(path) as img:
                img_array = np.array(img)
                img_width, img_height = img.size
                initial_height = self.data[self.data['x [m]']==0]['y [m]'].mean()
                img_width = 0.1*self.x_max
                ax.imshow(img_array, aspect='auto', extent=[-img_width, 0, 0, initial_height])
            path2 = os.path.join('images', 'rectangle.png')
            with Image.open(path2) as img2:
                ax.imshow(img2, aspect='auto', extent=[-img_width, self.x_max, -0.03*self.y_max, 0])
                ax.imshow(img2, aspect='auto', extent=[self.x_max, self.x_max+0.03*self.x_max, -0.03*self.y_max, self.y_max])
        except FileNotFoundError as err:
            print(f"Image not found: {err}")
        plt.plot([-0.1*self.x_max, self.x_max], [0, 0], color='black', linewidth=2)
        plt.plot([self.x_max, self.x_max], [0, self.y_max], color='black', linewidth=2)
        self.target_thickness = 7
        plt.plot([self.target_distance, self.target_distance], [self.center_height - self.target_diameter / 2, self.center_height + self.target_diameter / 2], color='black', linewidth=self.target_thickness)
        plt.plot([self.target_distance, self.target_distance], [self.center_height - 7/9*self.target_diameter / 2, self.center_height + 7/9*self.target_diameter / 2], color='red', linewidth=self.target_thickness)
        plt.plot([self.target_distance, self.target_distance], [self.center_height - 5/9*self.target_diameter / 2, self.center_height + 5/9*self.target_diameter / 2], color='black', linewidth=self.target_thickness)
        plt.plot([self.target_distance, self.target_distance], [self.center_height - 3/9*self.target_diameter / 2, self.center_height + 3/9*self.target_diameter / 2], color='red', linewidth=self.target_thickness)
        plt.plot([self.target_distance, self.target_distance], [self.center_height - 1/9*self.target_diameter / 2, self.center_height + 1/9*self.target_diameter / 2], color='black', linewidth=self.target_thickness)
        sns.lineplot(data=self.data, x='x [m]', y='y [m]', hue=self.hue, palette=self.palette)
        plt.show()


if __name__ == '__main__':
    title = 'Hit the target game'
    pm = ProjectileMotion(0.394290, 1.916865, 12.115902, -32.352685)
    pm2 = ProjectileMotion(0.394290, 1.916865, 12.115902, 10)
    pm3 = ProjectileMotion(0.394290, 1.916865, 1, 80)
    Graph(0.394290, 1.396010, 0.673569, [pm, pm2, pm3], title=title).make_plot()