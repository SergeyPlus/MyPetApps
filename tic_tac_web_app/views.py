from flask import url_for, flash
from flask import render_template, request, redirect, session, abort
from flask_mail import Message

from config import LoggerConfig
from forms import MyRegistrationForm, MyLogInForm, PlayersForms, TicTacFieldTable, ChangePassword
import werkzeug.exceptions
from werkzeug.security import generate_password_hash

import logging
from logging import config
import datetime
from typing import Dict

from app import create_app, mail

from data_base import UserDbInterface, UserDb
from work_objects import Game, Login, Players


config.dictConfig(LoggerConfig.log_config_dict)
view_logger = logging.getLogger('view_logger')
view_logger.propagate = False

app = create_app(config_name='development')


@app.route('/', methods=['GET', 'POST'])
def entry_point():
    """
    View function is a start point where User could go to registration or log in
    """

    form = MyLogInForm()

    if session.get('login'):
        return redirect(url_for('get_main_page', login=session['login']))

    elif form.validate_on_submit() and Login.check_login_and_password(form):
        session['login'] = form.login.data
        view_logger.info(f'The name of user {session.get("login")} was set to the session')
        return redirect(url_for('get_main_page', login=session['login']))

    elif form.validate_on_submit() and not Login.check_login_and_password(form):
        flash('please check your login or password and try to enter again')

    view_logger.info(f'There was gotten GET request')
    return render_template('entry_point.html',
                           form=form,
                           now=datetime.datetime.utcnow()
                           )


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    """
    Vie function which renders registration form.
    If registration passed OK User automatically redirect to entry_point view
    function for log in
    """
    reg_form = MyRegistrationForm()

    if reg_form.validate_on_submit():

        if Login.check_login(reg_form):
            UserDbInterface.add_data_to_database(reg_form)
            flash(f'{reg_form.name.data}, your registration is successfully made')
            return redirect(url_for('entry_point'))

        flash(f'user with login "{reg_form.login.data}" already has. please set different one')

    return render_template('registration.html',
                           reg_form=reg_form,
                           now=datetime.datetime.utcnow()
                           )


@app.route('/main_page/<login>/')
def get_main_page(login):
    """
    Main page. After log in User comes to this page and then make choose where go further. Now it's available
    the only Tic tac game
    """
    if not session.get('login') or session.get('login') != login:
        abort(401)
    return render_template('main_page.html',
                           login=login,
                           now=datetime.datetime.utcnow()
                           )


@app.route('/main_page/set_profile', methods=['GET', 'POST'])
def set_profile():
    if not session.get('login'):
        abort(401)

    return render_template('profile.html',
                           now=datetime.datetime.utcnow(),
                           )


@app.route('/main_page/tic_tac_game_players_introduction', methods=['GET', 'POST'])
def tic_tac_game_players_introduction():
    """
    View function which is rendering tic tac game page and require to set player names.
    """
    if not session.get('login'):
        abort(401)

    # if flag = 0 it will be rendered form_players with inputting player names
    players = Players()
    game_render_form: str = Game.game_context.get('game_render_form')
    view_logger.info(
        f'Players introduction. Game_render_form: {Game.game_context.get("game_render_form")}')

    form_players = PlayersForms(meta={'csrf': False})
    if form_players.validate_on_submit() and game_render_form == 'set_player_names':
        view_logger.info(f'The players form is validated')

        players.players_data['name_1'] = form_players.player_1_name.data
        players.players_data['name_2'] = form_players.player_2_name.data
        Game.identify_symbol()
        Game.game_context['game_render_form'] = 'game'
        session['players_data'] = players.players_data

        view_logger.info(
            f"Player_1 data: [name  {session.get('players_data')['name_1']}, "
            f"              sym  {session.get('players_data')['sym_1']}, "
            f"              score {session.get('players_data')['score_1']}]")

        view_logger.info(
            f"Player_2 data: [name  {session.get('players_data')['name_2']}, "
            f"              sym  {session.get('players_data')['sym_2']}, "
            f"              score {session.get('players_data')['score_2']}]")
        return redirect(url_for('tic_tac_game_start_game'))
    return render_template(
        'tic_tac_game.html',
        player_1_name=session.get('players_data', {}).get('name_1'),
        player_2_name=session.get('players_data', {}).get('name_2'),
        field_table=Game.game_context.get("tic_tac_table"),
        now=datetime.datetime.utcnow(),
        winner=Game.game_context['winner'],
        game_render_form=Game.game_context['game_render_form']
    )


@app.route('/main_page/tic_tac_game_start_game', methods=['GET', 'POST'])
def tic_tac_game_start_game():
    if not session.get('login'):
        abort(401)
    
    players = Players()
    tic_tac_form = TicTacFieldTable(meta={'csrf': False})
    if tic_tac_form.validate_on_submit():
        response: Dict = tic_tac_form.data
        view_logger.info(f"Received turn from Player with symbol {response}")
        
        message = Game.game_manager(response)
        if message:
            flash(message=message)
            return redirect(url_for('tic_tac_game_start_game'))
        
        view_logger.info(f'Game context {Game.game_context}')
        session['players_data'] = players.players_data
        return redirect(url_for('tic_tac_game_start_game'))
    view_logger.info(f'Game_render_form {Game.game_context["game_render_form"]}')
    return render_template(
        'tic_tac_game.html',
        player_1_name=session.get('players_data', {}).get('name_1'),
        player_2_name=session.get('players_data', {}).get('name_2'),
        field_table=Game.game_context.get("tic_tac_table"),
        now=datetime.datetime.utcnow(),
        winner=Game.game_context['winner'],
        game_render_form=Game.game_context['game_render_form']
    )

@app.route('/main_page/tic_tac_game_change_game/<int:code>/')
def tic_tac_game_change_game(code):
    if not session.get('login'):
        abort(401)
    
    response = request.args.to_dict()
    view_logger.info(f'Received GET request with {response} with code {code}')

    # in order to play next round of the game with same players
    if code == 0 and response.get('restart') == 'yes': 
        return redirect(url_for('tic_tac_game_change_game', code=1))

        # in order to end the game with these players and start game for new players
    elif code == 0 and response.get('restart') == 'no': 
        return redirect(url_for('tic_tac_game_change_game', code=2))

    # in order to restart game
    if code == 1:
        view_logger.info(f'Worked restart game: code = {code}')
        Game.restart_game_with_same_players()
        return redirect(url_for('tic_tac_game_start_game'))

    # in order to leave the game and go to main page
    elif code == 2:
        view_logger.info(f'Worked leave game: code = {code}')
        Game.restart_game_with_new_players()
        players = Players()
        session['players_data'] = players.players_data
        return redirect(url_for('get_main_page', login=session.get('login')))

    view_logger.info(
        f'Session data winner {Game.game_context}')

    return render_template(
        'tic_tac_game.html',
        player_1_name=session.get('players_data', {}).get('name_1'),
        player_2_name=session.get('players_data', {}).get('name_2'),
        field_table=Game.game_context.get("tic_tac_table"),
        now=datetime.datetime.utcnow(),
        winner=Game.game_context['winner'],
        game_render_form=Game.game_context['game_render_form']
    )


@app.route('/remind_password', methods=["GET", "POST"])
def remind_password():

    change_password_form = ChangePassword()
    view_logger.info(f'Request data - {change_password_form.data}')
    if change_password_form.validate_on_submit():

        login: str = change_password_form.login.data
        email: str = change_password_form.email.data
        view_logger.info(f'Remind password starting, received login {login} and email {email} for processing')

        user_data: UserDb = UserDbInterface.get_user_data(login)
        if email == user_data['email']:
            view_logger.info(f'Login {user_data["login"]} is email {user_data["email"]} is correct. Sending email')

            password: str = change_password_form.password.data
            hash_password: str = generate_password_hash(password)
            UserDbInterface.update_password(login, hash_password)

            subject = 'From Tic-tac app'
            email_message: str = (f'Hello {user_data["name"]}! '
                                  f'\nThis is tic_tac support team. Your NEW password is {password}. '
                                  f'\n\nLooking forward You playing in our app!')
            msg = Message(body=email_message,
                          sender='seregasun@list.ru',
                          recipients=[user_data["email"]],
                          subject=subject)
            mail.send(msg)
            flash(f'the password was sent at Your email')
            return redirect(url_for('entry_point'))

        flash(f'please set correct login or email which you used for registration')
        return redirect(url_for('remind_password'))
    return render_template('remind_password.html',
                           now=datetime.datetime.utcnow(),
                           change_password_form=change_password_form)


@app.errorhandler(werkzeug.exceptions.HTTPException)
def handle_exception(e):

    if isinstance(e, werkzeug.exceptions.Unauthorized):
        view_logger.info(f'Error handler starting to work. Exception info {e}')
        error_message = 'Please make authorization'
        return render_template('error_handler.html', error_message=error_message, now=datetime.datetime.utcnow())
    elif isinstance(e, werkzeug.exceptions.NotFound):
        view_logger.info(f'Error handler starting to work. Exception info {e}')
        error_message = 'Incorrect URL'
        return render_template('error_handler.html', error_message=error_message, now=datetime.datetime.utcnow())
    view_logger.info(f'Error handler starting to work. Exception info {e}')
    error_message = 'Ooops! Something goes wrong'
    return render_template('Something goes wrong', error_message=error_message, now=datetime.datetime.utcnow())


if __name__ == '__main__':
    app.run(port=5001)
