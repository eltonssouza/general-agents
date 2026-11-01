# Test fixture (own example, not from the book): code with deliberate smells.
def process(self, order, customer, discount, urgent=False):
    if not order:
        return
    # total = calculate(order)
    for item in order.items:
        if item.active:
            if item.price > 1000:
                apply(item, 0.15)
