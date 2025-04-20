# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Especialidad(models.Model):
    idespecialidad = models.AutoField(db_column='idEspecialidad', primary_key=True)  # Field name made lowercase.
    nombreespecialidad = models.CharField(db_column='nombreEspecialidad', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'especialidad'

class Implemento(models.Model):
    idimplemento = models.AutoField(db_column='idImplemento', primary_key=True)  # Field name made lowercase.
    nombreimplemento = models.CharField(db_column='nombreImplemento', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'implemento'

class Estadoimplemento(models.Model):
    idestadoimplemento = models.AutoField(db_column='idEstadoImplemento', primary_key=True)  # Field name made lowercase.
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estadoimplemento'


class Pasillo(models.Model):
    idpasillo = models.AutoField(db_column='idPasillo', primary_key=True)  # Field name made lowercase.
    pasillo = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pasillo'


class Estado(models.Model):
    idestado = models.AutoField(db_column='idEstado', primary_key=True)  # Field name made lowercase.
    descripcionestado = models.TextField(db_column='descripcionEstado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estado'

class Paciente(models.Model):
    rutpaciente = models.CharField(db_column='rutPaciente', primary_key=True, max_length=11)  # Field name made lowercase.
    nombrepaciente = models.CharField(db_column='nombrePaciente', max_length=60, blank=True, null=True)  # Field name made lowercase.
    apellidopaciente = models.CharField(db_column='apellidoPaciente', max_length=60, blank=True, null=True)  # Field name made lowercase.
    fechanacimientopaciente = models.DateField(db_column='fechaNacimientoPaciente', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paciente'

class Medico(models.Model):
    rutmedico = models.CharField(db_column='rutMedico', primary_key=True, max_length=11)  # Field name made lowercase.
    idespecialidad = models.ForeignKey(Especialidad, models.DO_NOTHING, db_column='idEspecialidad', blank=True, null=True)  # Field name made lowercase.
    nombremedico = models.CharField(db_column='nombreMedico', max_length=60, blank=True, null=True)  # Field name made lowercase.
    apellidomedico = models.CharField(db_column='apellidoMedico', max_length=60, blank=True, null=True)  # Field name made lowercase.
    fechanacimientomedico = models.DateField(db_column='fechaNacimientoMedico', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'medico'


class Box(models.Model):
    idbox = models.AutoField(db_column='idBox', primary_key=True)  # Field name made lowercase.
    idpasillo = models.ForeignKey('Pasillo', models.DO_NOTHING, db_column='idPasillo', blank=True, null=True)  # Field name made lowercase.
    numerobox = models.IntegerField(db_column='numeroBox', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'box'

class Boximplemento(models.Model):
    idimplemento = models.ForeignKey('Implemento', models.DO_NOTHING, db_column='idImplemento')  # Field name made lowercase.
    idbox = models.ForeignKey(Box, models.DO_NOTHING, db_column='idBox')  # Field name made lowercase.
    idestadoimplemento = models.ForeignKey('Estadoimplemento', models.DO_NOTHING, db_column='idEstadoImplemento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'boximplemento'
        unique_together = (('idimplemento', 'idbox'),)


class Consulta(models.Model):
    idconsulta = models.AutoField(db_column='idConsulta', primary_key=True)  # Field name made lowercase.
    idbox = models.ForeignKey(Box, models.DO_NOTHING, db_column='idBox', blank=True, null=True)  # Field name made lowercase.
    rutpaciente = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='rutPaciente', blank=True, null=True)  # Field name made lowercase.
    rutmedico = models.ForeignKey('Medico', models.DO_NOTHING, db_column='rutMedico', blank=True, null=True)  # Field name made lowercase.
    idestado = models.ForeignKey('Estado', models.DO_NOTHING, db_column='idEstado', blank=True, null=True)  # Field name made lowercase.
    fechaconsulta = models.DateField(db_column='fechaConsulta', blank=True, null=True)  # Field name made lowercase.
    horainicio = models.TimeField(db_column='horaInicio', blank=True, null=True)  # Field name made lowercase.
    horafin = models.TimeField(db_column='horaFin', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'consulta'

