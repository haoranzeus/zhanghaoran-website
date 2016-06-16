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

在app/models.py中创建数据库，内容如下：

	from . import db
	
	class Role(db.Model):
	    __tablename__ = "enteries"
	    id = db.Column(db.Integer, primary_key=True)
	    title = db.Column(db.String(64), unique=True, nullable=False)
	    text = db.Column(db.Test, nullable=False)

