from typing import Dict, Optional
import logging

from discord_webhook import DiscordWebhook, DiscordEmbed  # type: ignore

from notifications.plugin import (
    BaseNotificationPlugin,
    ValidationError,
    site,
    FailureAlertContext, PrinterNotificationContext,
    events,
)

LOGGER = logging.getLogger(__name__)


class DiscordNotificationPlugin(BaseNotificationPlugin):
    FAILURE_COLOR = 0xcf142b  # stop red
    HAZZARD_COLOR = 0xEED202  # hazard yellow
    INFO_COLOR = 0x9863F4  # purple, as used on the main website
    OK_COLOR = 0x33a532

    def validate_config(self, data: Dict) -> Dict:
        if 'webhook_url' in data:
            webhook_url = data['webhook_url'].strip()
            return {'webhook_url': webhook_url}
        raise ValidationError('webhook_url key is missing from config')

    def i(self, s: str) -> str:
        return f"_{s}_"

    def b(self, s: str) -> str:
        return f"**{s}**"

    def u(self, s: str) -> str:
        return f"__{s}__"

    @classmethod
    def call_webhook(self, title: str, text: str, color: int, webhook_url: str, image_url: Optional[str] = None):
        webhook = DiscordWebhook(url=webhook_url, username="The Spaghetti Detective")
        embed = DiscordEmbed(title=title, description=text, color=color)
        if image_url:
            embed.set_image(url=image_url)

        embed.set_author(
            name="Click Here to Examine.",
            url=site.build_full_url('/printers/'),
            icon_url="https://github.com/TheSpaghettiDetective/TheSpaghettiDetective/raw/master/frontend/static/img/logo-square.png"
        )
        embed.set_timestamp()
        embed.set_footer(text="The Spaghetti Detective")
        webhook.add_embed(embed)
        webhook.execute()

    def send_failure_alert(self, context: FailureAlertContext, **kwargs) -> None:
        if 'webhook_url' not in context.config:
            return

        color = self.INFO_COLOR

        if context.is_warning and context.print_paused:
            color = self.FAILURE_COLOR
        elif context.is_warning:
            color = self.HAZZARD_COLOR

        text = self.get_failure_alert_text(context=context)
        if not text:
            return

        text = f"Hi {context.user.first_name or ''},\n{text}"

        self.call_webhook(
            title=context.printer.name,
            text=text,
            color=color,
            webhook_url=context.config['webhook_url'],
            image_url=context.print.poster_url,
        )

    def send_printer_notification(self, context: PrinterNotificationContext, **kwargs) -> None:
        if 'webhook_url' not in context.config:
            return

        color = self.event_to_color(event_name=context.event_name)
        text = self.get_printer_notification_text(context=context)
        if not text:
            return

        text = f"Hi {context.user.first_name or ''},\n{text}"

        self.call_webhook(
            title=context.printer.name,
            text=text,
            color=color,
            webhook_url=context.config['webhook_url'],
            image_url=context.print.poster_url
        )

    def event_to_color(self, event_name: str) -> int:
        if event_name in (events.PrintFailed, ):
            return self.FAILURE_COLOR

        if event_name in (events.FilamentChange, ):
            return self.HAZZARD_COLOR

        if event_name in (events.PrintDone, ):
            return self.OK_COLOR

        return self.INFO_COLOR

    def send_test_notification(self, config: Dict, **kwargs) -> None:
        self.call_webhook(
            title='Test Notification',
            text='It works!',
            color=self.OK_COLOR,
            webhook_url=config.get('webhook_url', ''),
            image_url='',
        )


def __load_plugin__():
    return DiscordNotificationPlugin()
