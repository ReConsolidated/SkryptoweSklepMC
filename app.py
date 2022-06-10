import time

import stripe
from flask import Flask, jsonify, render_template, request, redirect

from ShopItems.Battlepass import Battlepass
from ShopItems.Rank import Rank
from database import add_item

app = Flask(__name__)

stripe_keys = {
    "secret_key": 'sk_test_51Jv6IEDfMCRtnfre8bYJKANCzp0eUBeeTFTrTQGcLBAywQVBct0gMdZ8AmcUML'
                  'TOB3A6tj7fj7PKjpWUEF0WAViS00UlLvpITK ',
    "publishable_key": 'pk_test_51Jv6IEDfMCRtnfre4YLHLslh4VHoVnNXuf1gE6HExcNZ1M4QjLJ85N9YTx'
                       'LnuMReLZzfJLBPVRCNQ1NIluRpVamf00EjtKXFEZ',
    "endpoint_secret": 'whsec_63853541d2d4c1d2c7fcb28c702c8d01e1e886ffa47f8a5d191f3975af1cfd60'
}


def current_milli_time():
    return round(time.time() * 1000)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sklep")
def sklep():
    return render_template("index.html")


@app.route("/dc")
def discord():
    return redirect("https://discord.gg/4JHN2smYwJ", code=302)


@app.route("/fb")
def facebook():
    return redirect("https://www.facebook.com/Grypciocraftpl-102822122044565", code=302)


@app.route("/tt")
def facebook():
    return redirect("https://www.facebook.com/Grypciocraftpl-102822122044565", code=302)


@app.route("/karnet")
def battlepass():
    return render_template("battlepass.html")


@app.route("/sukces")
def success():
    return render_template("thankyou.html")


@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


@app.route("/create-checkout-session/<rank_type>/<nickname>")
def create_checkout_session(rank_type, nickname):
    app.logger.warning("name: " + nickname)
    domain_url = "http://127.0.0.1:5000/"
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - capture the payment later
        # [customer_email] - prefill the email input in the form
        # For full details see https://stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        shop_items = [
            Rank("vip", "price_1Jv9lVDfMCRtnfreng2t8Jrd"),
            Rank("svip", "price_1Jv9mADfMCRtnfreRn9Sccug"),
            Rank("mvip", "price_1Jv9mRDfMCRtnfre5nP4Wswf"),
            Rank("sponsor", "price_1L8PlcDfMCRtnfreP5Dea94j"),
            Battlepass()
        ]

        item = None
        for shop_item in shop_items:
            if shop_item.get_name() == rank_type:
                item = shop_item

        if item is None:
            return

        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "sukces",
            cancel_url=domain_url,
            payment_method_types=["card", "p24"],
            mode="payment",
            line_items=[
                {
                    "price": item.get_price_key(),
                    "quantity": 1,
                }
            ],
            metadata={
                "name": nickname,
                "item": item.get_name()
            }
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    app.logger.warning("webhook used!")
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")
        print(event)
        name = event["data"]["object"]["metadata"]["name"]
        email = event["data"]["object"]["customer_details"]["email"]
        time = current_milli_time()
        item = event["data"]["object"]["metadata"]["item"]
        add_item(name, time, email, item)

    return "Success", 200


if __name__ == "__main__":
    app.debug = True
    app.run()
