import yadisk

y = yadisk.YaDisk(token="y0_AgAAAAA6Qd7JAAoMJgAAAADlfHsiBIK6yTKwQduJv4vG9Sg4ZH8z2ug")
#y.mkdir('/test')
# или
# y = yadisk.YaDisk("<id-приложения>", "<secret-приложения>", "<токен>")
y.upload('images/check.png', '/test/check.png')

# Проверяет, валиден ли токен
files = list(y.listdir('/test')) 
for p in files:
    print(p["name"]) 

