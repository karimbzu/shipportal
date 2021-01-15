// static/main.js

console.log("Sanity check!");

function isEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

// Get Stripe publishable key
fetch("/user/config/")
    .then((result) => {
        return result.json();
    })
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);

        // new
        // Event handler
        document.querySelector("#submitBtn").addEventListener("click", () => {


            // Get Checkout Session ID
            fetch("/user/create-checkout-session/")
                .then((result) => {
                    return result.json();
                })
                .then((data) => {
                    console.log(data);
                    // Redirect to Stripe Checkout
                    return stripe.redirectToCheckout({sessionId: data.sessionId})
                })
                .then((res) => {
                    console.log(res);
                });

        });

    });