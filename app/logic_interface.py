from click import UsageError
import regex
import json
import copy

from werkzeug.security import generate_password_hash, check_password_hash

from app.api_interface import get_token, get_customer, post_customer, map_to_ehyp, map_to_euro
from app.models.user import User
from .db_interface import *

def change_user_pwd(user_id: str, new_pwd: str, pwd_confirm: str):
        PATTERN_SPECIALS = regex.compile('[–+-/\\(){}[\]<>§$%&=\*°#@€¿&_ʼ‘’"„“”᾽‧¸‚,;…\'~‐‑‒]')
        PATTERN_CAPS = regex.compile('[A-ZÄÖÜ]')
        PATTERN_NUMBERS = regex.compile('[0-9]')

        check_specials = regex.search(PATTERN_SPECIALS, new_pwd)
        check_caps = regex.search(PATTERN_CAPS, new_pwd)
        check_numbers = regex.search(PATTERN_NUMBERS, new_pwd)

        if new_pwd != pwd_confirm:
            return 1
        elif len(new_pwd) < 8 or len(new_pwd) > 20:
            return 2
        elif not check_caps and not (check_specials or check_numbers):
            return 3
        else:
            res_pwd = update_pwd(user_id, new_pwd)
            if res_pwd:
                return 0
            else:
                return -1

def create_user(user_mail: str,
                ehyp_token: str,
                qp_id: str,
                qp_sec: str,
                con_id_qp: str,
                bfx_id: str,
                bfx_sec: str,
                con_id_bfx: str,
                region: str):
    PATERN_MAIL = regex.compile('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

    if regex.fullmatch(PATERN_MAIL, user_mail):
        user_id = generate_password_hash(user_mail, method="sha256").split("$")[-1][-5:]
        new_user = User(user_id=user_id,
                        ehyp_token=ehyp_token,
                        qp_id=qp_id,
                        qp_sec=qp_sec,
                        con_id_qp=con_id_qp,
                        bfx_id=bfx_id,
                        bfx_sec=bfx_sec,
                        con_id_bfx=con_id_bfx,
                        region=region)
        res = add_user(new_user)
        if res:
            return user_id
        else:
            return 1
    else:
        return -1

def fill_user_data(user_id: str):
    return get_user(user_id)

def update_user(user_id: str,
                ehyp_token: str,
                qp_id: str,
                qp_sec: str,
                con_id_qp: str,
                bfx_id: str, 
                bfx_sec: str,
                con_id_bfx: str,
                region: str):
    user = get_user(user_id)

    if ehyp_token != user.ehyp_token:
        res_ehyp_token = update_ehyp_token(user_id, ehyp_token)
    else:
        res_ehyp_token = True
    if qp_id != user.qp_id:
        res_qp_id = update_client_ID_qp(user_id, qp_id)
    else:
        res_qp_id = True
    if qp_sec != user.qp_sec:
        res_qp_sec = update_client_sec_qp(user_id, qp_sec)
    else:
        res_qp_sec = True
    if con_id_qp != user.con_id_qp:
        res_con_id_qp = update_cons_ID_qp(user_id, con_id_qp)
    else:
        res_con_id_qp = True
    if bfx_id != user.bfx_id:
        res_bfx_id = update_client_ID_bfx(user_id, bfx_id)
    else:
        res_bfx_id = True
    if bfx_sec != user.bfx_sec:
        res_bfx_sec = update_client_sec_bfx(user_id, bfx_sec)
    else:
        res_bfx_sec = True
    if con_id_bfx != user.con_id_bfx:
        res_con_id_bfx = update_cons_ID_bfx(user_id, con_id_bfx)
    else:
        res_con_id_bfx = True
    if region != user.region:
        res_region = update_region(user_id, region)
    else:
        res_region = True

    if res_ehyp_token and res_qp_id and res_qp_sec and res_con_id_qp and res_bfx_id and res_bfx_sec and res_con_id_bfx and res_region:
        return True
    else: 
        return False

def remove_user(user_id: str):
    return delete_user(user_id)

def from_ehyp(user_id: str, ops_no: str, token_ehyp: str, token_qp: str, token_bfx: str, provider: str, qp_to: str, bfx_to: str) :
    try:
        data_received = get_customer(ops_no, token_ehyp, provider)
    except Exception:
        return 1

    data_dict_euro = json.load(open("./app/models/europace.json"))

    if qp_to == "clicked":
        data_dict_euro_qp = copy.deepcopy(data_dict_euro)
        con_id_qp = get_qp_con_id(user_id)
        data_dict_euro_qp['importMetadaten']['betreuung']['kundenbetreuer'] = con_id_qp
        data_dict_euro_qp['importMetadaten']['betreuung']['bearbeiter'] = con_id_qp
        data_to_send_qp = map_to_euro(data_received, data_dict_euro_qp)
        res_qp = post_customer(data_to_send_qp, token_qp, provider)
    else:
        res_qp = None
    if bfx_to == "clicked":
        data_dict_euro_bfx = copy.deepcopy(data_dict_euro)
        con_id_bfx = get_bfx_con_id(user_id)
        data_dict_euro_bfx['importMetadaten']['betreuung']['kundenbetreuer'] = con_id_bfx
        data_dict_euro_bfx['importMetadaten']['betreuung']['bearbeiter'] = con_id_bfx
        data_to_send_bfx = map_to_euro(data_received, data_dict_euro_bfx)
        res_bfx = post_customer(data_to_send_bfx, token_bfx, provider)
    else:
        res_bfx = None

    if (res_qp is not None and res_qp.status_code != 201) and (res_bfx is not None and res_bfx.status_code != 201):
        print(f"[REQUEST ERROR]: {res_qp.status_code} @QP AND {res_bfx.status_code} @BFX")
        return 2
    elif res_qp is not None and res_qp.status_code != 201:
        print(f"[REQUEST ERROR]: {res_qp.status_code} @QP")
        return 3
    elif res_bfx is not None and res_bfx != 201:
        print(f"[REQUEST ERROR]: {res_bfx.status_code} @BFX")
        return 4
    else:
        print(f"[SUCCES]: 201 @All requests!")
        return 0

def from_qp(user_id: str, ops_no: str, token_ehyp: str, token_qp: str, token_bfx: str, provider: str, ehyp_to: str, bfx_to: str):
    try:
        data_received = get_customer(ops_no, token_qp, provider)
    except Exception:
        return 1

    data_dict_ehyp = json.load(open("./app/models/ehyp.json")) if ehyp_to else None

    if ehyp_to == "clicked":
        data_to_send = map_to_ehyp(data_received, data_dict_ehyp)
        res_ehyp = post_customer(data_to_send, token_ehyp, provider)
    else: 
        res_ehyp = None
    if bfx_to == "clicked":
        con_id_bfx = get_bfx_con_id(user_id)
        data_received['importMetadaten']['betreuung']['kundenbetreuer'] = con_id_bfx
        data_received['importMetadaten']['betreuung']['bearbeiter'] = con_id_bfx
        res_bfx = post_customer(data_received, token_bfx, provider)
    else:
        res_bfx = None

    if (res_ehyp is not None and res_ehyp.status_code != 201) and (res_bfx is not None and res_bfx.status_code != 201):
        print(f"[REQUEST ERROR]: {res_ehyp.status_code} @eHyp AND {res_bfx.status_code} @BFX")
        return 2
    elif res_ehyp is not None and res_ehyp.status_code != 201:
        print(f"[REQUEST ERROR]: {res_ehyp.status_code} @eHyp")
        return 5
    elif res_bfx is not None and res_bfx != 201:
        print(f"[REQUEST ERROR]: {res_bfx.status_code} @BFX")
        return 4
    else:
        print(f"[SUCCES]: 201 @All requests!")
        return 0

def from_bfx(user_id: str, ops_no: str, token_ehyp: str, token_qp: str, token_bfx: str, provider: str, ehyp_to: str, qp_to: str):
    try:
        data_received = get_customer(ops_no, token_bfx, provider)
    except Exception:
        return 1

    data_dict_ehyp = json.load(open("./app/models/ehyp.json")) if ehyp_to else None

    if ehyp_to == "clicked":
        data_to_send = map_to_ehyp(data_received, data_dict_ehyp)
        res_ehyp = post_customer(data_to_send, token_ehyp, provider)
    else:
        res_ehyp = None
    if qp_to == "clicked":
        con_id_qp = get_qp_con_id(user_id)
        data_received['importMetadaten']['betreuung']['kundenbetreuer'] = con_id_qp
        data_received['importMetadaten']['betreuung']['bearbeiter'] = con_id_qp
        res_qp = post_customer(data_received, token_qp, provider)
    else:
        res_qp = None

    if (res_ehyp is not None and res_ehyp.status_code != 201) and (res_qp is not None and res_qp.status_code != 201):
        print(f"[REQUEST ERROR]: {res_ehyp.status_code} @eHyp AND {res_qp.status_code} @QP")
        return 2
    elif res_ehyp is not None and res_ehyp.status_code != 201:
        print(f"[REQUEST ERROR]: {res_ehyp.status_code} @eHyp")
        return 5
    elif res_qp is not None and res_qp != 201:
        print(f"[REQUEST ERROR]: {res_qp.status_code} @QP")
        return 3
    else:
        print(f"[SUCCES]: 201 @All requests!")
        return 0 # TODO change prints to return value

def service(user_id: str, ops_no: str, provider: str, ehyp_to: str, qp_to: str, bfx_to: str):
    if qp_to or provider == "qp":
        qp_id = get_qp_id(user_id)
        qp_secret = get_qp_secret(user_id)
        token_qp = get_token(qp_id, qp_secret) if provider == "qp" or qp_to else None
    else:
        token_qp = None

    if bfx_to or provider == "bfx":
        bfx_id = get_bfx_id(user_id)
        bfx_secret = get_bfx_secret(user_id)
        token_bfx = get_token(bfx_id, bfx_secret) if provider == "bfx" or bfx_to else None
    else:
        token_bfx = None

    token_ehyp = get_ehyp_token(user_id)

    if provider == "ehyp":
        return from_ehyp(user_id, ops_no, token_ehyp, token_qp, token_bfx, provider, qp_to, bfx_to)
    elif provider == "qp":
        return from_qp(user_id, ops_no, token_ehyp, token_qp, token_bfx, provider, ehyp_to, bfx_to)
    else:
        return from_bfx(user_id, ops_no, token_ehyp, token_qp, token_bfx, provider, ehyp_to, qp_to)
