// Function to handle response and parse JSON
function handleResponse(response) {
    if (!response.ok) {
        return response.json().then(err => {
            throw new Error(err.error || 'Payment failed');
        }).catch(() => {
            throw new Error('Server returned an invalid response.');
        });
    }
    return response.json();
}

// Function to get CSRF Token
function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : null;
}


function handleError(error) {
    console.error('Error:', error);
    alert(error.message || 'Payment processing failed');
    resetButtons();
}

function handleStripeError() {
    alert('Failed to load payment processor. Please refresh the page.');
    resetButtons();
}

function resetButtons() {
    document.querySelectorAll('.btn-select').forEach(btn => {
        btn.disabled = false;
        btn.innerHTML = btn.dataset.originalText || 'Select Plan';
    });
}




async function initiateCheckout(planId) {
  const input = document.querySelector(`input[name="plan_id"][value="${planId}"]`);
  if (!input) return alert("Plan not found.");


  const form = input.closest('form');

    console.log('POST body:', new URLSearchParams(new FormData(form)).toString());
  const button = form.querySelector('button');

  button.disabled = true;
  button.textContent = 'Processing...';

  try {
    const response = await fetch(window.CHECKOUT_SESSION_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: new URLSearchParams(new FormData(form))
    });

    const data = await response.json();

    if (!response.ok || data.error) {
      throw new Error(data.error || 'Checkout failed.');
    }

    const result = await stripe.redirectToCheckout({
      sessionId: data.sessionId || data.id
    });

    if (result.error) {
      throw new Error(result.error.message);
    }
  } catch (error) {
    console.error(error);
    alert('Error: ' + error.message);
    button.disabled = false;
    button.textContent = button.dataset.originalText || 'Try Again';
  }
}


// Store original button text
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.btn-select').forEach(button => {
    button.dataset.originalText = button.textContent;
  });
});


async function testAsync() {
  const response = await fetch('https://jsonplaceholder.typicode.com/todos/1');
  const data = await response.json();
  console.log(data);
}

testAsync();



window.initiateCheckout = initiateCheckout;



