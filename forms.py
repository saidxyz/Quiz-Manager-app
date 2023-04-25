#from wtforms import Form, BooleanField,StringField, SubmitField, validators
#from wtforms.validators import DataRequired, Email, Length
#from wtforms.fields import TextAreaField, HiddenField, EmailField, PasswordField
#
#class UsersForm(Form):
#    id = HiddenField()
#    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
#    first_name = StringField('First Name', validators=[DataRequired()])
#    last_name = StringField('Last Name', validators=[DataRequired()])
#    password = PasswordField('Password', validators=[DataRequired()])
#    submit = SubmitField('Login')