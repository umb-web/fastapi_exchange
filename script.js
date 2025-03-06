document.getElementById("exchange_form").addEventListener('submit', async function(event) {
	event.preventDefault();

	let amount = document.getElementById("amount").value;
	let current_currency = document.getElementById("current_currency").value;
	let destinated_currency = document.getElementById("destinated_currency").value;

	const endpoint = "http://127.0.0.1:8000/exchange_currency";

	try {
		const response = await fetch(endpoint, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({
				"amount": Number(amount),
				"from_currency": current_currency,
				"to_currency": destinated_currency
			})
		});

		if (!response.ok) {
			throw new Error(`error exchanging: ${response.status} ${response.statusText}`);
		}

		let data = await response.json();
		console.log(data)
		const result = document.getElementById("result_p")
		result.innerHTML = `${data.total} ${destinated_currency}`


	} catch (error) {
		console.error("problem with exchange", error);
	}
});

