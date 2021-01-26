const http = require('http')
const url = require('url')
const fetchMeetup = require('./app')

const server = http.createServer((req, res) => {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write('<h1>Laboratory Works 2</h1>');
    res.write('<form action="events" method="get">');
    res.write('<p>Start Date:</p>');
    res.write('<input name="start_date" type="date">');
    res.write('<p>End Date:</p>');
    res.write('<input name="end_date" type="date">');
    res.write('</br>');
    res.write('<button type="submit">Submit</button>');
    res.write('</form>');
    res.write('<hr />');

    if (req.url.includes('events')) {
        const url_parts = url.parse(req.url, true)
        const query = url_parts.query
        const start_date = query["start_date"] + 'T00:00:00.000'
        const end_date = query["end_date"] + 'T00:00:00.000'
        fetchMeetup.fetchMeetup(start_date, end_date, (err, data) => {
            const events = data.events;
            events.forEach(element => {
                console.log(element.local_date)
                res.write(`<p>${element.name}</p>`);
                res.write(`<p>${element.description}</p>`);
                res.write(`<p>${element.local_date}</p>`);
                res.write(`<p>${element.local_time}</p>`);
                res.write('<hr />');
            })
            res.end()
        })
    } else {
        res.end()
    }
})

const PORT = process.env.PORT || 3000

server.listen(PORT, () => {
    console.log(`Server has been started on ${PORT}...`)
})

