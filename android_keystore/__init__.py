__all__ = ['main']

import os
import subprocess

import click
from password_generator import PasswordGenerator

KEY_STORE_NAME = 'keystore.jks'
KEY_STORE_PROPERTIES_NAME = 'keystore.properties'


@click.command()
@click.option('--common-name', type=str, required=True)
def main(common_name: str):
    if os.path.exists(KEY_STORE_NAME):
        raise click.ClickException(f'{KEY_STORE_NAME} already exists.')
    if os.path.exists(KEY_STORE_PROPERTIES_NAME):
        raise click.ClickException(f'{KEY_STORE_PROPERTIES_NAME} already exists.')

    # prepare password for keystore
    pwo = PasswordGenerator()
    pwo.minlen = 32
    pwo.maxlen = 32
    pwo.excludelchars = "'"
    release_key_password = pwo.generate()

    subprocess.run(_build_cmd(common_name, release_key_password), shell=True, check=True)

    with open(KEY_STORE_PROPERTIES_NAME, 'w') as f:
        print(f'key0={release_key_password}', file=f)


def _build_cmd(common_name: str, password: str):
    cmd = 'keytool -genkey -v ' \
          f'-keystore {KEY_STORE_NAME} ' \
          '-keyalg RSA -keysize 2048 -validity 10000 ' \
          f'-dname "CN={common_name}" ' \
          f"-storepass '{password}' " \
          f"-keypass '{password}' " \
          f'-alias key0'
    return cmd
