const express = require('express')
const session = require('express-session')
const fs = require('fs')
const { check, validationResult } = require('express-validator')
const app = express()
app.set('view engine', 'pug')
app.use(express.json())
app.use(session({ secret: 'change-in-production', store: undefined }))

app.use((req, res, next) => {
  req.start = Date.now()
  next()
})

app.post('/form', [check('name').isLength({ min: 3 })], (req, res) => {
  const errors = validationResult(req)
  if (!errors.isEmpty()) {
    return res.status(422).json({ errors: errors.array() })
  }
  res.render('about', { name: req.body.name })
})

fs.readFile('/tmp/a.txt', (err, data) => {
  if (err) { console.error(err); return }
  console.log(data)
})

const server = app.listen(3000, () => console.log('Server ready'))
process.on('SIGTERM', () => { server.close() })
