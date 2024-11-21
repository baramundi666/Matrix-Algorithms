class CompressTreeVisualizer:
    def __init__(self, compress_tree):
        self.compress_tree = compress_tree

    def reconstruct_block(self, node):
        if node.is_leaf:
            if node.zeros:
                return np.zeros((node.t_max - node.t_min, node.s_max - node.s_min))
            else:
                return node.U @ np.diag(node.S) @ node.V
        else:
            raise ValueError("Node is not a leaf.")

    def reconstruct_matrix(self):
        matrix = np.zeros_like(self.compress_tree.matrix)
        stack = [self.compress_tree]

        while stack:
            node = stack.pop()
            if node.is_leaf:
                block = self.reconstruct_block(node)
                matrix[node.t_min:node.t_max, node.s_min:node.s_max] = block
            else:
                stack.extend(node.children)

        return matrix

    def draw_matrix(self):
        matrix = self.reconstruct_matrix()
        plt.imshow(matrix, cmap="viridis", aspect="auto")
        plt.colorbar(label="Values")
        plt.title("Reconstructed Matrix from Compressed Tree")
        plt.show()


# Przykladowa macierz i kompresja
original_matrix = np.random.rand(16, 16)
tree = CompressTree(original_matrix, 0, 16, 0, 16)
tree.compress(r=2, epsilon=1e-2)

# Rysowanie
# visualizer = CompressTreeVisualizer(tree)
# visualizer.draw_matrix()

from PIL import Image
import numpy as np



# image = Image.open("mouse-80quality.jpg")
# image = image.crop((200, 200, 328, 328))
#
# # Konwertuj obraz na RGB (w razie potrzeby)
# rgb_image = image.convert("RGB")
#
# # Przekształć dane obrazu na macierz NumPy
# bitmap = np.array(rgb_image)
#
# print(bitmap)



from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


class CompressTreeBitmapVisualizer(CompressTreeVisualizer):
    def draw_bitmap(self):
        matrix = self.reconstruct_matrix()
        # Konwersja do obrazu
        return matrix


def visualize_compressed_image(image_path, crop_box, r=2, epsilon=1e-2):
    # 1. Załaduj obraz
    image = Image.open(image_path)
    image = image.crop(crop_box)
    image = image.convert("RGB")  # Konwersja na RGB
    image.show()
    bitmap = np.array(image)

    # 2. Wyodrębnij kanały RGB
    red_channel = bitmap[:, :, 0]
    green_channel = bitmap[:, :, 1]
    blue_channel = bitmap[:, :, 2]

    # 3. Kompresuj kanały
    red_tree = CompressTree(red_channel, 0, red_channel.shape[0], 0, red_channel.shape[1])
    red_tree.compress(r, epsilon)

    green_tree = CompressTree(green_channel, 0, green_channel.shape[0], 0, green_channel.shape[1])
    green_tree.compress(r, epsilon)

    blue_tree = CompressTree(blue_channel, 0, blue_channel.shape[0], 0, blue_channel.shape[1])
    blue_tree.compress(r, epsilon)

    # 4. Wizualizacja osobnych kanałów
    visualizer_red = CompressTreeBitmapVisualizer(red_tree)
    visualizer_green = CompressTreeBitmapVisualizer(green_tree)
    visualizer_blue = CompressTreeBitmapVisualizer(blue_tree)

    red_compressed = visualizer_red.draw_bitmap()
    green_compressed = visualizer_green.draw_bitmap()
    blue_compressed = visualizer_blue.draw_bitmap()

    # Wyświetlenie każdego kanału
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

    # 5. Rekonstrukcja pełnego obrazu RGB
    reconstructed_bitmap = np.stack([red_compressed, green_compressed, blue_compressed], axis=-1)

    # 6. Wyświetlenie pełnego obrazu
    reconstructed_image = Image.fromarray(reconstructed_bitmap)
    reconstructed_image.show()


# Przykładowe użycie
image_path = "city.jpg"
crop_box = (200, 200, 328, 328)
# crop_box = (0, 0, 512, 512)
visualize_compressed_image(image_path, crop_box)





