# 个人网站设计笔记1 #

工作比较无聊，想做点有点创造性，有点成就感的事情，那就试着做个个人网站吧。没有相关经验，估计后来会困难重重。不过现在互联网各种资料一应俱全，网站的开发也因为一些新工具的产生而越来越简单。

这个网站打算采用Python的Flask框架，基础知识从一本叫《Flask Web开发》的动物书上获得。

毕竟是一个摸索的过程，所以文档也先采用按照时间线记录流水账的形式。

## 项目结构 ##

按照《Flask Web开发》设计项目结构。

	|- zhanghaoran-website
		|- app/
			|- templates/
				|- base.html
				|- index.html
				|- 404.html
				|- 500.html
			|- static/
			|- main/
				|- __init__.py
			__init__.py
		|- migrations/
		|- tests/
		|- venv/
		|- config.py
		|- manage.py

其中app作为程序包，用来保存程序的所有代码、模板和静态文件。migrations文件夹包含数据库迁移脚本。单元测试编写在tests包中。venv文件夹包含Python虚拟环境。

config.py用于预存一些配置选项，比如开发、测试的选项。manage.py作为启动脚本。

## 创建虚拟环境 ##

Python3已经出来了有一段时间了，既然是新手，不存在什么代码兼容的问题，自然是要选择新的版本。这里选择Python3作为我的开发版本。

首先要创建一个虚拟环境，在之前fedora的环境下可以使用如下命令：

	$ python3 -m venv venv

但是在ubuntu下竟然会报错：

	The virtual environment was not created successfully because ensurepip is not
	available.  On Debian/Ubuntu systems, you need to install the python3-venv
	package using the following command.

    	apt-get install python3-venv

	You may need to use sudo with that command.  After installing the python3-venv
	package, recreate your virtual environment.

当然，也没有一个叫做python3-venv的包可以安装。在网上搜索，貌似这是Python3.4在ubuntu上的一个bug。网上的一个解决方式是生成不包含pip的虚拟环境，然后手动安装pip。
	
	1) Create the venv with --without-pip. For instance:
	$ python3 -m venv venv --without-pip
	2) Download https://bootstrap.pypa.io/get-pip.py as ~/tmp/get-pip.py.
	3) Bootstrap pip "manually" in your venv:
	<venv-dir>/bin/python ~/tmp/get-pip.py

按照这个方法做，有效！

## 编写配置选项文件config.py ##

配置选项是为了在不同的环境中采用不同的配置，比如开发、测试、生产环境要使用不同的数据库。我们将配置信息写在一个独立的文件中config.py。

代码如下：

	import os
	basedir = os.path.abspath(os.path.dirname(__file__))
	
	
	class Config:
	    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	
	    @staticmethod
	    def init_app(app):
	        pass
	
	
	class DevelopmentConfig(Config):
	    DEBUG = True
	    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
	            'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
	                                                          
	                                                          
	                                                          
	class TestingConfig(Config):                          
	    TESTING = True                                    
	    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
	            'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
	                                                      
	                                                      
	class ProductionConfig(Config):                       
	    pass                                              
	    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	            'sqlite:///' + os.path.join(basedir, 'data.sqlite')
	                                             
	                                                      
	config = {                                            
	        'development': DevelopmentConfig,             
	        'testing': TestingConfig, 
	        'production': ProductionConfig,
	                                  
	        'default': DevelopmentConfig,
	        }  

其中SECRET_KEY用于一些需要密钥的地方，需要从环境变量读取以确保安全。

SQLALCHEMY_COMMIT_ON_TEARDOWN和SQLALCHEMY_URI是Flask-sqlalchemy里定义的配置，前者表示每次request自动提交db.session.commit()，后者表示数据库的绝对路径。

配置类可以定义init_app()类方法，其参数是程序实例。在这个方法中，可以执行对当前环境的配置初始化。现在，基类Config中的init_app()为空。

## 在程序包的构造文件中使用工厂函数 ##

工厂函数可以延迟创建程序实例，把创建过程移到可显示调用的工厂函数中。这种方法不仅可以给脚本留出配置程序的时间，还能够创建多个程序实例，这些实例有时在测试中非常有用。

app/__init__.py的代码如下：
	
	from flask import Flask, render_template
	from flask.ext.bootstrap import Bootstrap
	from flask.ext.moment import Moment
	from flask.ext.sqlalchemy import SQLAlchemy
	from config import config
	
	
	bootstrap = Bootstrap()
	moment = Moment()
	db = SQLAlchemy()
	
	
	def create_app(config_name):
	    """factory function of app.
	    config_name: configure name defined in config.py"""
	
	    app = Flask(__name__)
	    app.config.from_object(config[config_name])
	    config[config_name].init_app(app)
	
	    bootstrap.init_app(app)
	    moment.init_app(app)
	    db.init_app(app)
	
	    return app

create_app()函数就是程序的工厂函数，接受一个参数，是程序使用的配置名。配置类在前面的config.py文件中定义。

Flask app.config配置对象提供一个from_object()方法直接导入程序。

Flask的手册中关于Flask的config属性说明是这样的：

The configuration dictionary as Config. This behaves exactly like a regular dictionary but supports additional methods to load a config from files.

## 在蓝本中实现程序功能 ##

现在程序实例app需要在运行时由工厂函数create_app()创建，这样就不能使用app.route修饰器来定义路由了。解决方式是使用Flask提供的蓝本。蓝本与程序类似，也可以定义路由。不同的是，在蓝本中定义的路由处于休眠状态，直到蓝本注册到程序上之后，路由才真正成为程序的一部分。

蓝本在官方手册中的说明是：

Bluepint Objects. Represets a blueprint. A blueprint is an object that records functions that will be called with the Blueprint Setup State later to register functions or other things on the main application.

### 创建蓝本 ###

在app/main/__init__.py中创建蓝本：

	from flask import Blueprint    
	                               
	main = Blueprint('main', __name__)
	
	from . import views, errors    

通过实例化一个Blueprint类对象可以创建蓝本。这个构造函数必须指定的参数：蓝本名字和蓝本所在的包或模块。

程序的路由保存在包里的app/main/views.py模块中，而错误处理程序保存在app/main/errors.py模块中。导入这两个模块就能把路由和错误处理程序与蓝本关联起来。注意，这些模块在app/main/__init__.py脚本的末尾导入，是为了避免循环导入依赖，因为在views.py和errors.py中还要导入蓝本main。

### 注册蓝本 ###

蓝本在工厂函数create_app()中注册到函数上，在app/__init__.py中添加注册蓝本的代码。

	def create_app(config_name):
		# ...
	    from .main import main as main_blueprint
	    app.register_blueprint(main_blueprint)

		return app

这样在创建app之后将蓝本注册到app上了。

### 蓝本中的错误处理程序 ###

在app/main/errors.py中写入蓝本的错误处理程序。

	from . import main             
	      
	@main.app_errorhandler(404)
	def page_not_found(e):         
	    return render_template('404.html'), 404
	  
	@main.app_errorhandler(500)    
	def internal_server_error(e):
	    return render_template('500.html'), 500

app_errorhandler是blueprints模块中提供的错误处理程序，官方解释是：

Like :meth:`Flask.errorhandler` but for a blueprint.  This handler is used for all requests, even if outside of the blueprint.

如果用errorhandler，则只有蓝本中的错误才能触发。要想注册程序全局的错误处理程序，必须使用app_errorhandler。

### 程序路由 ###

在app/main/views.py中添加蓝本定义的程序路由。

	from flask import render_template 
	                               
	from . import main             
	
	@main.route                    
	def index():                   
	    return render_template('index.html')

这里采用render_template对模板进行渲染，render_template是jinja2提供的模板引擎，flask已经集成了，不需要额外安装。其第一个参数是模板的名字或者一个模板名字的可迭代对象，第二个参数是要填入模板变量的键值对。

在蓝本中编写视图函数时，路由装饰器由蓝本提供。

### 编写模板 ###

编写简单的index模板和错误处理的模板。由于各个页面中可能会有很多相同的部分，为了不重复编写代码，我们可以将共同的部分写入app/templates/base.html，然后其他的模板再从该模板进行衍生。

## 启动脚本 ##

