from PIL import Image
from datetime import timedelta
from timeit import default_timer as timer
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils.extmath import randomized_svd

from src.algorithms.compression.compress_matrix_utils import matrix_vector_mult
from src.algorithms.compression.compress_tree import CompressTree
from src.algorithms.compression.visualizer import CompressTreeBitmapVisualizer, CompressTreeStructureVisualizer
from tests.test_compress_matrix_utils import generate_full_matrix, \
    generate_full_vector


def visualize_compressed_image(image_path, crop_box, r=4, sigma_n=512):
    image = Image.open(image_path)
    image = image.crop(crop_box)
    image = image.convert("RGB")
    # image.show()
    bitmap = np.array(image)
    red_channel = bitmap[:, :, 0]
    green_channel = bitmap[:, :, 1]
    blue_channel = bitmap[:, :, 2]

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.imshow(red_channel, cmap="Reds")
    plt.title("Red Channel")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(green_channel, cmap="Greens")
    plt.title("Green Channel")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(blue_channel, cmap="Blues")
    plt.title("Blue Channel")
    plt.axis("off")

    plt.show()

    _, R_sigma, _ = randomized_svd(red_channel, n_components=sigma_n, random_state=0)
    _, G_sigma, _ = randomized_svd(red_channel, n_components=sigma_n, random_state=0)
    _, B_sigma, _ = randomized_svd(red_channel, n_components=sigma_n, random_state=0)

    print(R_sigma, G_sigma, B_sigma)
    x = np.arange(0, sigma_n)
    plt.title("Singular values for RGB channels")
    plt.plot(x, R_sigma, label="Red Channel", color="red")
    plt.plot(x, G_sigma, label="Green Channel", color="green")
    plt.plot(x, B_sigma, label="Blue Channel", color="blue")
    plt.xlabel('i')
    plt.ylabel('y')
    plt.yscale('log')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, shadow=True, ncol=1)
    plt.grid()
    plt.show()
    R_sigma=R_sigma[-1]
    G_sigma=G_sigma[-1]
    B_sigma=B_sigma[-1]
    red_tree = CompressTree(red_channel, 0, red_channel.shape[0], 0, red_channel.shape[1])
    red_tree.compress(r, R_sigma)

    green_tree = CompressTree(green_channel, 0, green_channel.shape[0], 0, green_channel.shape[1])
    green_tree.compress(r, G_sigma)

    blue_tree = CompressTree(blue_channel, 0, blue_channel.shape[0], 0, blue_channel.shape[1])
    blue_tree.compress(r, B_sigma)

    visualizer_red = CompressTreeStructureVisualizer(red_tree)
    visualizer_green = CompressTreeStructureVisualizer(green_tree)
    visualizer_blue = CompressTreeStructureVisualizer(blue_tree)

    visualizer_red.visualize_tree_structure()
    visualizer_green.visualize_tree_structure()
    visualizer_blue.visualize_tree_structure()

    visualizer_red_ = CompressTreeBitmapVisualizer(red_tree)
    visualizer_green_ = CompressTreeBitmapVisualizer(green_tree)
    visualizer_blue_ = CompressTreeBitmapVisualizer(blue_tree)

    red_compressed = visualizer_red_.draw_bitmap()
    green_compressed = visualizer_green_.draw_bitmap()
    blue_compressed = visualizer_blue_.draw_bitmap()

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.imshow(red_compressed, cmap="Reds")
    plt.title("Red Channel")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(green_compressed, cmap="Greens")
    plt.title("Green Channel")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(blue_compressed, cmap="Blues")
    plt.title("Blue Channel")
    plt.axis("off")

    plt.show()

    reconstructed_bitmap = np.stack([red_compressed, green_compressed, blue_compressed], axis=-1)

    reconstructed_image = Image.fromarray(reconstructed_bitmap)
    reconstructed_image.show()


def lab3():
    image_path = "images/city.jpg"
    crop_box = (0, 0, 512, 512)
    visualize_compressed_image(image_path, crop_box)


def lab4():
    r = 1
    epsilon = 1e-7
    for k in [4]:
        matrix = generate_full_matrix(k)
        compressed_matrix = CompressTree(matrix, 0, matrix.shape[0], 0, matrix.shape[1])
        compressed_matrix.compress(r, epsilon)
        print("compressed")
        # visualizer = CompressTreeStructureVisualizer(compressed_matrix)
        # visualizer.visualize_tree_structure()
        vector = generate_full_vector(k)
        y = matrix @ vector
        # y = matrix @ matrix
        start = timer()
        y_dash = matrix_vector_mult(compressed_matrix, vector)
        # y_dash = matrix_matrix_mult(compressed_matrix, compressed_matrix).decompress()
        end = timer()
        time_elapsed = end - start
        print(f"Time for k={k}: {timedelta(seconds=time_elapsed)}")
        print(f"Time in seconds: {time_elapsed}")
        frobenius_norm = np.sum((y - y_dash) ** 2)
        print(frobenius_norm)

def main():
    lab4()

if __name__ == "__main__":
    main()