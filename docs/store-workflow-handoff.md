# Elevated Home — store workflow and next-session handoff

Prepared September 25, 2026. This is a proposed workflow, not a record of completed Shopify or AutoDS configuration. Provider features, plan eligibility, and fees should be checked before subscribing.

## Objective and direction

Build a cohesive, aspirational Shopify home store. The products, photography, descriptions, and room settings should communicate taste, comfort, and success. West Elm is a reference for room-based merchandising and editorial consistency; develop our own identity and imagery.

The eventual catalog target is around 10 products in each of seven sections: Home; Living and Entertainment; Kitchen; Bathroom; Garage; Outdoor Living and Gardens; Seasonal. Only publish sections with enough suitable products. Start production with three complete product pages and a homepage concept before creating the entire catalog.

Proposed visual direction: ivory, oatmeal, walnut, charcoal, and muted olive; linen, wood, plaster, and stone in room settings; soft daylight and warm evening lighting; restrained books, ceramics, and greenery. These are styling references, not claims about product materials.

## Recommended division of work

Use an established app for supplier imports, variant connections, inventory/price monitoring, purchasing, and tracking. Build our AI workflow around branded copy, collection assignment, Higgsfield imagery, and updating the imported Shopify listings.

AutoDS with Fulfilled by AutoDS is the leading candidate because the user wants routine supplier orders placed and paid without manual input. Confirm support for each chosen product, variant, warehouse, and destination before committing.

DSers is an alternative for importing and managing AliExpress products. Its documented AliExpress fulfillment flow still includes manual payment on AliExpress; automatic tracking afterward is not the same as fully automatic purchasing.

Do not have multiple apps automatically order the same Shopify products. Give each product one fulfillment owner to avoid duplicate purchases.

## End-to-end workflow

1. Finalize products and exact supplier variants. Record supplier URL, option combinations, dimensions, actual materials, purchase cost, shipping, destination, delivery estimate, return arrangements, and usable reference photos.
2. Connect Shopify and the selected fulfillment app. Import selected listings as drafts and preserve their supplier/variant connections.
3. Verify every variant mapping and establish pricing rules before publishing.
4. Rewrite titles and descriptions using verified facts and the shared brand voice. Assign collections and consistent product-page sections.
5. Create Higgsfield imagery from actual product references and approved room/style references. Review every image for fidelity.
6. Update the existing Shopify products with approved copy and media. Avoid deleting and recreating variants that the fulfillment app tracks.
7. Configure payments, domain, business email, shipping, applicable taxes, contact information, policies, order emails, and tracking presentation.
8. Run an end-to-end test, including variant selection, payment, supplier order mapping, shipping cost, tracking, and fulfillment status. Any paid supplier test requires an explicit item and spending limit.
9. Publish after review. Monitor exceptions and actual margins even when normal orders are automatic.

Intended routine flow: customer pays in Shopify → eligible order enters AutoDS → supplier purchase is placed and paid within configured limits → supplier ships → tracking and fulfillment information return to Shopify.

## AutoDS requirements and costs

- Fulfilled by AutoDS requires the Orders Processor add-on, appropriate supplier settings, automatic ordering enabled, sufficient Managed Balance, and separate Auto-Order Credits.
- Managed Balance pays supplier costs; order credits pay for automation. A funded balance alone is insufficient.
- Customer payments go to the selling channel. AutoDS does not directly spend those proceeds, so working capital is needed before Shopify payouts arrive.
- The Shopify app listing showed a starting subscription of $26.90/month when researched. This is not the complete price of automation: account for the required plan, add-ons, order credits, supplier costs, shipping, and any other applicable fees.
- The Import 200 entry plan does **not** include price monitoring according to AutoDS documentation. Choose a plan with the required monitoring features.
- Supported supplier status does not guarantee every item, warehouse, destination, or option is eligible.
- The proposed setup must be reconciled with the earlier $100 initial budget; do not assume recurring software and fulfillment float fit that cap.
- Normal orders can be automatic; low funds, unavailable variants, address issues, price limits, cancellations, returns, and other failures can still require intervention.

## Variant handling

Use one Shopify page for the same design in different finishes or sizes. Present substantially different designs grouped inside one AliExpress listing as separate store products if that makes browsing clearer; each still needs its own correct supplier connection.

Example: Amber glass / US plug → the exact supplier Amber glass + US plug variant. Verify all dimensions of the choice: color, size, plug, quantity, accessories, and shipping origin where relevant.

- Import the desired combinations, then use clear option labels such as Finish, Size, and Shade Color.
- Price each variant using its own costs. A small accessory or single item may be the source of the listing's low headline price.
- Assign accurate variant images. Do not show one finish and ship another.
- Restrict electrical variants to versions suitable for the intended US market; verify the actual specifications.
- Recheck mapping after changing option names, SKUs, or variants. Supplier changes can also break mappings.
- If a variant becomes unavailable, stop or flag affected orders. Do not silently substitute a different finish or model.

## Welcome offers, sales, and margin protection

The shopper pays the store's Shopify price. AliExpress welcome discounts do not automatically pass to that shopper. The actual supplier buyer is our account or AutoDS's purchasing account; eligibility depends on that account and the promotion's terms. A new Shopify customer is not a new AliExpress buyer for this purpose.

Base prices on a verified repeat-purchase cost for the exact variant and destination, not an introductory deal or the crossed-out reference price. Treat any eligible temporary savings as extra margin. AutoDS states that it monitors regular retail prices rather than temporary promotions or member-exclusive discounts; verify its imported cost against the actual purchase flow.

Two protections are needed:

1. **Price monitoring and pricing rules:** update prices for future Shopify purchases when monitored supplier costs change.
2. **Order purchase limits:** block automatic supplier purchases above the allowed cost if an order has already been sold at an older price.

Monitoring is periodic, not instantaneous. AutoDS describes multiple scans daily, with changes typically appearing within 1–2 hours. This is not a guaranteed synchronization deadline. A customer can order during the gap. Updating a listing cannot retroactively increase an existing customer's payment.

Example: a lamp sells for $49 and normally costs $22 delivered. If supplier cost increases to $30, repricing can protect future orders. For an existing $49 order, purchase limits determine whether fulfillment proceeds or is blocked for review.

### Pricing configuration and limits

- Include product cost, shipping, applicable purchase taxes/duties, payment/platform fees, automation charges, store discounts, and a reasonable contingency when assessing contribution margin. Account separately for ads, subscriptions, and returns when assessing overall profitability.
- Use the correct supplier region and Ship to Country setting. AutoDS warns that Worldwide does not automatically supply destination-specific shipping costs; begin with a clearly defined destination such as the US.
- Enable price and stock monitoring on an eligible plan, and verify it applies to every intended product/variant.
- Configure profit rules and purchase ceilings; test their meaning with a worked order rather than assuming a label guarantees profit.
- **Maximum loss = $0 does not preserve the original profit.** AutoDS documents a limit based on buy price + calculated order profit + allowed loss. A cost increase can consume expected profit before the order is blocked.
- To preserve a minimum contribution, the allowed supplier spend should be no greater than net order revenue minus other order costs minus the required contribution. Verify how this policy maps to available AutoDS settings; add a custom check only if necessary.
- A blocked purchase does not cancel or refund the Shopify customer automatically. Review it promptly, use a verified equivalent supplier if appropriate, or handle cancellation/refund and customer communication.
- Do not automatically use Force Resend: AutoDS says it bypasses protection settings, including cost and shipping limits.
- Global pricing changes may apply only to new imports. Update and verify existing listings separately. Manual price edits directly in Shopify can be overwritten by AutoDS monitoring.
- Review actual order costs and margins; displayed estimates do not guarantee final profit. Automation reduces risk but cannot guarantee zero losses.

## Higgsfield and cohesive merchandising

Establish three approved product pages first. Use a small library of consistent rooms: living/reading area, kitchen/dining area, bathroom, and outdoor dining setting. Reuse room references, camera treatment, lighting, and color grading so products look like a collection.

Suggested image set per product:

- Clean catalog image with consistent background and crop.
- Lifestyle image showing the actual product in an aspirational room.
- Accurate detail image of finish/construction.
- Scale or dimensions image based on verified measurements.
- Functional image where helpful, such as lighting switched on.

For variants, keep the room and composition consistent while accurately representing the selected variant. Review generated geometry, finish, scale, cords, controls, accessories, and light output. Retain accurate supplier photographs where generation cannot preserve details. Confirm image-use rights; importing a supplier image does not itself grant permission. Do not describe materials or performance from AI imagery.

Suggested homepage sequence: room hero → featured collection → shop by room → selected products → styled room with Shop the Look → brand story. Product pages should share the same layout for benefits, specifications, care, shipping, and returns.

## Next-session checklist

- [ ] Confirm store URL, current setup, and working budget for subscriptions and fulfillment funds.
- [ ] Select three initial products and the exact variants to offer.
- [ ] Verify normal supplier checkout costs and US delivery, excluding welcome offers.
- [ ] Confirm AutoDS eligibility and the full price of the required plan/add-ons.
- [ ] Import three products as drafts and verify every variant mapping.
- [ ] Configure and test monitoring, fees, shipping assumptions, and order purchase limits.
- [ ] Approve a visual style guide and a small set of room references.
- [ ] Produce and review the first Higgsfield image sets and product copy.
- [ ] Complete the homepage concept and three product pages.
- [ ] Test checkout and the supplier fulfillment path before launch.

## Existing research

- `research/script-expanded-candidates-live.json`: finder output containing 324 rows / 297 unique ASINs. These are demand references, not confirmed dropshipping suppliers.
- `research/elevated-home-sample-review.md`: four identified AliExpress samples and related finder candidates.
- `research/jina-samples/`: retrieved AliExpress pages; several are CAPTCHA responses. Only four of the ten supplied examples were identified, and their product images were not visually verified.
- `docs/launch-checklist.md`: existing launch checklist; this document supplements it and does not mark tasks complete.

## Sources consulted

- [AutoDS Shopify listing and subscription pricing](https://apps.shopify.com/autods)
- [Fulfilled by AutoDS setup, suppliers, funding, and failures](https://help.autods.com/en/articles/12700443-automate-your-orders-with-fulfilled-by-autods-fba)
- [AutoDS price and stock monitoring; plan eligibility](https://help.autods.com/en/articles/12699906-product-monitoring-configure-price-and-stock-updates-preferences)
- [AutoDS pricing, fees, promotions, and shipping assumptions](https://help.autods.com/en/articles/12699821-pricing-settings-and-fee-management-in-autods)
- [AutoDS order limits and protection overrides](https://help.autods.com/en/articles/12700454-orders-page-settings-navigation-statuses-edit-filter-and-troubleshoot)
- [AutoDS product imports and variants](https://help.autods.com/en/articles/12700438-product-uploads-supported-suppliers-import-to-store-and-manage-variants)
- [AutoDS Shopify integration and price overrides](https://help.autods.com/en/articles/12699781-shopify-store-connect-build-and-optimize-your-store-with-autods)
- [DSers Shopify app](https://apps.shopify.com/dsers)
- [DSers supplier ordering and manual payment](https://help.dsers.com/fulfilling-customer-orders-how-to-place-pay-for-supplier-orders/)
- [DSers variant mapping](https://help.dsers.com/how-variant-mapping-works/)
- [DSers mapping failures after supplier changes](https://help.dsers.com/sku-changes-notification-what-to-do-when-variant-mapping-fails/)
- [Shopify variants](https://help.shopify.com/en/manual/products/variants/add-variants)
- [Shopify launch checklist](https://help.shopify.com/en/manual/intro-to-shopify/initial-setup/new-to-shopify-checklists/general-checklist)
- [Higgsfield product photography workflow](https://console.higgsfield.ai/models/workflows/product-shots/playground)
