import click
import requests
import json

base_url = 'http://api.football-data.org/'
headers = {'X-Auth-Token': 'c2c9d320022e49d184e6845a7e88673d'}
app_url = 'v1/competitions'
data = requests.get(base_url+app_url, headers=headers).json()

@click.command(context_settings=dict(max_content_width=200, help_option_names=['-h', '--help']))
@click.option('--info', is_flag=True, help='Lists competition names')
@click.option('--fixtures', is_flag=True, help='Looks up a competition (i.e. [PL] Premier League)\'s upcoming fixtures')
@click.option('--live', is_flag=True, help='Live score report')
@click.option('--standings', is_flag=True, help='Retrieves the a specific competition\'s current standings')
@click.option('--team', is_flag=True, help='Retrieves information of a particular team')
@click.option('--about', is_flag=True, help='Show developer\'s details')

def start(info, fixtures, live, standings, team, about):
    # Introduction message
    """Cli-soccer offers a fast, programmatic way of retrieving soccer team news, fixtures, league tables, and live scores. Currently in development stage, and only several teams and leauges will work.
    
    For feedback or report, please send an email to naruthk@uw.edu (Naruth Kongurai). Thanks in advance for all the response and support.
        
    
    ===================================================

    """

    if info:
        getMasterDetails()
    if fixtures:
        getFixtures('PL')
    if live:
        click.echo('Currently unsupported')
    if standings:
        click.echo('Currently unsupported')
    if team:
        click.echo('Currently unsupported')
    if about:
        click.echo('Currently unsupported')

def getMasterDetails():
    print '================= COMPETITIONS ===================='
    for item in data:
        print '    [' + item['league'] + '] - ' + item['caption']
    print '==================================================='

def getFixtures(league):
    print(league)