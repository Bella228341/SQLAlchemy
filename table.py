from app import db


class Role(db.Model):
    id = db.Column(db.Integer, primaty_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)


user_role = Role(name='user')
admin_role = Role(name='admin')

db.session.add(user_role)
db.session.add(admin_role)
db.session.commit()

roles = Role.query.all()
for role in roles:
    print(role.name)
