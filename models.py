from peewee import *
from os import path
from datetime import datetime
ROOT = path.dirname(path.realpath(__file__))
db = SqliteDatabase(path.join(ROOT, "Todo2.db"))


class User(Model):
    names = CharField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db
        db_table="users"


class Job(Model):
    owner = ForeignKeyField(User, related_name="users")
    task = CharField()
    status = CharField(default="Incomplete")

    class Meta:
        database = db
        db_table="jobs"


User.create_table(fail_silently=True)
Job.create_table(fail_silently=True)


# User.create(names="John Mark", email="johnmark@gmail.com", password="123456")
# User.create(names="Mark Kigwa", email="kigwa@gmail.com", password="123456")
# Job.create (owner=1, task="write report")
# Job.create (owner=1, task="Do dishes")
# Job.create (owner=2, task="Go out")
# Job.create (owner=2, task="File taxes")

#Job.create (owner=5, task="File returns")