async function dbConnector (fastify, options) {
  fastify.decorate('db', {})
}
module.exports = dbConnector
