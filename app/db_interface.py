from . import db
from .models.user import User
from werkzeug.security import generate_password_hash

def add_user(user: User):
    try:
        db.session.add(user)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

def get_user(user_id: str):
    return User.query.filter_by(user_id=user_id).first()

def get_ehyp_token(user_id: str):
    return User.query.filter_by(user_id=user_id).first().ehyp_token

def get_qp_id(user_id:str):
    return User.query.filter_by(user_id=user_id).first().qp_id

def get_qp_secret(user_id:str):
    return User.query.filter_by(user_id=user_id).first().qp_sec

def get_bfx_id(user_id:str):
    return User.query.filter_by(user_id=user_id).first().bfx_id

def get_bfx_secret(user_id:str):
    return User.query.filter_by(user_id=user_id).first().bfx_sec

def get_qp_con_id(user_id:str):
    return User.query.filter_by(user_id=user_id).first().con_id_qp

def get_bfx_con_id(user_id:str):
    return User.query.filter_by(user_id=user_id).first().con_id_bfx

def update_pwd(user_id: str, new_pwd: str):
    try:
        update_pwd = User.query.filter_by(user_id=user_id).update(dict(pwd=generate_password_hash(new_pwd, method="sha256")))
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

def update_ehyp_token(user_id: str, new_ehyp_token: str):
    try:
        update_ehyp_token = User.query.filter_by(user_id=user_id).update(dict(ehyp_token=new_ehyp_token))
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

def update_client_ID_qp(user_id: str, new_client_ID_qp: str):
    try:
        update_client_ID_qp = User.query.filter_by(user_id=user_id).update(dict(client_ID_qp=new_client_ID_qp))
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

def update_client_sec_qp(user_id: str, new_client_sec_qp: str):
    try:
        update_client_sec_qp = User.query.filter_by(user_id=user_id).update(dict(client_sec_qp=new_client_sec_qp))
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

def update_cons_ID_qp(user_id: str, new_cons_ID_qp: str):
    try:
        update_cons_ID_qp = User.query.filter_by(user_id=user_id).update(dict(cons_ID_qp=new_cons_ID_qp))
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

def update_client_ID_bfx(user_id: str, new_client_ID_bfx: str):
    try:
        update_client_ID_bfxd = User.query.filter_by(user_id=user_id).update(dict(client_ID_bfxd=new_client_ID_bfx))
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

def update_client_sec_bfx(user_id: str, new_client_sec_bfx: str):
    try:
        update_client_sec_bfx = User.query.filter_by(user_id=user_id).update(dict(client_sec_bfx=new_client_sec_bfx))
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

def update_cons_ID_bfx(user_id: str, new_cons_ID_bfx: str):
    try:
        update_cons_ID_bfx = User.query.filter_by(user_id=user_id).update(dict(cons_ID_bfx=new_cons_ID_bfx))
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

def update_region(user_id: str, new_region: str):
    try:
        update_region = User.query.filter_by(user_id=user_id).update(dict(region=new_region))
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

def delete_user(user_id: str):
    try:
        del_user = User.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False
