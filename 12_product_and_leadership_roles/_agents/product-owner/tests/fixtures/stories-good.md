# Test fixture (own example): well-formed stories.

### Story 1: Apply a discount coupon
**As a** store customer, **I want** to apply a coupon to the cart, **so that** I pay less on the purchase.

**Scenario:** valid coupon
- **Given** a cart totaling R$ 100.00
- **When** I apply the coupon "TEN" for 10%
- **Then** the total becomes R$ 90.00

**Scenario:** expired coupon
- **Given** a coupon "OLD" that expired on 2026-01-01
- **When** I apply the coupon to the cart
- **Then** I see the message "Coupon expired" and the total does not change
