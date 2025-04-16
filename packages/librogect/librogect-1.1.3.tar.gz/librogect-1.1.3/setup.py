from setuptools import setup, find_packages

setup(name="librogect",  # Название вашего пакета
    version="1.1.3",  # Версия вашего пакета
    packages=find_packages(),  # Автоматически находит все пакеты
    install_requires=[],  # Зависимости вашего пакета
    description="Использование: Так как это молодая библиотека, многое придётся сделать вручную. Чтобы начать поиск корней, нужно написать команду resh('(-) (a)x^2 +(-) (b)x +(-) (c) = 0'). Вместо (a), (b), (c) нужно уточнить числа. Если нужно, чтобы a или b были равны единице перед x^2 или x соответственно, то перед ними следует написать 1. Также с 0. Также она может построить график функции. Прошу не брать большие отрезки осей, если у вас слабое устройство. ",
    author=" Никитос ",  # Ваше имя
    author_email="matika059@gmail.com",  # Ваш email
    classifiers=[
        "Programming Language :: Python :: 3",  # Версия Python
        "License :: OSI Approved :: MIT License",  # Лицензия
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6')