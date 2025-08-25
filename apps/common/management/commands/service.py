from django.core.management.base import BaseCommand

from apps.common.models import Service


class Command(BaseCommand):
    help = "Creates default services"

    def handle(self, *args, **options):
        services = [
            {
                "icon_name": "Newspaper",
                "name": "Qonuniy yangiliklar",
                "des": "Yuk tashish sohasiga oid qoidalaridagi eng so‘nggi o‘zgarishlar bo‘yicha oylik yangiliklar.",
                "status": Service.ServiceStaus.active,
            },
            {
                "icon_name": "ShieldCheck",
                "name": "Sug‘urta chegirmalari",
                "des": "Yuk mashinalari sug‘urtasida 15–25% chegirma. \n Sog‘liqni sug‘urtalashda 10–20% chegirma.",
                "status": Service.ServiceStaus.active,
            },
            {
                "icon_name": "GraduationCap",
                "name": "Bepul onlayn kurslar",
                "des": "Kasbiy malaka oshirish uchun turli mavzulardagi treninglar.",
                "status": Service.ServiceStaus.active,
            },
            {
                "icon_name": "Trophy",
                "name": "Milliy haydovchilar chempionati (NTDC)",
                "des": "A’zolarimiz uchun maxsus tanlov va musobaqalar.",
                "status": Service.ServiceStaus.active,
            },
            {
                "icon_name": "HardHat",
                "name": "Ish xavfsizligi bo‘yicha master-klasslar",
                "des": "Yo‘lda va ish jarayonida xavfsizlik bo‘yicha amaliy treninglar.",
                "status": Service.ServiceStaus.active,
            },
            {
                "icon_name": "Search",
                "name": "Yuk izlash platformasi",
                "des": "A’zolarimizga mo‘ljallangan eksklyuziv yuk topish tizimi.",
                "status": Service.ServiceStaus.active,
            },
            {
                "icon_name": "Gavel",
                "name": "Sud himoyasi",
                "des": "DOT (Transport Departamenti) tekshiruvlarida yuridik yordam ko‘rsatish.",
                "status": Service.ServiceStaus.in_progress,
            },
            {
                "icon_name": "Fuel",
                "name": "Yoqilg‘i shartnomalari",
                "des": "Uyushma a’zolari uchun yoqilg’i quyush shahobchalarida maxsus chegirmali narxlar.",
                "status": Service.ServiceStaus.in_progress,
            },
            {
                "icon_name": "FileSignature",
                "name": "Xalqaro yuk tashish bo‘yicha hujjatlar",
                "des": "CMR shartnomalarini rasmiylashtirishda ko‘maklashish.",
                "status": Service.ServiceStaus.in_progress,
            },
            {
                "icon_name": "BarChart3",
                "name": "Yuk tashish bozori hisobotlari",
                "des": "Oylik va choraklik tahlillar orqali bozor tendensiyalarini taqdim etish.",
                "status": Service.ServiceStaus.in_progress,
            },
            {
                "icon_name": "Gauge",
                "name": "Yoqilg‘i narxlari monitoringi",
                "des": "O‘zbekiston bo‘ylab yoqilg‘i narxlarini real vaqt rejimida kuzatish.",
                "status": Service.ServiceStaus.in_progress,
            },
            {
                "icon_name": "Banknote",
                "name": "Ish haqi bozori tahlillari",
                "des": "Haydovchilar va soha xodimlari uchun eng so‘nggi ish haqi ma’lumotlari.",
                "status": Service.ServiceStaus.in_progress,
            },
            {
                "icon_name": "Globe2",
                "name": "IRU bilan hamkorlik",
                "des": "Xalqaro Yo‘l Transporti Uyushmasi bilan rasmiy aloqalar o‘rnatish.",
                "status": Service.ServiceStaus.in_progress,
            },
            {
                "icon_name": "Briefcase",
                "name": "Individual biznes konsalting",
                "des": "Yuk tashish kompaniyalarini samarali boshqarish bo‘yicha professional maslahatlar.",
                "status": Service.ServiceStaus.in_progress,
            },
        ]

        for service in services:
            obj, created = Service.objects.get_or_create(
                name=service["name"],
                defaults=service
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {obj.name}"))
