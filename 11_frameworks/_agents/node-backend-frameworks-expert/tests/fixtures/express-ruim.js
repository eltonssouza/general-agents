const express = require('express')
const session = require('express-session')
const fs = require('fs')
const app = express()

app.get('/', (req, res) => res.send('Hello World!'))

app.use(session({ resave: false }))

app.use((req, res, next) => {
  req.start = Date.now()
})

app.post('/form', (req, res) => {
  const name = req.body.name
  const data = fs.readFileSync('./big.txt', 'utf8')
  res.render('about', { name, data })
})

app.get('/file', (req, res) => {
  fs.readFile('./data.txt', (err, data) => {
    res.end(data)
  })
})

const stats = fs.stat('/tmp/a.txt')
const p = Promise((resolve) => resolve(1))
app.listen(3000, () => console.log('Server ready'))
process.exit(1)
