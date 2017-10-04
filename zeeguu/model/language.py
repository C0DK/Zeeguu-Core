import zeeguu

db = zeeguu.db


class Language(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}
    __tablename__ = 'language'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5))
    name = db.Column(db.String(255), unique=True)

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return '<Language %r>' % (self.code)

    def __eq__(self, other):
        return self.code == other.code or self.name == other.name

    @classmethod
    def default_learned(cls):
        return cls.find("de")

    @classmethod
    def default_native_language(cls):
        return cls.find("en")

    @classmethod
    def native_languages(cls):
        return [cls.find("en"), cls.find("nl"), cls.find('zh-CN')]

    @classmethod
    def available_languages(cls):
        # return list(set(cls.all()) - set([Language.find("en")]))
        return [Language.find('de'), Language.find('es'), Language.find('fr'), Language.find('nl')]

    @classmethod
    def find(cls, code):
        return cls.query.filter(Language.code == code).one()

    @classmethod
    def all(cls):
        return cls.query.filter().all()
