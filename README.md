# [WIP]交互式人脸检索系统

## 简介

此系统所要解决的问题是，在目标人脸不清晰或者根本没有数字图像的情况下，在人脸数据库中通过有限轮次的检索，识别出目标。在每一轮次的检索中，用户选择本轮反馈图像中与目标最相像的，系统利用图像之间的特征距离逐步给出最可能的结果，反复进行如上步骤，直到目标人脸被找到。

## 技术栈

* 后端： Falcon + PostgreSQL
* 前端： Vue + vue element admin

## 生产环境部署

### install

sudo docker-compose up -d --no-deps --build backend huey postgres redis nginx

## 访问

http://localhost

用户名账号随便填

## dev


docker-compose run  --service-ports backend

### 后端

apt install postgresql
pipenv install -python pypy3
pipenv install

### 前端

cd web
yarn install


## run

pipenv shell
<!-- gunicorn application.app -->
gunicorn application.app -k gevent --timeout 300 --reload
huey_consumer.py application.tasks.huey

cd web && yarn dev
<!-- docker run --detach -p 80:8000 flask_gunicorn_app -->
## 特征文件规范

### 命名

<!-- *.dat -->

### 格式

文件为CSV格式，首行为照片名列表，照片名列表请按字符串升序，例如。
特征文件的照片列表应该和照片库的照片列表完全一致（数量一致，文件名一致）
`
1.jpg 2.jpg 3.jpg
// 1.jpg 的维度特征
// 2.jpg 的维度特征
// 3.jpg 的维度特征
`

## 距离文件规范

### 命名


### 格式

文件为CSV格式，首行以及首列为照片名列表，单元格(i,j)的值第i张图片到第j张图片的距离，为了节省空间可以使用上三角矩阵，格式示例如下。
距离文件的照片列表应该和照片库的照片列表完全一致（数量一致，文件名一致）

`
（备注）亦可留空 1.jpg,         2.jpg               3.jpg
1.jpg 0     dis('1.jpg', '2.jpg') dis('1.jpg', '3.jpg')
2.jpg /               0           dis('1.jpg', '3.jpg')
3.jpg /               /                  0
`

<!-- # docker -->

<!-- docker build .  -t cosformula/face-retrievatl:<tag> -->
<!-- docker-compose up -d --no-deps --build web postgres redis
docker-compose run web -->