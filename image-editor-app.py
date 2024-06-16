import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageOps
import io

# Функция для применения фильтров
def apply_filter(image, filter_type, intensity):
    if filter_type == 'Черно-белый':
        return image.convert("L")
    
    elif filter_type == 'Размытие':
        return image.filter(ImageFilter.GaussianBlur(intensity))
    
    elif filter_type == 'Резкость':
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(intensity)
    
    elif filter_type == 'Контраст':
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(intensity)
    
    elif filter_type == 'Яркость':
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(intensity)
    
    elif filter_type == 'Инвертирование цветов':
        return ImageOps.invert(image.convert("RGB"))
    
    else:
        return image

# Функция для поворота изображения
def rotate_image(image, angle):
    return image.rotate(angle, expand=True)

# Функция для изменения размера изображения
def resize_image(image, width, height):
    return image.resize((width, height))

# Функция для добавления текста на изображение
def add_text(image, text, position, font_size, color):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(font_size)
    draw.text(position, text, fill=color, font=font)
    return image

st.title("Проект стуента Людмилы Федоровой")
st.title("Редактор изображений")

# Загрузка изображения
uploaded_file = st.file_uploader("Загрузите изображение", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Оригинальное изображение", use_column_width=True)

    st.write("### Выберите операцию")
    operation = st.selectbox("Операция", ["Нет", "Фильтр", "Поворот", "Изменение размера", "Добавление текста", "Инвертирование цветов"])

    if operation == "Фильтр":
        filter_type = st.selectbox("Тип фильтра", ["Черно-белый", "Размытие", "Резкость", "Контраст", "Яркость"])
        intensity = st.slider("Интенсивность", 0.0, 5.0, 1.0)
        edited_image = apply_filter(image, filter_type, intensity)

    elif operation == "Поворот":
        angle = st.slider("Угол поворота", 0, 360, 0)
        edited_image = rotate_image(image, angle)

    elif operation == "Изменение размера":
        width = st.number_input("Ширина", min_value=1, value=image.width)
        height = st.number_input("Высота", min_value=1, value=image.height)
        edited_image = resize_image(image, width, height)

    elif operation == "Добавление текста":
        text = st.text_input("Текст (только латинские символы)")
        position = (st.number_input("X позиция", min_value=0, max_value=image.width, value=0), 
                    st.number_input("Y позиция", min_value=0, max_value=image.height, value=0))
        font_size = st.number_input("Размер шрифта", min_value=1, value=20)
        color = st.color_picker("Цвет текста", "#FFFFFF")
        edited_image = add_text(image.copy(), text, position, font_size, color)

    elif operation == "Инвертирование цветов":
        edited_image = apply_filter(image, "Инвертирование цветов", 1)
    
    else:
        edited_image = image

    st.image(edited_image, caption="Измененное изображение", use_column_width=True)

    # Кнопка для сохранения изображения
    buffer = io.BytesIO()
    edited_image.save(buffer, format="PNG")
    buffer.seek(0)

    st.download_button(
        label="Скачать измененное изображение",
        data=buffer,
        file_name="edited_image.png",
        mime="image/png"
    )
else:
    st.write("Пожалуйста, загрузите изображение для редактирования.")
