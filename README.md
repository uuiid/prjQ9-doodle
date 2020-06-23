# prjQ9-doodle
pip freeze > requirements.txt
pip install -r requirements.txt

pyinstaller doodle.spec
console=True

filepath 属性代表所有路径包括文件名称
path 是文件的路径,不包括名称
filename 是文件名称
get 开头是获得
set 开头是设置
query 开头是查询
is 开头是判断
conver 开头是转换