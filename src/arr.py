import numpy as np

# This script is here to generate the test data and write it ot disk.
# All cicrcles have a radius of less than 3.15


def generate_circle(nb_points):
    """generate a circle with nb_points points between 0 and 1"""
    points = np.zeros((nb_points, 2))
    for i in range(nb_points):
        points[i][0] = np.cos(2 * np.pi * i / nb_points) / 2 + 0.5
        points[i][1] = np.sin(2 * np.pi * i / nb_points) / 2 + 0.5
    return np.array(points)


def save_cicrcle_array(arr):
    """save the array to disk"""
    np.save('./data/circle_' + str(len(arr)) + '.npy', arr)


if __name__ == '__main__':
    nb_points = 50
    arr = generate_circle(nb_points)
    save_cicrcle_array(arr)
