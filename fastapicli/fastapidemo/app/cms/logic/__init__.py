from cms.core.db import pgdb


from cms.logic.common.user import UserRole, User, init_super_user


pgdb.create_tables([UserRole, User])
init_super_user()
pgdb.close()
