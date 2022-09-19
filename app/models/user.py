from .. import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user" # unique constraint(?)

    user_id = db.Column(db.String(150), primary_key=True)
    pwd = db.Column(db.String(150), nullable=False, server_default="sha256$gKnA838LCi7xyTeZ$2d5343147a94b9b93de91c54a15f2f68df2e15457b69c06c08830f0c5263b2c7") #pwd: "change.quickly"

    ehyp_token = db.Column(db.String(150), nullable=False)

    qp_id = db.Column(db.String(150), nullable=False)
    qp_sec = db.Column(db.String(150), nullable=False)
    con_id_qp = db.Column(db.String(150), nullable=False)

    bfx_id = db.Column(db.String(150), nullable=False)
    bfx_sec = db.Column(db.String(150), nullable=False)
    con_id_bfx = db.Column(db.String(150), nullable=False)
    
    region = db.Column(db.String(150), nullable=False)

    def get_id(self):
        return (self.user_id)
