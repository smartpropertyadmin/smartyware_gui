from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_project import db
from flask_project.models import Post, audit_income_expenditure, GL_listing, account_code_current, account_code_last
from flask_project.posts.forms import PostForm
from sqlalchemy.sql import func
from datetime import datetime
import itertools
posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        print ('post had been submitted')
        flash('Your post has been created!', 'success')
        print('flash had been submitted')
        return redirect(url_for('main.home'))
        print('post had been redirected')
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route("/4067/income_expenditure", methods=['GET'])
def income_expenditure():
    Income_items =audit_income_expenditure.query.order_by(audit_income_expenditure.id).filter \
        (audit_income_expenditure.income_expenditure =="income").all()
    current_year_end = Income_items[0].__dict__.get("year_end")
    Current_Income_items = audit_income_expenditure.query.order_by(audit_income_expenditure.id).filter \
        ((audit_income_expenditure.income_expenditure == "income") & (audit_income_expenditure.year_end == current_year_end)).all()

    Previous_Income_items = audit_income_expenditure.query.order_by(audit_income_expenditure.id).filter \
        ((audit_income_expenditure.income_expenditure == "income") & (audit_income_expenditure.year_end != current_year_end)).all()

    Expenditure_items = audit_income_expenditure.query.order_by(audit_income_expenditure.id).filter \
        (audit_income_expenditure.income_expenditure =="expenditure").all()
    Current_Expenditure_items= audit_income_expenditure.query.order_by(audit_income_expenditure.id).filter \
        ((audit_income_expenditure.income_expenditure == "expenditure") & (
                    audit_income_expenditure.year_end == current_year_end)).all()
    Previous_Expenditure_items = audit_income_expenditure.query.order_by(audit_income_expenditure.id).filter \
        ((audit_income_expenditure.income_expenditure == "expenditure") & (
                    audit_income_expenditure.year_end != current_year_end)).all()


    return render_template('Income_Expenditure.html',Current_Income_items = Current_Income_items , Previous_Income_items = Previous_Income_items,
                           Current_Expenditure_items=Current_Expenditure_items, Previous_Expenditure_items = Previous_Expenditure_items,
                           datetime = datetime, zip= zip)


@posts.route("/4067/income_expenditure/<string:audit_description>", methods=['GET'])
def income_expenditure_breakdown(audit_description):

    Income_items = audit_income_expenditure.query.order_by(audit_income_expenditure.id).filter \
        (audit_income_expenditure.income_expenditure == "income").all()
    last_year_end = Income_items[-1].__dict__.get("year_end")

    current_ie_breakdown = account_code_current.query.order_by(account_code_current.id).filter \
        (account_code_current.audit_description == audit_description).all()

    last_ie_breakdown = account_code_last.query.order_by(account_code_last.id).filter \
        (account_code_last.audit_description == audit_description).all()
    ie_breakdown_list ={}
    print (current_ie_breakdown[0].__dict__.get('account_description'))

    return render_template('income_expenditure_breakdown.html',current_ie_breakdown =current_ie_breakdown , last_ie_breakdown = last_ie_breakdown ,
                           datetime = datetime, Income_items = Income_items , zip = zip)

@posts.route("/4067/income_expenditure/<string:account_code>/breakdown", methods=['GET'])
def account_code_breakdown(account_code):
    Income_items = audit_income_expenditure.query.order_by(audit_income_expenditure.id).filter \
        (audit_income_expenditure.income_expenditure == "income").all()
    last_year_end = Income_items[-1].__dict__.get("year_end")

    current_ie_breakdown = GL_listing.query.order_by(GL_listing.debit_credit_amt).filter \
        ((GL_listing.account_code== account_code) & (GL_listing.item_date > last_year_end)).all()

    last_ie_breakdown = GL_listing.query.order_by(GL_listing.debit_credit_amt).filter \
        ((GL_listing.account_code == account_code) & (GL_listing.item_date <= last_year_end)).all()


    return render_template('account_code_breakdown.html', current_ie_breakdown=current_ie_breakdown,
                       last_ie_breakdown=last_ie_breakdown,
                       datetime=datetime, Income_items=Income_items, itertools=itertools)


