# import sqlalchemy
#
# from source.database.session import SqlAlchemyBase
#
#
# class AlertGraph(SqlAlchemyBase):
#     __table_args__ = {'extend_existing': True}
#     __tablename__ = 'temperature_graph'
#
#     city = sqlalchemy.Column(
#         sqlalchemy.TEXT,
#         nullable=False,
#         unique=True,
#         primary_key=True
#     )
#     am12 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     am1 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     am2 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     am3 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     am4 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     am5 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     am6 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     am7 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     am8 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     am9 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     am10 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     am11 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     pm12 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     pm1 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     pm2 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     pm3 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     pm4 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     pm5 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     pm6 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     pm7 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     pm8 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     pm9 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     pm10 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#     pm11 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
#
#
# def __repr__(self):
#     return '<User %r>' % self.username
