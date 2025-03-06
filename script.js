document.getElementById("form_convertidor").addEventListener('submit', async function(event) {
	event.preventDefault()
	let amount = document.getElementById("cantidad").value
	let currency = document.getElementById("moneda").value

	const endpoint = "http://127.0.0.1:8000/convertidor"

	const response = await fetch(endpoint, {
		method: "POST",
		headers: {
			"Content-type": "application/json"
		},
		body: JSON.stringify({
			amount: Number(amount),
			to_currency: currency
		})
	})
	let data = await response.json()
})

