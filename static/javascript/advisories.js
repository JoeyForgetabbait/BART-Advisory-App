d3.json('./api/v1.0/advisories').then(function (response) {
	var advisories_text = '<table><thead><th>Time</th><th>Description</th></thead><tbody>';
	for (let i = 0; i < response.length; i++) {
		advisories_text += `<tr><td>${response[i]['Time']}</td><td>${response[i]['Description']}</td></tr>`
	}
	advisories_text += '</tbody></table>'
	d3.select('#pie').html(advisories_text);
})

