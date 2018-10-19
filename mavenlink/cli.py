import os
import click
import subprocess
from pprint import pformat
from mavenlink.settings import conf, data
from mavenlink.services import MavenlinkService

ts = MavenlinkService(conf=conf)
OBJECT_TYPES = ('module', 'layer', 'environment')


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.pass_context
@click.argument('path', default=os.path.expanduser('~'))
@click.option('--username', prompt=True)
@click.option('--password', prompt=True,
                            hide_input=True,
                            confirmation_prompt=True)
def setup(ctx, path, username, password):
    """
    Create a .mavenlink.yml at a specified path
    """
    print('init a new project at "{}"'.format(path))
    resp = ts.initialize_project(path=path,
                                 username=username,
                                 password=password)
    click.echo('\nConfig\n"""{}"""'.format(resp))

@cli.command()
@click.pass_context
def config(ctx):
    """
    show the current config
    """
    click.echo('\nYour current config is:\n"""{}"""'.format(pformat(data)))

@cli.command()
@click.option('--username')
@click.option('--password', prompt=True,
                            hide_input=True,
                            confirmation_prompt=True)
@click.pass_context
def login(ctx, username, password):
    """
    Will create a new {}
    """.format(OBJECT_TYPES)
    print('Login to mavenlink')
    resp = ts.login(username=username, password=password)
    click.echo(resp)


@cli.command()
@click.pass_context
@click.argument('stdinput', type=click.File('rb'))
@click.option('--filename', type=click.Path(exists=True))
def consume(ctx, stdinput, filename):
    """
    Will take a file or stdin and process it
    """
    if filename:
        filename = click.format_filename(filename)
        resp = ts.consume(input=filename)
    else:
        resp = ts.consume(input=stdinput)
    
    click.echo(resp)


@cli.command()
@click.pass_context
def preview(ctx):
    """
    Will show the current timesheet as a preview
    """
    resp = ts.preview()
    click.echo(resp)


@cli.command()
@click.pass_context
def send(ctx, environment, command):
    """
    Will send the current timesheet to mavenlink
    """
    click.echo('Sending...')


cli.add_command(setup)
cli.add_command(config)
cli.add_command(login)
cli.add_command(consume)
cli.add_command(preview)
cli.add_command(send)

def run():
    cli(obj={})

if __name__ == '__main__':
    run()