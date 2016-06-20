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

## 增加数据库元素 ##

目前数据库中仅有title和text两个列似乎太少了，还应该有个发布时间，另外，目前是直接用text的内容渲染文章页面，这样就没法显示板式，似乎可以将文章内容用markdown写好后生成html的格式，然后再将整个html格式的内容存入数据库，用它来渲染页面。

下面就写一个小工具来向数据库中增加一片文章，其中就包括html格式的文章内容。

小工具为tools/getText.py，内容如下：

	#!/usr/bin/python3
	
	import sys
	
	def usage():
	    print(
	    """
	    ./addarticle.py  <htmlfile>
	    """
	    )
	
	def getText(htmlfile):
	    with open(htmlfile) as f:
	        text = f.read()
	
	    return text

其实作用很简单，就是在python shell的过程中可以引用getText获取一个文件的内容，主要用于从markdown文件中获取内容，保存到一个变量。

## 增加markdown支持 ##

不想搞的太复杂，就是想先将文章写成markdown的形式，然后渲染到页面中，可能可以采用后端渲染的形式，但这种轻量级的东西貌似用前端渲染更合适。但javascript还不会，网上说可以用markdown-js这个东西，链接为：

[https://github.com/evilstreak/markdown-js/releases](https://github.com/evilstreak/markdown-js/releases "https://github.com/evilstreak/markdown-js/releases")

然后网上抄了段代码

	<textarea id="text-input" oninput="this.editor.update()">{{ entry.text }}</textarea>
	<div id="preview"> </div>
	<script src="{{ url_for('static', filename='markdown.js') }}"></script>
	<script>
	    function Editor(input, preview) {
	        this.update = function () {
	            preview.innerHTML = markdown.toHTML(input.value);
	        };
	        input.editor = this;
	        this.update();
	    }
	    var $ = function (id) { return document.getElementById(id); };
	    new Editor($("text-input"), $("preview"));
	</script>

这段代码其实我是不太会改的，前面那个textarea标签如果去掉了，就没有id参数了，也就不会显示后面的渲染结构，但如果不去掉，前面又有一段莫名其妙的框框显示markdown的原始字符串。