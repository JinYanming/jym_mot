import os
def clear_subfile(targetUrl)
  for file in os.listdir(targetUrl):
     path_file = os.path.join(targetUrl,file)  // 取文件绝对路径
     if os.path.isfile(path_file):
       os.remove(path_file)
     else:
         clear_subfile(path_file)
