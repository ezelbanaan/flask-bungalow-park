from flask import render_template, url_for, flash, redirect, abort, Blueprint
from flask_login import login_required, current_user
from webapp import db
from webapp.bungalows.forms import AddBungalowForm
from webapp.models import Bungalow

bungalows = Blueprint('bungalows', __name__ , template_folder='templates')

@bungalows.route('/add_bungalow', methods=["POST", "GET"])
@login_required
def add_bungalow():
    form = AddBungalowForm()
    if current_user.is_admin:
        if form.validate_on_submit():
            bungalow = Bungalow(name=form.name.data, content=form.content.data , bungalow_type=form.bungalow_type.data, weekprice=form.weekprice.data)
            db.session.add(bungalow)
            db.session.commit()
            flash(f"Bungalow added!", 'success')
            return redirect(url_for('bungalows.zoek'))
    else:
        abort(403)
    return render_template('add_bungalow.html', form=form)

@bungalows.route('/search-book')
def zoek():
    all_bungalows = Bungalow.query.all()
    return render_template('search-book.html', title="Search & Book", all_bungalows=all_bungalows)

