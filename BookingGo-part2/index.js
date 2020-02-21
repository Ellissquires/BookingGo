const express = require('express')
const app = express()
const port = 3000
const { exec } = require("child_process")

app.get('/api/search', (req, res) => {
    // Retrieve query params
    let pickup = req.query.pickup.split(',')
    let dropoff = req.query.dropoff.split(',')
    let n_passengers = parseInt(req.query.n_passengers)

    // Check if any off the parameters are missing
    if (!pickup || !dropoff || !n_passengers){
        return res.json({"error": "Something is missing from the input"})
    } 

    // Parse inputs into floats
    pickup = pickup.map(parseFloat)
    dropoff = dropoff.map(parseFloat)

    // Check if any off the location paramaters are invalid (NaN)
    if (pickup.concat(dropoff).filter(isNaN).length > 0){
        return res.json({"error": "The input is not in the correct format"})
    }

    // Assigning individual location components
    const [pickup_lat, pickup_lng] = pickup 
    const [dropoff_lat, dropoff_lng] = dropoff
    const params = `${pickup_lat} ${pickup_lng} ${dropoff_lat} ${dropoff_lng} ${n_passengers}`

    // Python script call definition with sanitised paramaters
    let script_call = `python TaxiSearch.py search --json -- ${params}`

    // Executing the script returning the stdout as JSON
    const TaxiSearch = exec(script_call, function (error, stdout, stderr) {
        if (error) {
            console.log(error)
            res.status(400)
        } else {
            // Clean stdout by removing all the new lines
            results = JSON.parse(stdout.replace(/\r?\n|\r/g, "").replace(/'/g, '"'))
            return res.json(results)
        }
    })

    TaxiSearch.on('exit', function (code) {
        console.log('Child process exited with exit code '+code);
    })
})
app.listen(port, () => console.log(`TaxiSearch API listening on port ${port}`))