# Naruth Kongurai
# Version 1.0.1
# Simple program to fetch scores, fixtures, live updates, and news for Liverpool F.C using command-line-interface. 
# MIT License - Copyrighted 2017

import click
import requests
import json
from texttable import Texttable, get_color_string, bcolors

@click.command(context_settings=dict(max_content_width=200, help_option_names=['-h', '--help']))
@click.option('--info', '-i', is_flag=True, help='Lists competition names')
@click.option('--fixtures', '-f', help='Looks up Liverpool fixtures for a certain nuimber of days from now')
@click.option('--live', '-l', is_flag=True, help='Live score report')
@click.option('--standings', '-s', is_flag=True, help='Retrieves the a specific competition\'s current standings')
@click.option('--players', '-p', is_flag=True, help='Retrieves all players in the Liverpool squad')
@click.option('--news', '-n', is_flag=True, help='Show Liverpool team news')


def start(info, fixtures, live, standings, players, news):
    """Fetch scores, fixtures, live updates, and news for Liverpool F.C using command-line-interface. 

    "Liverpool Football Club is a professional association football club based in Liverpool, Merseyside, 
    England. They compete in the Premier League, the top tier of English football." - Wikipedia
    
    This CLI application is written in Python as my own personal project. For feedback or report, please 
    send an email to naruthk@uw.edu (Naruth Kongurai).
        
    ===================================================

    """

    global base_url, headers

    base_url = 'http://api.football-data.org/'
    headers = {'X-Auth-Token': 'c2c9d320022e49d184e6845a7e88673d'}
    
    printIntro()

    if info:
        getCompetitionDetails()
    if fixtures:
        getFixtures(fixtures)
    if live:
        click.echo('Currently unsupported')
    if standings:
        getStandings()
    if players:
        getPlayers()
    if news:
        click.echo('Currently unsupported')


def getCompetitionDetails():
    # Retrives the details of the Premier League, which is the competition that Liverpool are playing in
    
    json_competition = getJson('v1/competitions') # Retrieve JSON data
    print '================= COMPETITIONS ===================='
    for item in json_competition:
        print '    [' + item['league'] + '] - ' + item['caption']
    print '==================================================='


def getFixtures(days):
    # Retrives the upcoming fixtures by a specified number of days"

    list_dates = []
    list_home_teams = []
    list_away_teams = []
    list_goalsFor = []
    list_goalsAgainst = []

    json_fixtures = getJson('v1/teams/64/fixtures?timeFrame=n' + str(days)) # Retrieve JSON data
    for item in json_fixtures['fixtures']:
        datetime = item['date'] # Slice Date from 2017-08-19T14:00:00Z to 19 August 2017 (14:00)
        day = datetime[8:10]
        month = datetime[5:7]
        year = datetime[0:4]
        monthDict = {   # Convert month numbers to its proper names
                '01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', 
                '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', 
                '11':'Nov', '12':'Dec'}
        dateString = '[' + day + ' ' + monthDict[month] + ' ' + year + ']'
        
        list_dates.append(dateString)
        list_home_teams.append(str(item['homeTeamName']))
        list_away_teams.append(str(item['awayTeamName']))
        
        if str(item['status']) in ('SCHEDULED', 'TIMED'):
            list_goalsFor.append(' - ')
            list_goalsAgainst.append(' - ')
        else:
            list_goalsFor.append(str(item['result']['goalsHomeTeam']))
            list_goalsAgainst.append(str(item['result']['goalsAwayTeam']))
    
    # Table setup
    table_fixtures = Texttable()
    table_fixtures.set_deco(Texttable.HEADER)
    table_fixtures.set_cols_align(['l', 'r', 'c', 'c', 'l'])
    table_fixtures.set_cols_width(['15', '20', '1', '1', '20'])
    for row in zip(
            list_dates, list_home_teams, list_goalsFor, 
            list_goalsAgainst, list_away_teams):
        table_fixtures.add_row(row)

    printHeader('fixtures')
    printFooter(table_fixtures.draw())


def getStandings():
    # Retrieves and prints a table of team standings, including information such
    # as Position Number, Team Name, Number of Games Played, Wins, Draws, Losses,
    # Goals For, Goals Against, Goals Differences, and Total Points
    
    list_pos = []
    list_teams = []
    list_played = []
    list_wins = []
    list_draws = []
    list_losses = []
    list_goals = []
    list_goalsagainst = []
    list_goalsdiff = []
    list_points = []

    json_standings = getJson('v1/competitions/445/leagueTable') # Retrieve JSON data
    # Read through each row in the JSON file and appends to appropriate lists
    for item in json_standings['standing']:
        list_pos.append(str(item['position']))
        list_teams.append(item['teamName'])
        list_played.append(str(item['playedGames']))
        list_wins.append(str(item['wins']))
        list_draws.append(str(item['draws']))
        list_losses.append(str(item['losses']))
        list_goals.append(str(item['goals']))
        list_goalsagainst.append(str(item['goalsAgainst']))
        list_goalsdiff.append(str(item['goalDifference']))
        list_points.append(str(item['points']))

    # Table setup
    table_standings = Texttable()
    table_standings.set_cols_align(['c', 'l', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c'])
    table_standings.set_cols_width(['3', '30', '6', '5', '5', '7', '5', '5', '5', '6'])
    table_standings.set_deco(Texttable.HEADER)
    table_standings.add_row([
            'Pos', 'Team', 'Played', 'Wins', 'Draws', 'Losses', 'Goals', 'GA', 'GD', 'Points'])
    for row in zip(
            list_pos, list_teams, list_played, list_wins, 
            list_draws, list_losses, list_goals, list_goalsagainst, 
            list_goalsdiff, list_points):
        table_standings.add_row(row)

    printHeader('standings')
    print 'Matchday: ' + str(json_standings['matchday']) + "\n"
    printFooter(table_standings.draw())



def getPlayers():
    # Retrieves the jersey numbers, names, positions, date of births, and
    # nationalities of the players and outputs the data in a tabulated way

    list_numbers = []
    list_names = []
    list_positions = []
    list_dateOfBirth = []
    list_nationalities = []

    json_players = getJson('v1/teams/64/players')   # Retrieve JSON data
    # Read through each row in the JSON file and appends to appropriate lists
    for item in json_players['players']:
        list_numbers.append(str(item['jerseyNumber']))
        list_names.append(item['name'])
        list_positions.append(str(item['position']))
        list_dateOfBirth.append(str(item['dateOfBirth']))
        list_nationalities.append(str(item['nationality']))

    # Table setup
    table_players = Texttable()
    table_players.set_cols_align(['c', 'l', 'l', 'l', 'l'])
    table_players.set_cols_width(['3', '30', '20', '10', '20'])
    table_players.set_deco(Texttable.HEADER)
    table_players.add_row(['No.', 'Name', 'Position', 'Date of Birth', 'Nationality'])
    for row in zip(list_numbers, list_names, list_positions, list_dateOfBirth, list_nationalities):
        table_players.add_row(row)

    printHeader('players')
    print 'Number of players in the squad: ' + str(json_players['count']) + "\n"
    printFooter(table_players.draw())


def getJson(app_url):
    # Fetches data based on given URL
    return requests.get(base_url+app_url, headers=headers).json()

def printIntro():
    # Prints basic help message to the user"
    print '\nType cli-soccer -h for more help + information.\n'

def printHeader(title):
    # Prints title in uppercase
    print '==================== ' + str.upper(title) + ' ======================'

def printFooter(table):
    # Prints a particular table
    print table + '\n==================================================='