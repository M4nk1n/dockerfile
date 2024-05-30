#!/bin/sh

# 修复目录权限
# mediaowner=$(ls -ld /data | awk '{print $3}')
# echo "Current /data owner is $mediaowner"
# if [ "$mediaowner" != "nginx" ]
# then
#     chown -R nginx:nginx /data
# fi

# 优先判断是否是多用户模式
if [ -e /etc/nginx/htpasswd ]; then exit 0; fi

# 再判断是否是单用户模式
if [ -n "$USERNAME" ] && [ -n "$PASSWORD" ]
then
  htpasswd -bc /etc/nginx/htpasswd $USERNAME $PASSWORD
  echo "成功添加单用户！"
  exit 0
fi

# 还不是就是无用户模式了
echo Using no auth.
sed -i 's%auth_basic "Restricted";% %g' /etc/nginx/http.d/default.conf
sed -i 's%auth_basic_user_file /etc/nginx/htpasswd;% %g' /etc/nginx/http.d/default.conf

# 两种用户模式都没有设置，则报错提示
# echo "错误！检查是否正确配置用户！"
# exit 1
