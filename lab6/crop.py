import os
import numpy as np
from PIL import Image


def find_white_pixels(mask_image):
    # Конвертируем изображение в массив numpy
    mask_array = np.array(mask_image)

    # Находим координаты белых пикселей
    white_pixels = np.argwhere(mask_array >= 230)

    if len(white_pixels) == 0:
        return None  # Если белых пикселей нет

    # Находим крайние координаты белых пикселей
    y_min = white_pixels[:, 0].min()  # Минимальные координаты Y
    y_max = white_pixels[:, 0].max()  # Максимальные координаты Y
    x_min = white_pixels[:, 1].min()  # Минимальные координаты X
    x_max = white_pixels[:, 1].max()  # Максимальные координаты X

    return x_min, y_min, x_max, y_max


def crop_images(image_folder, mask_folder, output_image_folder, output_label_folder, padding=10):
    os.makedirs(output_image_folder, exist_ok=True)
    os.makedirs(output_label_folder, exist_ok=True)

    for filename in os.listdir(mask_folder):
        # Оставляем только маски в формате .png и .jpg
        if filename.endswith('.png') or filename.endswith('.jpg'):
            # Получаем пути к изображению и маске
            mask_path = os.path.join(mask_folder, filename)
            image_path = os.path.join(image_folder, filename)

            # Открываем маску и изображение
            mask_image = Image.open(mask_path).convert('L')  # Конвертируем в градации серого
            original_image = Image.open(image_path)

            # Находим координаты обрезки
            coords = find_white_pixels(mask_image)
            if coords:
                x_min, y_min, x_max, y_max = coords

                # Добавляем боковые границы (padding) к обрезке
                x_min = max(x_min - padding, 0)  # Не позволяем x_min уходить за пределы изображения
                y_min = max(y_min - padding, 0)  # Не позволяем y_min уходить за пределы изображения
                x_max = min(x_max + padding, original_image.width)
                y_max = min(y_max + padding, original_image.height)

                # Определяем область обрезки
                crop_box = (x_min, y_min, x_max, y_max)

                # Обрезаем изображение и маску
                cropped_image = original_image.crop(crop_box)
                cropped_mask = mask_image.crop(crop_box)

                # Сохраняем обрезанные изображения
                cropped_image.save(os.path.join(output_image_folder, filename))
                cropped_mask.save(os.path.join(output_label_folder, filename))

# Пример использования
crop_images('images_touching', 'labels_touching', 'images_touching_crop', 'labels_touching_crop', padding=10)