const fastify = require('fastify')({ logger: true })
const fastifyPlugin = require('fastify-plugin')

async function dbConnector (fastify, options) {
  fastify.decorate('db', {})
}

fastify.post('/', async (request, reply) => {
  return request.body
})

fastify.listen({ port: 3000 }, function (err, address) {
  if (err) {
    fastify.log.error(err)
    process.exit(1)
  }
})
