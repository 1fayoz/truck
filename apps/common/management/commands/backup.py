import gzip
import io
import os

import requests
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.settings.base import DATABASES


def compress_in_memory(data: bytes) -> bytes:
    compressed_stream = io.BytesIO()
    with gzip.GzipFile(fileobj=compressed_stream, mode='wb') as f_out:
        f_out.write(data)
    return compressed_stream.getvalue()


def send_to_telegram(compressed_data: bytes, project_name: str, chat_id: int, bot_token: str):
    now = timezone.now()
    caption = (
        f'Proyekt: {project_name}\n'
        f'📂 **Yangi ma\'lumotlar bazasi dump fayli** \n'
        f'🕒 **Yaratilgan vaqt:** {now.strftime("%d/%m/%Y %H:%M:%S")}\n'
        f'#{project_name}\n'
    )
    files = {
        'document': ('dump.sql.gz', io.BytesIO(compressed_data), 'application/gzip')
    }
    data = {'chat_id': chat_id, 'caption': caption, 'parse_mode': 'Markdown'}

    res = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendDocument',
        data=data,
        files=files
    )
    if res.status_code != 200:
        return False, f'text: {res.text}, status_code: {res.status_code}'
    return True, 'success'


def dump_pg_data(project_name, db_name, db_user, db_password, db_host, db_port, chat_id, bot_token):
    try:
        command = f'PGPASSWORD={db_password} pg_dump -U {db_user} -h {db_host} -p {db_port} {db_name}'
        dump_data = os.popen(command).read().encode()

        if not dump_data:
            raise Exception("Database dump failed or returned empty.")

        compressed_data = compress_in_memory(dump_data)
        return send_to_telegram(compressed_data, project_name, chat_id, bot_token)
    except Exception as e:
        return False, f'Error: {e}'


class Command(BaseCommand):
    help = "Creates a backup of the PostgreSQL database and sends it to Telegram."

    def handle(self, *args, **options):
        database = DATABASES['default']

        db_name = database['NAME']
        db_user = database['USER']
        db_password = database['PASSWORD']
        db_host = database['HOST']
        db_port = database['PORT']

        bot_token = "7114639308:AAHKYcHotUw2_5yno-O1avO0PedoG3G_07I"
        chat_id = 5593831038
        project_name = "uztruck.org"

        success, message = dump_pg_data(
            project_name, db_name, db_user, db_password, db_host, db_port, chat_id, bot_token
        )

        if success:
            self.stdout.write(self.style.SUCCESS("Backup process completed successfully."))
        else:
            self.stdout.write(self.style.ERROR(f"Backup failed: {message}"))
