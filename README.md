Driver for Table 10Moons on Linux
=================================

** Create Package

pyinstaller --exclude-module /build --exclude-module /__pycache__ --exclude-module /driver/__pycache__ --exclude-module /dist --add-data 'driver:.' --onefile main.py

pyinstaller --clean main.spec

** Run in /dist

sudo ./main



![tmoons](https://user-images.githubusercontent.com/14333871/184971313-2d859133-ef4f-431a-98db-5f00444b396b.gif)



** Download

https://drive.google.com/drive/folders/12p1a4NG2-gK_JdMvcwZ4WOKl7Iff076X?usp=sharing

Tested with table T503


Credits

Some parts of code are taken from: https://github.com/Mantaseus/Huion_Kamvas_Linux

Base: https://github.com/alex-s-v/10moons-driver
