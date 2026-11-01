const mysql = require('mysql')
const connection = mysql.createConnection({})
const id = 223
connection.query('SELECT * FROM todos WHERE id = ' + id, (error, todos) => {
  console.log(todos)
})
connection.query(`SELECT * FROM todos WHERE id = ${id}`, (error, todos, fields) => {
  if (error) throw error
})
connection.query('INSERT INTO todos SET ?', {a: 1}, (error, results) => {
  if (error) throw error
  console.log(results.resultId)
})
setInterval(async () => { await fetch('/x') }, 1000)
const ws = 'ws://example.com/socket'
