from pymysql import connect
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


class DB(object):
    def __init__(self):
        self.conn = connect(host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            charset='utf8')
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_one(self, sql):
        self.cursor.execute(sql)

        query_result = self.cursor.fetchone()
        if not query_result:
            return None

        fields = [field[0] for field in self.cursor.description]

        return_data = dict()
        for field, value in zip(fields, query_result):
            return_data[field] = value

        return return_data

    def get_all(self, sql='select * from users'):
        self.cursor.execute(sql)

        query_result = self.cursor.fetchall()
        if not query_result:
            return None

        fields = [field[0] for field in self.cursor.description]

        return_data = []
        for row in query_result:
            row_data = dict()
            for field, value in zip(fields, row):
                row_data[field] = value
            return_data.append(row_data)

        return return_data

    def insert(self, user_name, password, nick_name):
        # 先查询是否存在相同的用户名
        sql = 'select * from users where user_name="{}"'.format(user_name)
        if self.get_one(sql):
            print('The user name already exists')
            return False

        sql = 'insert into users values(0, "{}", "{}", "{}")'.format(user_name, password, nick_name)

        self.cursor.execute(sql)
        self.conn.commit()

        return True

    def update(self, user_name, password, nick_name):
        # 先查询是否存在相同的用户名
        sql = 'select * from users where user_name="{}"'.format(user_name)
        if not self.get_one(sql):
            print('The user name does not exist')
            return False

        sql = 'update users set user_password="{}", user_nickname="{}" where user_name="{}"'.format(password, nick_name, user_name)

        self.cursor.execute(sql)
        self.conn.commit()

        return True

    def delete(self, user_name):
        # 先查询是否存在相同的用户名
        sql = 'select * from users where user_name="{}"'.format(user_name)
        if not self.get_one(sql):
            print('The user name does not exist')
            return False

        sql = 'delete from users where user_name="{}"'.format(user_name)

        self.cursor.execute(sql)
        self.conn.commit()

        return True


if __name__ == '__main__':
    db = DB()
    print(db.get_one('select * from users where user_name="user1"'))
    print(db.get_all())

    db.delete('user2')
    print(db.get_all())

    db.insert('user2', '123456', 'user2')
    print(db.get_all())

    db.update('user2', '654321', 'user2')
    print(db.get_all())

    db.close()
