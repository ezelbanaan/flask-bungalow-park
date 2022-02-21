from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_required, current_user
from webapp import db
from webapp.bookings.forms import BookForm, UpdateBookingForm
from webapp.models import Booking, Bungalow

bookings = Blueprint('bookings', __name__ , template_folder='templates')

@bookings.route('/booking/<int:booking_id>/delete', methods=["POST", "GET"])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.guest_id != current_user.id:
        abort(403)
    db.session.delete(booking)
    db.session.commit()
    flash(f"Your booking has been cancelled!", 'success')
    return redirect(url_for('main.account'))

@bookings.route('/booking/<int:booking_id>/update', methods=["POST", "GET"])
@login_required
def update_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.guest_id != current_user.id:
        abort(403)
    booked_weeks = [x for x, in db.session.query(Booking.week).filter_by(bungalow_id=booking.bungalow_id).all()]
    weekchoices = []
    for x in range(1, 53):
        if str(x) in booked_weeks:
            weekchoices.append((x, f"Week {x} - Gereserveerd"))
        else:
            weekchoices.append((x, f"Week {x}"))
            
    form = UpdateBookingForm()
    form.week.choices = weekchoices
    if form.validate_on_submit():
        if Booking.query.filter_by(bungalow_id=booking.bungalow_id).filter_by(week=form.week.data).first() is None:
            booking.week = form.week.data
            db.session.commit()
            flash(f"Your booking has been adjusted!", 'success')
            return redirect(url_for('main.account'))
        else:
            flash(f"The bungalow is already reserved on your desired week!", 'danger')
            return redirect(url_for('bookings.update_booking', booking_id=booking_id))
    elif request.method == 'GET':
        form.week.default = booking.week
        form.process()
    return render_template('update_booking.html', form=form, booking=booking, css="bungalow.css")

@bookings.route('/bungalow/<int:id>', methods=["POST", "GET"])
@login_required
def book(id):
    booked_weeks = [x for x, in db.session.query(Booking.week).filter_by(bungalow_id=id).all()]
    weekchoices = []
    for x in range(1, 53):
        if str(x) in booked_weeks:
            weekchoices.append((x, f"Week {x} - Reserved"))
        else:
            weekchoices.append((x, f"Week {x}"))
    form = BookForm()
    form.week.choices = weekchoices
    bungalow = Bungalow.query.get(id)

    if form.validate_on_submit():
        if Booking.query.filter_by(bungalow_id=id).filter_by(week=form.week.data).first() is None:
            booking = Booking(guest_id=current_user.id, bungalow_id=id , week=form.week.data)
            db.session.add(booking)
            db.session.commit()
            flash(f"Bungalow reserved!", 'success')
            return redirect(url_for('main.account'))
        else:
            flash(f"The bungalow is already reserved on your desired week!", 'danger')
            return redirect(url_for('bookings.book', id=id))

    return render_template('book_bungalow.html', bungalow=bungalow, form=form, css='bungalow.css')
