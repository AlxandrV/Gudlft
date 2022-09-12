import json
from flask import Flask,render_template,request,redirect,flash,url_for

from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
MAX_PLACES = 12
points_per_place = 3


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return render_template('welcome.html', club=club, competitions=competitions, current_datetime=current_datetime)
    except IndexError:
        return render_template('index.html', error=True)
    except Exception as e:
        return page_not_found()


@app.route('/book/<competition>/<club>')
def book(competition,club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    except Exception:
        return page_not_found()



@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired > MAX_PLACES:
        flash(f'Maximum number of places at reservation {MAX_PLACES}!')
    elif placesRequired * points_per_place >= 0 and placesRequired * points_per_place <= int(club['points']):
        club['points'] = int(club['points']) - placesRequired * points_per_place
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        if 'investedPoints' in competition:
            if club['name'] in competition['investedPoints']:
                competition['investedPoints'][club['name']]['places'] += placesRequired
                competition['investedPoints'][club['name']]['points'] += placesRequired * points_per_place
            else:
                competition['investedPoints'][club['name']] = {
                    'places': placesRequired,
                    'points': placesRequired * points_per_place
                }
        else:
            competition['investedPoints'] = {
                club['name']: {
                    'places': placesRequired,
                    'points': placesRequired * points_per_place
                }
            }
        flash('Great-booking complete!')
    elif placesRequired * points_per_place > int(club['points']):
        flash('Insufficient points!')
    elif placesRequired > int(competition['numberOfPlaces']):
        flash('Number of places not available!')
    else:
        flash('Invalid number of places!')
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('welcome.html', club=club, competitions=competitions, current_datetime=current_datetime)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.errorhandler(Exception)
def page_not_found():
    return render_template('page_404.html')