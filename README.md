# renren

a scrapy spider to login  zimuzu . to get movie

本项目是一个人人影视字幕组的影视资源爬虫。
使用python 的scrapy框架编写
项目思路首先登录获得session，然后访问今日更新获取
更新资源的ID，随后通过非登录状态就可以获取影视内容页

##优点
只有前期获取下载链接的地方需要登录，影视内容页并不需要，因此，
本项目在影视内容页提取时在非登录状态下获取并解析出结果，
结果以html形式存储，方便直接打开下载所需资源，

##使用方法：
git clone https://github.com/tengbozhang/renren.git
cd renren/
编辑settings.py文件，
填写settings.py中的人人影视用户名(RENREN_USERNAME)和密码(RENREN_PASSWORD)
运行run.bat脚本。
windows直接双击,unix的话也是运行文件就行

##结果展示
本爬虫以html格式展示获取到的信息，浏览器打开点击喜欢的影视下载就行

