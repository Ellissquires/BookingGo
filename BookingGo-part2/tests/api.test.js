
const request = require('supertest')
const app = require('../index')

describe('API Endpoints', () => {
    it('Should error when parameters missing', async () => {
      const res = await request(app).get('/api/search/?pickup=45,56')
      expect(res.statusCode).toEqual(400)
    })

    it('Should error when no parameters are passed', async () => {
        const res = await request(app).get('/api/search')
        expect(res.statusCode).toEqual(400)
      })

    it('Should error when parameters are in incorrect format', async () => {
        const res = await request(app).get('/api/search/?pickup=45.5,46.8&dropoff=-45.3,45.2&n_passengers=ls -a')
        expect(res.statusCode).toEqual(400)
    })

    it('Should provide a reponse if the params are supplied correctly', async () => {
        const res = await request(app).get('/api/search/?pickup=45.5,46.8&dropoff=-45.3,45.2&n_passengers=4')
        expect(res.statusCode).toEqual(200)
    }, 10000)
  })