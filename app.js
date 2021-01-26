const fetch = require("node-fetch")

const fetchMeetup = (start_date, end_date, callback) => {
    fetch(`https://api.meetup.com/find/upcoming_events?start_date_range=${start_date}&end_date_range=${end_date}&lat=37.77&lon=-122.41&text=games`, {
        headers: {
            'Authorization' : 'Bearer e59b286b6db877e677c6f5ed0fba3f71',
            'Origin' : 'http://localhost:3000/'
        },
        credentials: 'include',
    })
        .then(
            function(response) {
                if (response.status !== 200) {
                    console.log('Looks like there was a problem. Status Code: ' +
                        response.status)
                }
                // Examine the text in the response
                response.json().then(function(data) {
                    callback(null, data)
                });
            }
        )
        .catch(function(err) {
            console.log('Fetch Error :-S', err)
        });
}
module.exports.fetchMeetup = fetchMeetup
