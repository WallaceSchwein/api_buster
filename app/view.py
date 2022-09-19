from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

from .logic_interface import service

view = Blueprint("view", __name__, template_folder="templates/view")

@view.route("/", methods=["GET", "POST"])
@view.route("/main", methods=["GET", "POST"])
@login_required
def main():
    if request.method == "POST":
        ops_no = request.form.get('ops-no')
        provider = request.form.get('init-check')
        ehyp = request.form.get('ehyp-to')
        qp = request.form.get('qp-to')
        bfx = request.form.get('bfx-to')

        if ops_no is None:
            flash(f"Bitte geben Sie eine gültige Vorgangsnummer an..", category="error")
        elif provider is None:
            flash(f"Bitte wählen Sie, von welchem Anbieter Sie die Kundendaten laden möchten..", category="error")
        elif ehyp is None and qp is None and bfx is None:
            flash(f"Bitte wählen Sie, an welchem Anbieter Sie die Kundendaten übermitteln möchten..", category="error")
        else:
            match service(current_user.user_id, ops_no, provider, ehyp, qp, bfx):
                case 0:
                    flash(f"Kundendaten konnten erfolgreich übermittelt werden!", category="succes")
                case 1:
                    flash(f"[PLATZHALTER FÜR FEHLER 1]", category="error")
                case 2:
                    flash(f"[PLATZHALTER FÜR FEHLER 2]", category="error")
                case 3:
                    flash(f"[PLATZHALTER FÜR FEHLER 3]", category="error")
                case 4:
                    flash(f"[PLATZHALTER FÜR FEHLER 4]", category="error")
                case 5:
                    flash(f"[PLATZHALTER FÜR FEHLER 5]", category="error")

    return render_template("api_dashboard.html", user=current_user)