from peewee import Model, SqliteDatabase, CharField, TextField

db = SqliteDatabase("translations.db")


class TranslationModel(Model):
    text = TextField()
    base_language = CharField()
    final_language = CharField()
    translation = TextField(null=True)

    class Meta:
        database = db
