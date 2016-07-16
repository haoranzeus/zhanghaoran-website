# 个人网站设计笔记4 #

## 服务器与域名 ##

最近在网上申请了一个域名，原本是想申请zhanghaoran.com的，结果一查，zhanghaoran.com，zhanghaoran.cn，zhanghaoran.net统统已经被申请了，而且挂在网上卖，额，谁让我这名字这么大众呢。反正就一域名嘛，都是DNS解析，怎么着都是一样用，于是我就申请了一个小众的域名：

[www.zhanghaoran.cc](www.zhanghaoran.cc)

当然，现在还打不开，因为还在审核过程中。

服务器本来是想买阿里云的，结果总是点不出选配置的界面（阿里看了也有做的不足的地方），然后我就转投腾讯的怀抱了，在腾讯云选了个最低配：

- 1核CPU
- 1G内存
- 1M带宽
- 10G数据盘

算下来一个月68元，恩，还可以接受。操作系统选的Centos，版本但求最新不求最好，选的7.2。

之后就是漫长的备案之旅了，上传了一大堆资料，腾讯还给寄来了拍照的幕布，拍好照上传。之后的备案提交都是腾讯负责，我这，就只有等了。

## MySQL之旅 ##

眼瞅着我这网站就可以试着上线了，数据库总不能还用sqlite吧，尝试着玩玩MySQL吧。哦，MySQL被Oracle收购后，红帽系就采用与MySQL同源的MariaDB了。

### 安装 ###

yum install mysql
yum install mysql-devel
yum install mariadb-server

### 运行mariadb服务器 ###

systemctl start mariadb.service

### 创建root用户 ###

mysql -u root -p

然后输入密码即可

### 普通用户设置 ###

要添加MySQL用户，可以通过向mysql数据库的user表中添加行。

	$ mysql -u -p
	Enter password:
	mysql> use mysql;
	Database changed

	mysql> Insert INTO user
			(host, user, password,
			 select_priv, insert_priv, uupdate_priv)
			 VALUES ('localhost', 'gest',
			 PASSWORD('guest123'), 'Y', 'Y', 'Y');
	Query OK, 1 row affected (0.20 sec)

	mysql> FLUSH PRIVILEGES;
	Query OK, 1 row affected (0.20 sec)

这里使用MySQL提供的PASSWORD()函数对密码进行加密。

执行FLUSH PRIVILEGES语句重新载入授权表。