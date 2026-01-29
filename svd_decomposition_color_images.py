import numpy as np
import matplotlib.pyplot as plt

def svd_recon_color(image, k):
    """
    Reconstruct a color image using the top k singular values for each color channel.
    :param image: H x W x 3 array (RGB)
    :param k: Number of singular values
    Returns: a reconstructed image clipped to [0, 255]
    """
    reconstructed = np.zeros_like(image)
    # applying svd on each channel
    for channel in range(3):
        U, S, VT = np.linalg.svd(image[:, :, channel], full_matrices=False)
        Uk = U[:, :k]
        Sk = np.diag(S[:k])
        Vk = VT[:k, :]
        reconstructed[:, :, channel] = Uk @ Sk @ Vk
    return np.clip(reconstructed, 0, 255)

def load_image(image_path):
    """
    Load image as float (0-255)
    :param image_path: File path to access image to be loaded
    """
    img = plt.imread(image_path).astype(float)
    # converting pngs with an alpha value to rgb
    if img.ndim == 2: img = np.stack([img]*3, axis=-1)
    elif img.shape[2] == 4: img = img[:, :, :3]
    return img

def plot_svd_color(image, k_values, save_dir="results"):
    """
    Show and save images with SVDs of given k values ran on it.
    :param image: An image to be loaded
    :param k_values: An array of various k values
    """
    import os
    os.makedirs(save_dir, exist_ok=True)
    fig, axes = plt.subplots(1, len(k_values), figsize=(15, 5))
    for i, k in enumerate(k_values):
        img_k = svd_recon_color(image, k)
        #auto save
        plt.imsave(f"{save_dir}/image_k{k}.png", img_k.astype(np.uint8))
        axes[i].imshow(img_k.astype(np.uint8))
        axes[i].set_title(f'k = {k}')
        axes[i].axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DVD collar image compression")
    parser.add_argument("image_path", type=str, help="Path to color image")
    parser.add_argument("--ks", type=int, nargs="+", default=[15, 25, 35, 45], help="List of k values for reconstruction")
    args = parser.parse_args()
    img = load_image(args.image_path)
    plot_svd_color(img, args.ks)