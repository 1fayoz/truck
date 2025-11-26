from django.core.management.base import BaseCommand

from apps.common.utils import dump_pg_data
from core.settings.base import DATABASES


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

        dump_pg_data(
            project_name, db_name, db_user, db_password, db_host, db_port, chat_id, bot_token
        )
        self.stdout.write(self.style.SUCCESS("Backup process completed successfully."))
