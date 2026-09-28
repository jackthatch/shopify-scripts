# Launch setup - shipping, policies, domain
Generated 2026-09-28

## What the API cannot do
Token scopes are: read/write_products, read/write_inventory, read_orders, read/write_themes.
There is **no shipping, content, discount or file scope**, so shipping rates and store
policies must be set by hand in the admin. Not a bug - a permissions limit.

## 1. Shipping rates  (Settings > Shipping and delivery)
Live state read from the API:
- Zone "Domestic" (United States) - **0 rates**
- Zone "Rest of World" - **0 rates**
Until a rate exists in the Domestic zone, checkout cannot complete.

In the **Domestic** zone, add TWO rates:

| Rate name | Price | Condition |
|---|---|---|
| Standard | 7.99 | none |
| Free shipping at $75 or more | 0.00 | Order total **is greater than or equal to** 75 |

The boundary is **inclusive**: $75.00 exactly gets free shipping. In Shopify's rate
condition builder that is the "is greater than or equal to" operator, not "is greater
than" - pick the wrong one and a $75.00 order is charged $7.99.

Shopify offers the cheapest rate an order qualifies for, so a $40 order gets the $7.99
rate and an $80 order gets free shipping. Set a delivery estimate of `7-15 business days`
on both.

Then deal with the **Rest of World** zone: we ship US only, so either delete it or leave
it empty. An empty zone means no shipping option is offered, which is the correct
behaviour - but check the storefront shows it that way rather than erroring.

## 2. Policies  (Settings > Policies)
Paste each file into the matching field:
- `01-refund-policy.md`    -> Refund policy
- `02-shipping-policy.md`  -> Shipping policy
- `03-terms-of-service.md` -> Terms of service
- Privacy policy already exists (Shopify default, 18.3k chars)

The support email is already set to `hello@sundayform.store` throughout, and the governing-law
clause is already set to Alabama - **check that Alabama is correct for your LLC/registration
state before publishing**, and change it if not.
Shopify also has an "Insert template" button per policy - faster, but generic, and it
does not reflect 7-15 day fulfilment or a US-only shipping area.

## 3. Domain
Taken by others: sundayform.com, sundayform.co, sundayform.co.uk.
Verified AVAILABLE 2026-09-28:
- sundayformhome.com      <- recommended
- getsundayform.com
- sundayformliving.com
- sundayformgoods.com / sundayformhouse.com / shopsundayform.com
- sundayform.store / .shop / .us / .studio

Buy it inside Shopify (Settings > Domains > Buy new domain). A Shopify-managed domain
connects itself, provisions SSL, and makes Meta/Google domain verification one click.
An external registrar needs manual DNS. Set it as the primary domain afterwards so the
myshopify URL redirects.

## 4. Shipping price reality check
With $7.99 flat under $75, here is the uplift on the top-priced variant of each product:

| Product | Price | +ship | Uplift |
|---|---|---|---|
| Sunset LED Table Lamp | 11.00 | 18.99 | +73% |
| Tyst Alarm Clock | 14.46 | 22.45 | +55% |
| Stoneware Tea Cup | 17.80 | 25.79 | +45% |
| Silicone Coasters | 23.80 | 31.79 | +34% |
| Heion Rice Paper Lamp | 29.99 | 37.98 | +27% |
| Gradient Coasters (set) | 34.99 | 42.98 | +23% |
| Mushroom Night Light | 44.99 | 52.98 | +18% |
| Retro Glass Chandelier | 59.99 | 67.98 | +13% |

**No single item in the catalogue reaches $75** (the only exception is a $242 variant of
the garden wall lamp). So free shipping requires a basket, and almost all of that basket
has to be two items.

The chandelier at $67.98 is $7.02 short - a customer at that point is one coaster away
from free shipping, which is a genuinely good AOV lever.

**The risk is at the bottom of the range.** $7.99 added to a $9.99 or $11.00 product is a
45-73% price increase at the exact moment paid traffic lands. Recommendation: point ads
at the $34.99 coaster set or the $59.99 chandelier, not the single $9.99 coasters, where
the same $7.99 is only 13-23%.
