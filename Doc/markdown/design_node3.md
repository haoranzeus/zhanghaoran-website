# 个人网站设计笔记3 #

上一篇笔记中主要是数据库，这一篇开始做表现的部分了。

表现部分先做的简单一点，先做两种页面，一个是主页，用来列出博客文章的链接，另一种是文章呈现的页面。

## 文章列表 ##

首先想要在主页显示文章的列表，在index.html中添加代码，参考书上的形式，是采用如下的代码：

	{% for entry in entries %}
	<a href="{{ url_for('.index', article=entry.title) }}">{{ entry.title }}</a>
	{% endfor %}

带用这种形式调用的url_for产生的url是：/?article=title1这样子，我想要一个固定的url，怎么办，用下面的形式：

	{% for entry in entries %}
	<a href="{{ url_for('.index') }}blog/{{ entry.id}}">{{ entry.title }}</a>
	{% endfor %}

这样url的形式就是/blog/1这样子。

## 文章显示模板 ##

增加一个文章显示模板app/templates/article.html

	{% extends "base.html" %}
	
	{% block title %}{{ entry.title }}{% endblock %}
	
	{% block page_content %}
	<div class="page-header">
	    <h1>{{ entry.title }}</h1>
	</div>
	    <body>{{ entry.text }}</body>
	{% endblock %}

这里简单的显示文章的标题和内容，待美化。

## 显示文章的路由 ##

在app/main/view.py中添加显示文章页面的路由

	@main.route('/blog/<int:id>')
	def article(id):
	    entry = Entries.query.get_or_404(id)
	    return render_template('article.html', entry=entry)

这里将文章的id值传入，通过该id在数据库表中查找相应内容。