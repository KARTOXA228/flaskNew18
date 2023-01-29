import math
import sqlite3
import time

#from flask_app import connect_db, app


def create_db():
    '''создание таблици базы данных'''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addMenu(self, title, url):
        try:
            self.__cur.execute('INSERT INTO mainmenu VALUES (NULL, ?, ?)', (title,url))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добовления в БД', str(e))
            return False
        return True

    def delMenu(self, id=0):
        try:
            if id == 0:
                self.__cur.execute(f"DELETE FROM mainmenu")
            else:
                self.__cur.execute(f"DELETE FROM mainmenu WHERE id={id}")
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка удаления из БД', str(e))
            return False
        return True
    def getMenu(self):
        try:
            sql = """SELECT * FROM mainmenu"""
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('Ошибка чтения из БД')
            return []
    def addPost(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES (NULL, ?, ?, ?)", (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления поста в БД", str(e))
            return False
        return True

    def getPostAnnoce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД" + str(e))
        return []

    def getPost(self, postid):
        try:
            self.__cur.execute(f"SELECT  title, text FROM posts WHERE id = {postid} LIMIT 1")
            res = self.__cur.fetchone()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД" + str(e))
        return (False, False)


if __name__ == '__main__':
    from flask_app import connect_db, app
    print(create_db.__doc__)
    db = connect_db()
    db = FDataBase(db)
    #print(db.addMenu('Домой', 'index'))
    #print(db.addMenu('Авторизация1', 'index'))
    #print(db.addMenu('Авторизация2', 'index'))


    #print(db.delMenu(0))

    print(db.delMenu(11))
