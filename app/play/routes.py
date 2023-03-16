from app.play import bp
from random import randint
from datetime import timedelta
from flask import Flask, request, redirect, session, url_for, flash
from flask.templating import render_template
from sqlalchemy.sql import func
fl_session = session
from app.models.game_tables import *
from app.models.authentication_check import *
from app.play.words import chose_list, list_of_words
from app.play.letters import letter_blend

# function to render index page (home)
@bp.route('/')
def index():
    user_words = Guess.query.all()
    resp = Secrets.query.all()
    player = Users.query.all() 
    points = Scores.query.all()
    max_score = db.session.query(func.max(Scores.score).label("max_score"))
    total_score = db.session.query(func.sum(Scores.score).label("total_score"))
    every_score = []
    for _res in total_score.all():
        every_score.append(_res)
    if(user_words and resp):
        return render_template('play/index.html',every_score=every_score,max_score=max_score, total_score=total_score, user_words=user_words, resp=resp, player=player, points=points, fl_session=fl_session)
    else:
        return render_template('play/index.html', fl_session=fl_session)
    
@bp.route('/us')
def about_us():
   return render_template('play/about.html', fl_session=fl_session)

@bp.route('/add_data')
def add_data():
    end_of_round = False
    if Guess.query.get(3) != None:
        end_of_round = True
        flash('Vous avez épuisé vos trois chances, une nouvelle manche commence')
    is_a_turn = False
    round_num = randint(1,3)
    db.session.query(Secrets).delete()
    db.session.query(Guess).delete()
    db.session.query(Letters).delete()
    db.session.query(Scores).delete()
    db.session.query(Users).delete()
    db.session.commit()
    base_list = chose_list(round_num)
    secret_words = list_of_words(base_list)[0]
    indice = list_of_words(base_list)[1][0]
    
    if secret_words != '':
        letters = letter_blend(secret_words)
        blend_words = Letters(round_1=letters) 
        secret_1 = secret_words[0]
        secret_2 = secret_words[1]
        secret_3 = secret_words[2]
        first = Secrets(secret_1=secret_1, secret_2=secret_2,secret_3=secret_3, theme=indice)
        db.session.add(first)
        db.session.add(blend_words)
        db.session.commit()
        
    words_star = Secrets.query.all()
    return render_template('play/play.html',end_of_round=end_of_round, words_star=words_star, fl_session=fl_session,first=first,letters=letters, secret_words=secret_words, word_1=secret_1,word_2=secret_2,word_3=secret_3, is_a_turn = is_a_turn, blend_words=blend_words)

@bp.route('/turn')
def turns():
    words_star = Secrets.query.all()
    blend_words = Letters.query.all()
    is_a_turn = True
    if Guess.query.get(3) != None:
        return redirect(url_for('play.add_data'))
       
    return render_template('play/play.html',is_a_turn = is_a_turn, fl_session=fl_session,blend_words=blend_words,words_star=words_star)

# function to add profiles
@bp.route('/add', methods=["POST"])
def profile():
    word = request.form.get("word")
    pseudo = request.form.get("pseudo")
    words_star = Secrets.query.all()
  
    if word == words_star[-1].secret_1 or word == words_star[-1].secret_2 or word == words_star[-1].secret_3:
        if db.session.query(Guess).filter(Guess.word==word).all():
            point = -1
        else:
            point = 1
    else:
        point = 0

    if word != '' and pseudo != '':
        answ = Guess(round=1,word=word, user_id=pseudo)
        you = Users(pseudo=pseudo, guess=word)
        points = Scores(score=point,score_object=word, scores_id = pseudo)
        db.session.add(answ)
        db.session.add(you)
        db.session.add(points)
        db.session.commit()
        return redirect(url_for('play.index'))
    if word != words_star:
        return redirect(url_for('play.index'))
    else:
	    return redirect(url_for('play.index'))
 

@bp.route('/delete/<int:id>')
def erase(id):
    try:
        data = Guess.query.get(id)
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('play.index'))
    except:
        return redirect(url_for('play.index'))
    
@bp.route('/delete_score/<int:id>')
def delete_score(id):
    try:
        data = Scores.query.get(id)
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('play.index'))
    except:
        return redirect(url_for('play.index'))
        
	

# @bp.route('/delete_all/<int:id>')
# def delete_all(id):
#     data = Secrets.query.get(id)
#     db.session.delete(data)
#     db.session.commit()
#     return redirect(url_for('play.index'))

# if __name__ == '__main__':
#     app.secret_key = os.urandom(12)
#     app.run(debug=True,host='0.0.0.0', port=4000)