# manage.py (mới)
import click
from flask.cli import FlaskGroup
from asrp import create_app

def create_my_app():
    """Factory function cho Flask CLI, trả về Flask app."""
    return create_app()

@click.group(cls=FlaskGroup, create_app=create_my_app)
def cli():
    """Management script cho ứng dụng ASRP."""
    pass

if __name__ == "__main__":
    cli()
