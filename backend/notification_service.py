import json
import logging
from datetime import datetime
from pathlib import Path
from threading import Lock

try:
    from pywebpush import webpush, WebPushException
except Exception:
    webpush = None
    WebPushException = Exception


class NotificationService:
    """
    Production-ready notification manager.

    Supports:
    - Duplicate filtering
    - Priority filtering
    - Persistent subscriptions
    - Web Push
    - Future Telegram / Discord / Email adapters
    """

    def __init__(self):

        self.last_notifications = {}

        self.lock = Lock()

        self.subscription_file = (
            Path(__file__).parent /
            "subscriptions.json"
        )

        self.subscriptions = []

        self.vapid_private_key = None
        self.vapid_claims = {
            "sub": "mailto:admin@example.com"
        }

        self.load_subscriptions()

    # --------------------------------------------------

    def load_subscriptions(self):

        if not self.subscription_file.exists():
            self.subscriptions = []
            return

        try:
            self.subscriptions = json.loads(
                self.subscription_file.read_text(
                    encoding="utf8"
                )
            )
        except Exception:
            self.subscriptions = []

    # --------------------------------------------------

    def save_subscriptions(self):

        self.subscription_file.write_text(
            json.dumps(
                self.subscriptions,
                indent=4
            ),
            encoding="utf8"
        )

    # --------------------------------------------------

    def add_subscription(self, subscription):

        with self.lock:

            if subscription not in self.subscriptions:

                self.subscriptions.append(subscription)

                self.save_subscriptions()

    # --------------------------------------------------

    def remove_subscription(self, subscription):

        with self.lock:

            if subscription in self.subscriptions:

                self.subscriptions.remove(subscription)

                self.save_subscriptions()

    # --------------------------------------------------

    def should_notify(self, signal):

        if not signal.get("status", False):
            return False

        confidence = signal.get("confidence", 0)

        if confidence < 85:
            return False

        if signal.get("signal") not in (
            "BUY",
            "SELL",
            "STRONG BUY",
            "STRONG SELL"
        ):
            return False

        key = (
            f"{signal['symbol']}_"
            f"{signal['timeframe']}"
        )

        previous = self.last_notifications.get(key)

        if previous == signal["signal"]:
            return False

        self.last_notifications[key] = signal["signal"]

        return True

    # --------------------------------------------------

    def build_payload(self, signal):

        return {

            "title":
                f"{signal['symbol']} "
                f"{signal['signal']}",

            "body":
                (
                    f"AI {signal['confidence']}% | "
                    f"Entry {signal['entry']} | "
                    f"SL {signal['stop_loss']} | "
                    f"TP1 {signal['take_profit_1']}"
                ),

            "icon": "/icons/icon-192.png",

            "badge": "/icons/icon-192.png",

            "url":
                (
                    "/?symbol="
                    f"{signal['symbol']}"
                ),

            "timestamp":
                datetime.utcnow().isoformat(),

            "signal": signal

        }

    # --------------------------------------------------

    def send_web_push(self, payload):

        if webpush is None:
            return

        if self.vapid_private_key is None:
            return

        dead = []

        for sub in self.subscriptions:

            try:

                webpush(
                    subscription_info=sub,
                    data=json.dumps(payload),
                    vapid_private_key=self.vapid_private_key,
                    vapid_claims=self.vapid_claims
                )

            except WebPushException:

                dead.append(sub)

            except Exception:

                logging.exception(
                    "Web push failed."
                )

        if dead:

            for d in dead:

                if d in self.subscriptions:

                    self.subscriptions.remove(d)

            self.save_subscriptions()

    # --------------------------------------------------

    def send_console(self, payload):

        print()

        print("=" * 70)

        print(payload["title"])

        print(payload["body"])

        print("=" * 70)

        print()

    # --------------------------------------------------

    def send(self, signal):

        payload = self.build_payload(signal)

        logging.info(
            "%s | %s",
            payload["title"],
            payload["body"]
        )

        self.send_console(payload)

        self.send_web_push(payload)

        return payload

    # --------------------------------------------------

    def process(self, signal):

        if not self.should_notify(signal):
            return None

        return self.send(signal)


notification_service = NotificationService()