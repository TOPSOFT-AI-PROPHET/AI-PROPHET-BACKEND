# AI-PROPHET-BACKEND

## 所有人记得先把 python 的 virtual enviroment 给激活了然后进入之后进行下列操作
### 运行步骤
```shell
pip install -r requirements.txt
python manage.py runserver
```

### 数据库迁移部署
#### 如果不可以进行迁移，查看settings.py的 databse 账户密码设定，确定为本地的名字和密码 
```shell
python manage.py makemigrations
python manage.py migrate
```

### 创建超级用户
```shell
python manage.py createsuperuser
```
