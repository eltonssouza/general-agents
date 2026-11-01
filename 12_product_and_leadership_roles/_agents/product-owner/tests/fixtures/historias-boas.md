# Fixture de teste (exemplo próprio): histórias bem formadas.

### História 1: Aplicar cupom de desconto
**Como** cliente da loja, **quero** aplicar um cupom no carrinho, **para** pagar menos na compra.

**Cenário:** cupom válido
- **Dado** um carrinho com total de R$ 100,00
- **Quando** aplico o cupom "DEZ" de 10%
- **Então** o total passa a R$ 90,00

**Cenário:** cupom expirado
- **Dado** um cupom "VELHO" vencido em 2026-01-01
- **Quando** aplico o cupom no carrinho
- **Então** vejo a mensagem "Cupom expirado" e o total não muda
