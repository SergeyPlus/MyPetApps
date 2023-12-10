from typing import Dict
import werkzeug.exceptions
from flask import Flask, url_for, flash
from flask import render_template, request, redirect, session, abort
from forms import MyRegistrationForm, MyLogInForm, PlayersForms, TicTacFieldTable
import tic_tac_gaming
import logging
import checking
import datetime
from flask_moment import Moment

logging.basicConfig(level=10, format='%(module)s : %(asctime)s : %(message)s')
app_logger = logging.getLogger(__name__)

app = Flask(__name__)
moment = Moment(app)

app.config['SECRET_KEY'] = '68a118d78edce9e7b0fa1f2a6a8342a169fcd8b2'


@app.route('/', methods=['GET', 'POST'])
def entry_point():
    """
    View function is a start point where User could go to registration or log in
    """

    form = MyLogInForm(meta={'csrf': False})

    if session.get('login'):
        return redirect(url_for('get_main_page', login=session['login']))

    elif form.validate_on_submit() and checking.check_login_and_password(form):
        session['login'] = form.login.data
        app_logger.info(f'The name of user {session.get("login")} was set to the session')
        return redirect(url_for('get_main_page', login=session['login']))

    elif form.validate_on_submit() and not checking.check_login_and_password(form):
        flash('please check your login or password and try to enter again')

    app_logger.info(f'There was gotten GET request')
    return render_template('entry_point.html',
                           form=form,
                           now=datetime.datetime.utcnow()
                           )


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    """
    Vie function which renders registration form. If registration passed OK User automatically redirect to entry_point view
    function for log in
    """
    reg_form = MyRegistrationForm(meta={'csrf': False})

    if request.method == "POST" and reg_form.validate_on_submit():

        if checking.check_login(reg_form):
            checking.add_data_to_database(reg_form)
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


@app.route('/main_page/tic_tac_game/<int:change_game>', methods=['GET', 'POST'])
def tic_tac_game(change_game):
    """
    View function which is rendering tic tac game.
    """

    app_logger.info(f'Game is starting. Restart game value {change_game}')
    if not session.get('login'):
        abort(401)

    #if flag = 0 it will be rendered form_players with inputing player names
    flag: int = 0
    app_logger.info(f'Flag value: {flag}')

    form_players = PlayersForms(meta={'csrf': False})
    if form_players.validate_on_submit() and request.method == 'POST' and form_players.player_1_name.data is not None and form_players.player_2_name.data is not None:
        app_logger.info(f'The players form is validated')

        session['player_1_name'] = form_players.player_1_name.data
        session['player_2_name'] = form_players.player_2_name.data

        app_logger.info(f'Player {session["player_1_name"]} in session and player {session["player_2_name"]} in session')

        if tic_tac_gaming.identify_symbol():
            session['player_1_sym'] = 'x'
            session['player_2_sym'] = '0'
        else:
            session['player_1_sym'] = '0'
            session['player_2_sym'] = 'x'
        app_logger.info(f"{session.get('player_1_name')} plays for {session.get('player_1_sym')}  vs   "
                        f"{session.get('player_2_name')} plays for {session.get('player_2_sym')}")

        # if flag = 1 it will be rendered tic_tac_form - field of the game
        flag += 1
        session['flag'] = flag
        return redirect(url_for('tic_tac_game', change_game=0))

    tic_tac_form = TicTacFieldTable(meta={'csrf': False})
    if tic_tac_form.validate_on_submit() and request.method == 'POST':
        response: Dict = tic_tac_form.data

        app_logger.info(f"Received data from Player with symbol {response}")

        # checking how many symbols player put per 1 turn. It should be only 1 symbol
        if not tic_tac_gaming.check_symbols_quantity_for_turn(response):
            flash(f'please put the only 1 symbol for turn')
            app_logger.info(f"It's not possible to make turn by 2 symbols or without symbol")
            return redirect(url_for('tic_tac_game', change_game=0))

        app_logger.info(f'The checking of symbols quantity passed well')
        tic_tac_gaming.complete_field(response)

        tic_tac_table: Dict = {}
        for index, elem in enumerate(tic_tac_gaming.game_field):
            if elem == 1:
                tic_tac_table[f'nod_{index}'] = f'__X__'
            elif elem == 10:
                tic_tac_table[f'nod_{index}'] = f'__0__'
        session['tic_tac_table'] = tic_tac_table
        app_logger.info(f"The turn was recorded in session successfully  {session['tic_tac_table']}")

        # here it identifies is there a winner and if it happens we receive symbol which wins
        search_sym = tic_tac_gaming.check_winner()
        app_logger.info(f"After checking winner symbol {search_sym}")

        # if we have symbol which wins below we identify Player name who plays by this symbol
        # and put the data to the session
        if search_sym:
            winner = 'player_2_name'
            if session.get('player_1_sym') is search_sym:
                winner = 'player_1_name'
            winner_name = session.get(winner)
            session['winner'] = f"{winner_name} wins"
            app_logger.info(f"Winner is {winner} : {winner_name}")

            score = f'{winner[:8]}_score'
            session[score] = session.get(score, 0) + 1
            app_logger.info(f'Current score {session["player_1_name"]} : {session.get("player_1_score")}; '
                            f'{session["player_2_name"]} : {session.get("player_2_score")}')

            # in order to fix play field once winner is existed put _____ symbol into free cells
            for key in response.keys():
                if not session['tic_tac_table'].get(key):
                    session['tic_tac_table'][key] = '_____'
            app_logger.info(f'Tic_tac_table - {session["tic_tac_table"]}')

        # Checking for win - win situation if there is no empty cells and there is no a winner
        elif not search_sym and len(session['tic_tac_table'].keys()) == 9:
            session['player_1_score'] = session.get('player_1_score', 0) + 1
            session['player_2_score'] = session.get('player_2_score', 0) + 1
            session['winner'] = f" both players {session.get('player_1_name')} and {session.get('player_1_name')} win"
            app_logger.info(f"Win - Win situation")

        return redirect(url_for('tic_tac_game', change_game=0))

    if request.method == 'GET' and request.args.to_dict():
        response = request.args.to_dict()
        app_logger.info(f'Received GET request with {response}')

        # in order to play next round of the game under sme players
        if response.get('restart') == 'yes':
            session.pop('winner', '')
            session['tic_tac_table'].clear()
            tic_tac_gaming.game_field = [0] * 9
            app_logger.info(
                f'Session is empty player {session.get("winner")}, table {session.get("tic_tac_table")}')

        # in order to end the game with these players and start game for new players
        elif response.get('restart') == 'no':
            session.pop('flag', 0)
            session.pop('player_1_name', None)
            session.pop('player_2_name', None)
            session.pop('player_1_score', None)
            session.pop('player_2_score', None)
            session['tic_tac_table'].clear()
            session.pop('winner', '')
            tic_tac_gaming.game_field = [0] * 9
            app_logger.info(
                f'Session is empty player {session.get("player_1_name")}, score {session.get("player_1_score")} {session.get("tic_tac_table")}')
            return redirect(url_for('tic_tac_game', login=session.get('login')))
    app_logger.info(f'Change_game value {change_game}')

    # in order to restart game
    if change_game == 1:
        app_logger.info(f'Worked restart game condition: change_game = {change_game}')
        session['tic_tac_table'] = {}
        tic_tac_gaming.game_field = [0] * 9

    # in order to leave the game and go to main page
    elif change_game == 2:
        app_logger.info(f'Worked leave game condition: change_game = {change_game}')
        session.pop('flag', 0)
        session.pop('player_1_name', None)
        session.pop('player_2_name', None)
        session.pop('player_1_score', None)
        session.pop('player_2_score', None)
        session['tic_tac_table'].clear()
        session.pop('winner', '')
        tic_tac_gaming.game_field = [0] * 9
        app_logger.info(
            f'Session is empty player {session.get("player_1_name")}, score {session.get("player_1_score")} {session.get("tic_tac_table")}')
        return redirect(url_for('get_main_page', login=session.get('login')))

    app_logger.info(f'Result - {session.get("tic_tac_table")}')
    return render_template(
        'tic_tac_game.html',
        player_1_name=session.get('player_1_name'),
        player_2_name=session.get('player_2_name'),
        field_table=session.get("tic_tac_table", {}),
        now=datetime.datetime.utcnow(),
        winner=session.get('winner'),
        flag=session.get('flag')
    )


@app.errorhandler(werkzeug.exceptions.HTTPException)
def handle_exception(e):
    app_logger.info(f'Error handler starting to work. Exception info {e}')
    if isinstance(e, werkzeug.exceptions.Unauthorized):
        error_message = 'Please make authorization'
        return render_template('error_handler.html', error_message=error_message, now=datetime.datetime.utcnow())
    elif isinstance(e, werkzeug.exceptions.NotFound):
        error_message = 'Incorrect URL'
        return render_template('error_handler.html', error_message=error_message, now=datetime.datetime.utcnow())
    error_message = 'Ooops! Something goes wrong'
    return render_template('Something goes wrong', error_message=error_message, now=datetime.datetime.utcnow())


if __name__ == '__main__':
    app.run(debug=True)