from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for, session, current_app
    )

import sys
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('user', __name__, url_prefix="/user") 


@bp.route('/my')
@login_required
def my():
    db = get_db()
    user_data = db.execute(
            'SELECT availabe_coins, balance, daily_income, total_income FROM user_data WHERE id = ?;'
            ,(session['user_id'], )).fetchall()
    if not user_data:
        user_data = [0] * 4
    return render_template('blog/my.html', user_data=user_data)


@bp.route('/withdraw', methods=['POST', 'GET'])
@login_required
def withdraw():
    db = get_db()
    withdraw_data = db.execute(
                    'SELECT withdrawn_amount, withdrawn_amount FROM user_data WHERE id = ?;'
                    ,(session['user_id'], )).fetchall()

    if not withdraw_data:
        withdraw_data = [0] * 2

    if request.method == 'POST':
        error = None

        amount_entered = int(request.form['amount'])
        holder_name = request.form['holder-name']
        ifsc_code = request.form['ifsc-code']
        account_number = int(request.form['account-number'])
        upi_id = request.form['holder-name']
        if amount_entered < 100:
            error = 'Withdraw amount should be greater 100 INR'
        elif amount_entered > withdraw_data[0]:
            error = 'Insufficient Balance'

        if error is None:
            message = 'Successful' 
            flash(message)
            return render_template('blog/withdraw.html', withrawable_amount=withdraw_data[1], withdrawn_cash=withdraw_data[0])

        flash(error)
        return render_template('blog/withdraw.html', withrawable_amount=withdraw_data[1], withdrawn_cash=withdraw_data[0])
    return render_template('blog/withdraw.html', withrawable_amount=withdraw_data[1], withdrawn_cash=withdraw_data[0])


@bp.route('/buy/<equipment_index>')
@login_required
def buy_equipment(equipment_index):
    equipment_index = int(equipment_index)
    equipment = current_app.config['equipments_data'][equipment_index]
    # transaction here

    db = get_db()
    try:
        db.execute(
            'INSERT INTO lease (user_id, daily_income, total_income, leased_days, accumulated_income) VALUES (?, ?, ?, ?, ?)',
            (session['user_id'], *equipment)
            )
        db.commit()
    except db.IntegrityError:
        raise Exception('lease table create error')

    return redirect(url_for('main'))


@bp.route('my_leasing/')
@login_required
def my_leasing():
    db = get_db()
    all_leases = db.execute( 'SELECT daily_income, total_income, leased_days, accumulated_income FROM lease WHERE user_id = ?' , 
            (session['user_id'],)).fetchall()
    return render_template('blog/my_leasing.html', all_leases=all_leases)

@bp.route('withdrawal-record/')
@login_required
def withdrawal_record():
    db = get_db()
    all_records = []
    return render_template('blog/withdrawal_record.html', all_records=all_records)
