from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, FloatField, FieldList, DateField, \
    Form, ValidationError, FormField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),  Email()], id='input_email')
    password = PasswordField('Пароль', validators=[DataRequired(), Length(4, 64)], id='input_password' )
    remember_me = BooleanField('Запомнить меня', default=False, id='input_remember')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Имя',  validators=[DataRequired(), ], id='input_name')
    email = EmailField('Email', validators=[DataRequired(),  Email() ], id='input_email')
    password1 = PasswordField('Пароль', validators=[InputRequired(), Length(4, 64)], id='input_password1' )
    password2 = PasswordField('Повтор пароля', validators=[InputRequired(), Length(4, 64), EqualTo('password1', message='Пароли не совпадают')], id='input_password2' )

    submit = SubmitField('Зарегистрировать')


class MeasurementInpit(Form):
    ENTRY_TITLE = 'meter_entry_'
    entry = FloatField("", validators=[DataRequired(),])

class MeasurementsForm(FlaskForm):
    date_id = HiddenField('origin date id', default=0)
    date = DateField('дата', validators=[DataRequired(), ], id='measurement-date')
    entries = FieldList(FormField(MeasurementInpit))
    submit = SubmitField('Внести')