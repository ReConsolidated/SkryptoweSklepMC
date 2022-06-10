

fetch("/config")
    .then((result) => { return result.json(); })
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);

            // new
      // Event handler
        document.querySelector("#buy_vip").addEventListener("click", (e) => {
            // Get Checkout Session ID
            e.preventDefault();
            const val = document.querySelector('input').value;
            if (val.length == 0) {
              addError();
              return;
            }
            fetch("/create-checkout-session/vip/" + val)
            .then((result) => {
                return result.json(); })
            .then((data) => {
              // Redirect to Stripe Checkout
              return stripe.redirectToCheckout({sessionId: data.sessionId})
            })
            .then((res) => {
            });
        });

        document.querySelector("#buy_svip").addEventListener("click", (e) => {
            // Get Checkout Session ID
            e.preventDefault();
            const val = document.querySelector('input').value;
            if (val.length == 0) {
              addError();
              return;
            }
            fetch("/create-checkout-session/svip/" + val)
            .then((result) => {
                return result.json(); })
            .then((data) => {
              // Redirect to Stripe Checkout
              return stripe.redirectToCheckout({sessionId: data.sessionId})
            })
            .then((res) => {
            });
        });

        document.querySelector("#buy_mvip").addEventListener("click", (e) => {
            // Get Checkout Session ID
            e.preventDefault();
            const val = document.querySelector('input').value;
            if (val.length == 0) {
              addError();
              return;
            }
            fetch("/create-checkout-session/mvip/" + val)
            .then((result) => {
                return result.json(); })
            .then((data) => {
              // Redirect to Stripe Checkout
              return stripe.redirectToCheckout({sessionId: data.sessionId})
            })
            .then((res) => {
            });
        });

        document.querySelector("#buy_sponsor").addEventListener("click", (e) => {
            // Get Checkout Session ID
            e.preventDefault();
            const val = document.querySelector('input').value;
            if (val.length == 0) {
              addError();
              return;
            }
            fetch("/create-checkout-session/sponsor/" + val)
            .then((result) => {
                return result.json(); })
            .then((data) => {
              // Redirect to Stripe Checkout
              return stripe.redirectToCheckout({sessionId: data.sessionId})
            })
            .then((res) => {
            });
        });
    });