"""Forms for Edit Profile by Admins. """

from flask_wtf import FlaskForm
from flask_login import current_user
from flask_babelex import lazy_gettext as _
from sqlalchemy.orm.exc import NoResultFound
from flask_security.forms import email_required, email_validator, \
    unique_user_email
from wtforms import FormField, PasswordField, StringField, SubmitField, \
    BooleanField, RadioField
from wtforms.validators import DataRequired, EqualTo, StopValidation, \
    ValidationError, Email

from rapidannotator.models import User
from rapidannotator.validators import USERNAME_RULES, validate_username


def strip_filter(text):
    """Filter for trimming whitespace.

    :param text: The text to strip.
    :returns: The stripped text.
    """
    return text.strip() if text else text

class EditProfileForm(FlaskForm):
    username = StringField(
        label=_('Username'),
        description=_('Required. %(username_rules)s',
                      username_rules=USERNAME_RULES),
        validators=[DataRequired(message=_('Username not provided.'))],
        filters=[strip_filter],
    )

    fullname = StringField(
        label=_('Fullname'),
        filters=[strip_filter],
    )

    email = StringField(
        label=_('Email'),
        validators=[DataRequired(message=_('Email not provided.')), Email()]
    )

    password = PasswordField(
        label=_('Password'),
        validators=[DataRequired(message=_('Password not provided.'))],)
    
    password2 = PasswordField(
        label=_('Confirm Password'),
        validators=[DataRequired(message=_('Confirmation password not provided.')),
                    EqualTo('password')])

    def validate_username(self, username):
        """Wrap username validator for WTForms."""
        try:
            validate_username(username.data)
        except ValueError as e:
            raise ValidationError(_('Invalid Username'))

        user = User.query.filter_by(username=username.data).first()

        if user is not None:
            raise ValidationError(_('Username already taken or earlier Name is Provided!'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Email address already registered.'))
