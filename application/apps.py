from django.apps import AppConfig
from django.db.models.signals import pre_save


class ApplicationConfig(AppConfig):
    name = 'application'

    def register_timeline_log_signals(self):
        """
        Register signals for tracking changes to models.
        These changes can then be captured by the TimlineLog model.
        :return: None
        """
        # Imports must stay here. If you put it outside of this class it will fail.
        # Because this app is loaded on when it reaches ready() method.
        # Any interaction with django will fail before this class
        from application.signals import timeline_log_pre_save

        model_to_register = self.get_model('NannyApplication')

        # XXX: Ensure dispatch_uid declared to prevent duplicate logs being created.
        pre_save.connect(timeline_log_pre_save, sender=model_to_register, dispatch_uid="timeline_log_pre_save")


    def ready(self):
        self.register_timeline_log_signals()
