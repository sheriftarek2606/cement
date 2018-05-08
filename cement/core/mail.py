"""Cement core mail module."""

from abc import abstractmethod
from ..core.handler import Handler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class MailHandlerBase(Handler):

    """
    This class defines the Mail Handler Interface.  Classes that
    implement this interface must provide the methods and attributes defined
    below.

    **Configuration**

    Implementations must support the following configuration settings:

     * **to** - Default ``to`` addresses (list, or comma separated depending
       on the ConfigHandler in use)
     * **from_addr** - Default ``from_addr`` address
     * **cc** - Default ``cc`` addresses (list, or comma separated depending
       on the ConfigHandler in use)
     * **bcc** - Default ``bcc`` addresses (list, or comma separated depending
       on the ConfigHandler in use)
     * **subject** - Default ``subject``
     * **subject_prefix** - Additional string to prepend to the ``subject``

    **Usage**

    .. code-block:: python

        from cement.core.mail import MailHandlerBase

        class MyMailHandler(object):
            class Meta:
                label = 'my_mail'
            ...

    """

    class Meta:

        """Handler meta-data."""

        interface = 'mail'
        """The label identifier of the interface."""

    @abstractmethod
    def send(self, body, **kwargs):
        """
        Send a mail message.  Keyword arguments override configuration
        defaults (cc, bcc, etc).

        Args:
            body (str): The message body to send

        Keyword Args:
            to (list): List of recipients (generally email addresses)
            from_addr (str): Address (generally email) of the sender
            cc (list): List of CC Recipients
            bcc (list): List of BCC Recipients
            subject (str): Message subject line

        Returns:
            bool: ``True`` if message was sent successfully, ``False``
            otherwise

        Example:

            .. code-block:: python

                # Using all configuration defaults
                app.mail.send('This is my message body')

                # Overriding configuration defaults
                app.mail.send('My message body'
                    to=['john@example.com'],
                    from_addr='me@example.com',
                    cc=['jane@example.com', 'rita@example.com'],
                    subject='This is my subject',
                    )

        """
        pass  # pragma: nocover


class MailHandler(MailHandlerBase):

    """Mail handler implementation."""

    class Meta:

        """
        Handler meta-data (can be passed as keyword arguments to the parent
        class).
        """

        #: Configuration default values
        config_defaults = {
            'to': [],
            'from_addr': 'noreply@example.com',
            'cc': [],
            'bcc': [],
            'subject': 'Default Subject Line',
            'subject_prefix': '',
        }

    def _setup(self, app_obj):
        super()._setup(app_obj)
        self._validate_config()

    def _validate_config(self):
        # convert comma separated strings to lists (ConfigParser)
        for item in ['to', 'cc', 'bcc']:
            if item in self.app.config.keys(self._meta.config_section):
                value = self.app.config.get(self._meta.config_section, item)

                # convert a comma-separated string to a list
                if type(value) is str:
                    value_list = value.split(',')

                    # clean up extra space if they had it inbetween commas
                    value_list = [x.strip() for x in value_list]

                    # set the new extensions value in the config
                    self.app.config.set(self._meta.config_section, item,
                                        value_list)
