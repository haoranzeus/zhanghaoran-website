# 个人网站设计笔记2 #

在上一篇中我照着《Flask Web设计》搭建了一个web的程序框架，下面继续做开发。如果不需要接受评论，而且只有我一个人写文章的话，当然是可以使用静态页面，但既然向做，就做点好玩的，加点数据库啥的，这篇一个主要任务就是添加数据库。在添加数据库之前，先来做点美化工作，添加一个网站的favicon.ico。

## 添加收藏夹图标 ##

首先找个喜欢的图片，不能太复杂，太复杂的图片小小的图标也呈现不出来。

然后上网搜favicon.ico在线制作，就可以制作一个favicon.ico图标了。

创建app/static路径，用于存放静态文件，比如图片，css样式文件等，将生成的favicon.ico放到该路径下。

可以在app/template/base.html中添加如下代码：

	{% block head %}
	{{ super() }}
	<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}" type="image/x-icon">
	<link rel="icon" href="{{ url_for('static', filename = 'favicon.ico') }}" type="image/x-icon">
	{% endblock %}

这样图标的声明会插入head块的末尾。注意使用super()保留基模板中定义的块的原始内容。

## 数据库设计 ##

中间间断了好长时间，今天继续。

数据库先采用简单的，由于是个人网站，只有一个人写文章，也就无所谓作者了。不考虑什么评论之类的，那么就只需要一个名为entries表，三个表项：

- id
- title
- text

首先在app/__init__.py中创建数据库实例：

	db = SQLAlchemy()

由于使用了蓝本，现在还没有一个app可供数据库实例初始化，和其他的扩展一样，可以在create_app工厂函数中调用扩展的init_app()函数进行初始化。

	db.init_app(app)

在app/models.py中创建数据库表，也就是model，表类继承自db.Model，内容如下：

	from . import db
	
	class Entries(db.Model):
	    __tablename__ = "entries"
	    id = db.Column(db.Integer, primary_key=True)
	    title = db.Column(db.String(64), unique=True, nullable=False)
	    text = db.Column(db.Text, nullable=False)

现在可以创建数据库了，在shell环境下运行：

	$ python manage.py shell
	>>> from app import db
	>>> db.create_all()

此时其实数据库就已经创建好了。如果使用的是sqlite3，可以看到当前目录下生成了一个数据库文件。

我们还可以使用已经定义好的models.py添加一些数据

	>>> from app.models import Entries
	>>> artical1 = Entries(title="title1", text="text1")
	>>> print(articl1.title)
	title1
	>>> print(articl1.text)
	text1
	>>> print(articl1.id)
	None

新建对象的主键的id属性并没有确定，因为主键是由Flask-SQLAlchemy管理的。现在这些对象只存在于Python中，还未写入数据库。因此id尚未赋值。

通过数据库会话管理对数据库所做的改动，在Flask-SQLAlchemy中，会话由db.session表示。准备把对象写入数据库之前，先要将其添加到会话中。

	>>> db.session.add(artical1)

当有多个对象需要添加时，可以将对象组成列表，使用db.session.add_all([articl1, articl2 ..., articln])这样的形式添加

把对象写入数据库，使用commit()方法提交会话。

	>>> db.session.commit()

### 继承Python shell ###

每次启动Python shell的时候都需要手动import数据库实例和模型，比较麻烦，可以注册一个回调函数，让Flask-Script的shell命令导入特定对象：

	from flask_script import Shell

	def make_shell_context():
		return dict(app=app, db=db, Entries=Entries)
	manager.add_command("shell", Shell(make_context=make_shell_context))

这样以后启动Python shell，这些个东东不需要import就可以用了。

### 使用Flask-Migrate实现数据库迁移###

书上说有个Alembic的工具可以用来实现数据库迁移，另一个选择是Flask-Script

	pip install flask-migrate

在manage.py中添加如下代码：

	from flask_migrate import Migrate, MigrateCommand

	migrate = Migrate(app, db)
	manager.add_command('db', MigrateCommand)

然后可以使用如下命令创建迁移仓库：

	$ python manage.py db init

自动创建迁移脚本：

	$ python manage.py db migrate -m "initial migration"

当修改了model后，使用下面命令进行迁移：

	python manage.py db upgrade







