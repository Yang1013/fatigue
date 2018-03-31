import os

os.remove("chatdata.txt")
text = ""
with open("detect.txt", 'r') as f:
   text = f.read()

print(text)

with open("chatdata.txt", 'w') as f:
   if text[15] != "\"" and text[15] != ",":
      f.write("您眨眼次數為：" + text[14:16] + "次\n")
      if text[30] == 'y':
         f.write("您曾姿勢不佳\n")
      else:
         f.write("您姿勢良好\n")
      if text[46] == 'y':
         f.write("曾有陌生人拜訪\n")
      else:
         f.write("未有不明人士拜訪\n")
      if text[64] == 'y':
         f.write("您曾闔上雙眼一段時間\n")
      else:
         f.write("您不曾闔上雙眼過久\n")
      if text[77] == 'y':
         f.write("您曾打了哈欠\n")
      else:
         f.write("您不曾打哈欠\n")
   else:
      f.write("您眨眼次數為：" + text[14] + "次\n")
      if text[29] == 'y':
         f.write("您曾姿勢不佳\n")
      else:
         f.write("您姿勢良好\n")
      if text[45] == 'y':
         f.write("曾有陌生人拜訪\n")
      else:
         f.write("未有不明人士拜訪\n")
      if text[63] == 'y':
         f.write("您曾闔上雙眼一段時間\n")
      else:
         f.write("您不曾闔上雙眼過久\n")
      if text[76] == 'y':
         f.write("您曾打了哈欠\n")
      else:
         f.write("您不曾打哈欠\n")

