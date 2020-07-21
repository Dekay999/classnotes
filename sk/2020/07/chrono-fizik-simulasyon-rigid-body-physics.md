# 3D Fizik Simulasyonu, Chrono

Daha önce 2 boyut için gördüğümüz simülasyon yazılımının 3 boyutta
karşılı Chrono. Derlemek için bazı bilgiler,

http://api.projectchrono.org/4.0.0/tutorial_install_chrono.html

Kurmak için önce

https://gitlab.com/libeigen/eigen/-/archive/3.3.7/eigen-3.3.7.tar.gz

Açıp dizine girilir, ve

```
mkdir build_dir

cd build_dir

cmake ..

sudo make install
```

Eigen sadece header .h dosyaları, derlenen bir şey yok.

Chrono derlemeden önce kurulması gereken Ubuntu programları,

```
sudo apt-get install libirrlicht-dev swig freeglut3-dev libgl1-mesa-dev libx11-dev
```

Simdi Chrono paketinin kendisine gelelim,

Chrono

```
git clone https://github.com/projectchrono/chrono.git

cd chrono

mkdir build_dir

cd build_dir

cmake -DENABLE_MODULE_IRRLICHT=TRUE \
      -DENABLE_MODULE_PYTHON=TRUE \
      -DENABLE_MODULE_POSTPROCESS=TRUE \
      -DCMAKE_BUILD_TYPE=Debug ..
```

Artık `chrono/build_dir/bin` altında görülen bir sürü program
işletilebilir. Mesela

```
./demo_IRR_bricks
```

![](chrono.png)


Eğer kendi kodladığımız, kendi başına ayrı bir projeyi Chrono
kullanacak şekilde derlemek istiyorsak, `chrono/template_project`
altına gidebiliriz (ya da oradaki kodları herhangi bir yere
kopyalayıp, vs), ve

```
cmake -DCMAKE_BUILD_TYPE=Debug \
      -DChrono_DIR=/home/user/Downloads/repos/chrono/build_dir/cmake \
      /home/user/Downloads/repos/chrono/template_project
```

işletiriz. Bu işlem bir `Makefile` üretmiş olmalı. onu `make` ile
derleriz, ve `template_project/build/myexe` olarak bir işletilebilir
program üretilmiş olmalı. Onu rahatlıkla işletebiliriz. 


