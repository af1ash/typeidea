# typeidea

个人博客应用

## 环境变量配置项

|类型|参数名|默认值|描述|
|---|-----|-----|----|
|密钥|SECRET_KEY|||
|debug模式|DEBUG|false|是否开启debug模式，生产环境建议禁止开启|
|支持静态文件接口|WITH_STATIC|false|不使用nginx代理静态文件，需要设置为true|
|允许的主机|ALLOWED_HOSTS|*||
|默认超级管理员用户名|DJANGO_SUPERUSER_USERNAME|admin||
|默认超级管理员密码|DJANGO_SUPERUSER_PASSWORD|adminadmin||
|默认超级管理员邮箱|DJANGO_SUPERUSER_EMAIL|admin@example.com||
|默认数据库类型|DEFAULT_DB_TYPE|sqlit3|未配置默认使用sqlite3|
|mysql数据库名称|MYSQL_NAME|||
|mysql用户名|MYSQL_USER|||
|mysql密码|MYSQL_PASSWORD|||
|mysql主机|MYSQL_HOST|||
|mysql端口|MYSQL_PORT|||
