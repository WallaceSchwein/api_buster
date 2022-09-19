from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from .db_interface import delete_user
from .logic_interface import create_user, fill_user_data, update_user, change_user_pwd, delete_user
from .models.user import User
from werkzeug.security import check_password_hash

auth = Blueprint("auth", __name__, template_folder="templates/auth")

@auth.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if current_user.user_id == "admin":
        if request.method == "POST":
            if request.form.get('create-user') == "clicked":
                user_mail = request.form.get('mail')
                ehyp_token = request.form.get('ehyp-token-add')
                qp_id = request.form.get('qp-id-add')
                qp_sec = request.form.get('qp-sec-add')
                con_id_qp = request.form.get('con-id-qp-add')
                bfx_id = request.form.get('bfx-id-add')
                bfx_sec = request.form.get('bfx-sec-add')
                con_id_bfx = request.form.get('con-id-bfx-add')
                region = request.form.get('region-add')

                res = create_user(user_mail, ehyp_token, qp_id, qp_sec, con_id_qp, bfx_id, bfx_sec, con_id_bfx, region)

                if isinstance(res, str):
                    return render_template("admin_dashboard.html", # NOSONAR
                                           user=current_user, 
                                           new_id=res, 
                                           create_user="creating", 
                                           show_modal=True)
                if isinstance(res, int):
                    if res == 1:
                        flash(f"Bitte geben Sie eine gültige Mail-Adresse ein..", category="error")
                    else:
                        flash(f"Fehler! Nutzer konnte nicht angelegt werden..", category="error")
            elif request.form.get('edit-user') == "clicked":
                try:
                    user_id_set = request.form.get('user-id')

                    user = fill_user_data(user_id_set)

                    return render_template("admin_dashboard.html",
                                           user=current_user,
                                           user_id_set=user_id_set,
                                           ehyp_token_set=user.ehyp_token,
                                           qp_id_set=user.qp_id,
                                           qp_sec_set=user.qp_sec,
                                           con_id_qp_set=user.con_id_qp,
                                           bfx_id_set=user.bfx_id,
                                           bfx_sec_set=user.bfx_sec,
                                           con_id_bfx_set=user.con_id_bfx,
                                           region_set=user.region,
                                           edit_user='editing')
                except Exception:
                    flash(f"Fehler! Bitte geben Sie eine gültige User-ID ein..", category="error")
            elif request.form.get('reset-form') == "clicked":
                return render_template("admin_dashboard.html", user=current_user, edit_user='editing')
            else:
                user_id = request.form.get('user-id')
                ehyp_token = request.form.get('ehyp-token-up')
                qp_id = request.form.get('qp-id-up')
                qp_sec = request.form.get('qp-sec-up')
                con_id_qp = request.form.get('con-id-qp-up')
                bfx_id = request.form.get('bfx-id-up')
                bfx_sec = request.form.get('bfx-sec-up')
                con_id_bfx = request.form.get('con-id-bfx-up')
                region = request.form.get('region-up')

                if request.form.get('update-user') == "clicked":
                    res = update_user(user_id, ehyp_token, qp_id, qp_sec, con_id_qp, bfx_id, bfx_sec, con_id_bfx, region)
                    if res:
                        flash(f"Nutzerdaten erfolgreich geändert..", category="success")
                    else:
                        flash(f"Fehler! Nutzerdaten konnten nicht geändert werden..", category="error")
                elif request.form.get('delete-user') == "clicked":
                    res = delete_user(user_id)
                    if res:
                        flash(f"Nutzer wurde gelöscht..", category="success")
                    else:
                        flash(f"Fehler! Nutzer konnte nicht gelöscht werden..", category="error")
        return render_template("admin_dashboard.html", user=current_user)
    else:
        flash(f"Dieser Bereich kann nur vom Admin betreten werden..", category="error")
        return redirect(url_for('view.main'))

@auth.route("/changepwd", methods=["GET", "POST"])
@login_required
def change_pwd():
    if request.method == "POST":
        old_pwd = request.form.get('old-pwd')
        new_pwd = request.form.get('new-pwd')
        pwd_confirm = request.form.get('pwd-confirm')

        if check_password_hash(current_user.pwd, old_pwd):
            res = change_user_pwd(current_user.user_id, new_pwd, pwd_confirm)
            match res:
                case 0:
                    flash(f"Das Passwort wurde erfolgreich geändert..", category="success")
                case 1:
                    flash(f"Das neue Passwort muss zweimal das selbe sein..", category="error")
                case 2:
                    flash(f"Das neue Passwort muss zwischen 8 und 20 Zeichen lang sein..", category="error")
                case 3:
                    flash(f"Das neue Passwort muss mindestens einen Großbuchstaben, sowie eine Zahl oder ein Sonderzeichen enthalten..", category="error")
                case -1:
                    flash(f"Das Passwort konnte nicht gändert werden..", category="error")
        else:
            flash(f"Das eingegebene Passwort stimmt nicht mit dem aktuellen überein..", category="error")
        

    return render_template("change_pwd.html", user=current_user)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("view.main"))

    if request.method == "POST":
        uid = request.form.get('uid')
        pwd = request.form.get('pwd')

        if uid != "" and (len(uid) == 5 or uid == "admin"):
            user = User.query.filter_by(user_id=uid).first()
            if user and check_password_hash(user.pwd, pwd):
                login_user(user, remember=True)
                if uid == "admin":
                    return redirect(url_for("auth.admin"))
                else:
                    return redirect(url_for("view.main"))
            else:
                flash(f"User-ID oder Passwort ungültig! Bitte überprüfen Sie Ihre Eingabe..", category="error")
        elif uid != "" and len(uid) != 10:
            flash(f"{uid} ist keine gültige User-ID!\nBitte überprüfen Sie Ihre Eingabe..", category="error")

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for("auth.login"))