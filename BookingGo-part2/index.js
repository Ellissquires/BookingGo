const express = require('express')
const app = express()
const port = 3000
const { exec } = require("child_process")

app.get('/api/search', (req, res) => {
    const pickup = req.query.pickup.split(',')
    const dropoff = req.query.dropoff.split(',')
    const n_passengers = parseInt(req.query.n_passengers)
    let params

    if (!pickup || !dropoff || !n_passengers){
        res.json({"error": "The input is not in the correct format, or something is missing"})

    const [pickup_lat, pickup_lng] = pickup.map(parseFloat)
    const [dropoff_lat, dropoff_lng] = dropoff.map(parseFloat)
    params = `${pickup_lat} ${pickup_lng} ${dropoff_lat} ${dropoff_lng} ${n_passengers}`
    
    
    let script_call = `python TaxiSearch.py search --json -- ${params}`

    const TaxiSearch = exec(script_call, function (error, stdout, stderr) {
        if (error) {
            console.log(error)
            res.status(400)
        } else {
            // Clean stdout by removing all the new lines
            results = JSON.parse(stdout.replace(/\r?\n|\r/g, "").replace(/'/g, '"'))
            res.json(results)
        }
    });

    TaxiSearch.on('exit', function (code) {
        console.log('Child process exited with exit code '+code);
    });

})
app.listen(port, () => console.log(`Example app listening on port ${port}!`))