import click
import requests
import json
from texttable import Texttable, get_color_string, bcolors

base_url = 'http://api.football-data.org/'
headers = {'X-Auth-Token': 'c2c9d320022e49d184e6845a7e88673d'}

global table
table = Texttable()

@click.command(context_settings=dict(max_content_width=200, help_option_names=['-h', '--help']))
@click.option('--info', is_flag=True, help='Lists competition names')
@click.option('--fixtures', help='Looks up Liverpool fixtures by a certain nuimber of days from now')
@click.option('--live', is_flag=True, help='Live score report')
@click.option('--standings', is_flag=True, help='Retrieves the a specific competition\'s current standings')
@click.option('--players', is_flag=True, help='Retrieves all players in the Liverpool squad')
@click.option('--news', is_flag=True, help='Show Liverpool team news')

def start(info, fixtures, live, standings, players, news):
    # Introduction message
    """Fetch scores, fixtures, live updates, and news for Liverpool F.C using command-line-interface. 

    "Liverpool Football Club is a professional association football club based in Liverpool, Merseyside, England. They compete in the Premier League, the top tier of English football." - Wikipedia
    
    This CLI application is written in Python as my own personal project. For feedback or report, please send an email to naruthk@uw.edu (Naruth Kongurai).
        

    ===================================================

    """

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
        click.echo('Currently unsupported')
    if news:
        click.echo('Currently unsupported')


def printIntro():
    print '\nType cli-soccer -h for more help + information.\n'

def getCompetitionDetails():
    app_url = 'v1/competitions'
    json_competition = requests.get(base_url+app_url, headers=headers).json()
    print '================= COMPETITIONS ===================='
    for item in json_competition:
        print '    [' + item['league'] + '] - ' + item['caption']
    print '==================================================='

def getFixtures(days):
    print '========== FIXTURES ===== ' + str(days) + ' days ahead ==========='
    json_fixtures = ""
    app_url = 'v1/teams/64/fixtures?timeFrame=n' + str(days)
    json_fixtures = requests.get(base_url+app_url, headers=headers).json()
    for item in json_fixtures['fixtures']:
        # Slice Date from 2017-08-19T14:00:00Z to 19 August 2017 (14:00)
        datetime = item['date']
        day = datetime[8:10]
        month = datetime[5:7]
        year = datetime[0:4]
        monthDict = {'01':'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June', '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}
        print '    [' + day + ' ' + monthDict[month] + ' ' + year + '] - ' + item['status'] + " = " + item['homeTeamName'] + ' vs. ' + item['awayTeamName']
    print '==================================================='

def getStandings():
    print '=================== STANDINGS ====================='
    json_standings = ""
    app_url = 'v1/competitions/445/leagueTable'
    json_standings = requests.get(base_url+app_url, headers=headers).json()
    
    table.set_cols_align(['c', 'l', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c'])
    table.set_cols_width(['3', '30', '5', '5', '7', '5', '5', '5', '6', '6'])
    table.set_deco(Texttable.HEADER)
    list_pos = []
    list_teams = []
    list_wins = []
    list_draws = []
    list_losses = []
    list_goals = []
    list_goalsagainst = []
    list_goalsdiff = []
    list_points = []
    list_played = []

    for item in json_standings['standing']:
        list_pos.append(str(item['position']))
        list_teams.append(item['teamName'])
        list_wins.append(str(item['wins']))
        list_draws.append(str(item['draws']))
        list_losses.append(str(item['losses']))
        list_goals.append(str(item['goals']))
        list_goalsagainst.append(str(item['goalsAgainst']))
        list_goalsdiff.append(str(item['goalDifference']))
        list_points.append(str(item['points']))
        list_played.append(str(item['playedGames']))

    table.add_row(['Pos', 'Team', 'Wins', 'Draws', 'Losses', 'Goals', 'GA', 'GD', 'Points', 'Played'])
    for row in zip(list_pos, list_teams, list_wins, list_draws, list_losses, list_goals, list_goalsagainst, list_goalsdiff, list_points, list_played):
        table.add_row(row)

    final_standings = table.draw()

    print 'Matchday: ' + str(json_standings['matchday']) + "\n"
    print final_standings

    print '==================================================='