# Generated by Django 4.2.7 on 2024-03-05 07:12

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import location_field.models.plain


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('event', models.CharField(choices=[('S', 'siembra'), ('T', 'trasplante'), ('C', 'Cosecha'), ('R', 'riego'), ('F', 'fumigacion'), ('P', 'poda')], max_length=1)),
                ('estacion', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Huerto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubicacion', location_field.models.plain.PlainLocationField(max_length=63)),
                ('sitio', models.CharField(choices=[('M', 'maceta'), ('J', 'jardin'), ('T', 'terraza'), ('P', 'parcela')], max_length=1)),
                ('sustrato', models.CharField(choices=[('ARE', 'arenoso'), ('ARC', 'arcilloso'), ('LIM', 'limoso'), ('FRA', 'franco'), ('TUR', 'turbado')], max_length=3)),
                ('area', models.FloatField(blank=True, null=True)),
                ('acidez', models.FloatField(blank=True, null=True)),
                ('abonado', models.BooleanField()),
                ('disponible', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Plaga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origen', models.CharField(choices=[('V', 'virico'), ('B', 'bacteriano'), ('F', 'fungico'), ('A', 'animal'), ('P', 'vegetal')], max_length=1)),
                ('descripcion', models.TextField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('HE', 'herbacea'), ('AL', 'árbol'), ('AO', 'arbusto')], max_length=2)),
                ('ciclo', models.CharField(choices=[('A', 'anual'), ('B', 'bianual'), ('P', 'perenne')], max_length=1)),
                ('nombre_comun', models.CharField(db_column='nombre', max_length=20)),
                ('nombre_cientifico', models.CharField(max_length=30)),
                ('phmax', models.FloatField()),
                ('phmin', models.FloatField()),
                ('epoca_siembra', models.DateField(db_column='siembra_recomendada', default=django.utils.timezone.now)),
                ('fecha_siembra', models.DateField(db_column='siembra_real', default=django.utils.timezone.now)),
                ('recoleccion', models.DateField(db_column='fecha_recoleccion', default=django.utils.timezone.now)),
                ('tiempo_trasplante', models.IntegerField()),
                ('temp_max', models.IntegerField()),
                ('temp_min', models.IntegerField()),
                ('horas_luz', models.IntegerField()),
                ('demanda_hidrica', models.FloatField(blank=True, null=True)),
                ('huerto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plantas_huerto', to='Huerto.huerto')),
            ],
        ),
        migrations.CreateModel(
            name='Planta_regada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Huerto.planta')),
            ],
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('uploaded_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('rol', models.PositiveSmallIntegerField(choices=[(1, 'administrador'), (2, 'usu'), (3, 'usu_premium')], default=2)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Votacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_voto', models.DateTimeField(default=django.utils.timezone.now)),
                ('puntuacion', models.IntegerField()),
                ('comentarios', models.TextField(max_length=2000)),
                ('huerto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='huerto_voto', to='Huerto.huerto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_voto', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Usu_premium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Usu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tratamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(max_length=150)),
                ('consejos', models.TextField(max_length=1000)),
                ('aplicacion', models.TextField(max_length=200)),
                ('plaga', models.ManyToManyField(to='Huerto.plaga')),
            ],
        ),
        migrations.CreateModel(
            name='Riego',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto', models.CharField(choices=[('A', 'agua'), ('F', 'fertilizante'), ('L', 'lluvia'), ('P', 'plaguicida')], max_length=1)),
                ('planta', models.ManyToManyField(through='Huerto.Planta_regada', to='Huerto.planta')),
            ],
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_promocion', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=1000)),
                ('descuento', models.IntegerField()),
                ('fecha_promocion', models.DateField(default=django.utils.timezone.now)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='planta_regada',
            name='riego',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Huerto.riego'),
        ),
        migrations.CreateModel(
            name='PlagaPlanta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plaga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Huerto.plaga')),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Huerto.planta')),
            ],
        ),
        migrations.AddField(
            model_name='plaga',
            name='planta',
            field=models.ManyToManyField(through='Huerto.PlagaPlanta', to='Huerto.planta'),
        ),
        migrations.CreateModel(
            name='Incidencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(max_length=2000)),
                ('fecha_incidencia', models.DateField(db_column='fecha', default=django.utils.timezone.now)),
                ('huerto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='huerto_incidencia', to='Huerto.huerto')),
            ],
        ),
        migrations.AddField(
            model_name='huerto',
            name='usuario',
            field=models.ManyToManyField(related_name='usuario_huerto', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('descripcion', models.TextField(max_length=2000)),
                ('plaga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plaga_plant', to='Huerto.plaga')),
            ],
        ),
        migrations.CreateModel(
            name='Gastos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('herramientas', models.FloatField()),
                ('facturas', models.FloatField()),
                ('imprevistos', models.FloatField()),
                ('Descripcion', models.TextField(max_length=2000)),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_gasto', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fruto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('tipo', models.CharField(max_length=20)),
                ('planta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Huerto.planta')),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(max_length=2000)),
                ('calendario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Huerto.calendario')),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Huerto.planta')),
            ],
        ),
        migrations.AddField(
            model_name='calendario',
            name='Planta',
            field=models.ManyToManyField(through='Huerto.Evento', to='Huerto.planta'),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publicacion', models.CharField(choices=[('C', 'comentario'), ('N', 'noticia'), ('E', 'enlace'), ('T', 'tutorial'), ('R', 'reseña')], max_length=1)),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('etiqueta', models.CharField(max_length=15)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_blog', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banco', models.CharField(choices=[('C', 'Caixa'), ('B', 'BBVA'), ('U', 'Unicaja'), ('I', 'ING')], max_length=1)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_banco', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
