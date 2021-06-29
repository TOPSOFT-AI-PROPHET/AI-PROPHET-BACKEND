# AI-PROPHET-BACKEND


## 所有人记得先把 python 的 virtual enviroment 给激活了然后进入之后进行下列操作
## Make sure you have the python virtual enviroment before you run following steps
### 运行步骤
```shell
pip install -r requirements.txt
python manage.py runserver
```

### 数据库迁移部署
#### 如果不可以进行迁移，查看settings.py的 databse 账户密码设定，确定为本地的名字和密码 
#### If you cannot run migrations, plz check your main settings.py and make sure it is linked to your local one
```shell
python manage.py makemigrations
python manage.py migrate
```

### 创建超级用户
### create super admin
```shell
python manage.py createsuperuser
```

### 上传代码
#### 需要用 git status查看代码改动，不要覆盖不是你的代码
#### Use git status to select files you need to upload rather than adding in all changes
git status
git add XXXXXX
git commit -m "XXXXXX"
git push


POSTMAN intro: https://drive.google.com/drive/folders/1R72a4_txSHJGNKpygJAiwL_eq8OH6-Nv