# Shopify launch checklist

Working plan for the `shopify-scripts` project. Prepared September 25, 2026.

**Order:** validate products → verify suppliers and margins → create the brand and images → build the Shopify store → verify tracking → launch ads → improve and scale.

The store scope is **indoor lighting, home furniture, and accessories**, including chairs, tables, organization, and mirrors. Positioning is **warm and upscale**, presenting an aspirational, lavish home lifestyle to US customers with discretionary spending power. Start research broadly, then propose **3–5 cohesive launch products** and **one priority product** for the initial $100 validation phase. These are planning targets, not validated winners. The live research pipeline still needs a fresh run.

## 1. Set the scope and budget

- [x] Choose the initial country and currency: **United States, USD**.
- [x] Set the broad customer direction: customers with money to spend on an upscale home and lifestyle.
- [x] Set the category scope: **indoor lighting, home furniture, and accessories**, including chairs, tables, organization, and mirrors.
- [x] Set the style: **warm, upscale, and aspirational**, selling a lavish home lifestyle through the collection.
- [x] Set the sampling policy: **no product samples**.
- [x] Set the maximum initial validation spend: **$100 total**.
- [ ] Refine the first collection around one room or styling use case within this broader scope.
- [ ] Record actual tool/store costs and fit spending within the allocation below before purchasing.

### Working budget allocation

Treat $100 as the total initial validation cap, including new setup costs. Existing paid subscriptions may be reused without allocating a new purchase. These are spending ceilings, not quoted service prices or money already spent.

| Category | Allocation | Use |
| --- | ---: | --- |
| Samples | $0 | User decision; use supplier evidence instead |
| Store, domain, and tools | $30 | Essential setup only, after checking actual charges |
| Creative production | $0 | Authorized supplier media and existing/free image-generation access |
| Initial advertising experiment | $40 | One priority product; release only after launch checks pass |
| Fulfillment/refund contingency | $30 | Hold unspent; not an advertising budget |
| **Total** | **$100** | **Do not exceed the cap** |

If setup or creative costs exceed their allocations, reduce or defer advertising instead of exceeding $100. Do not assume a new Higgsfield subscription or a public Shopify launch fits the setup allowance. A $40 advertising experiment can provide directional evidence but cannot establish repeatable profitability. Begin with research, a small creative set, and organic interest checks; paid advertising is conditional on readiness and available funds.

Before accepting orders, confirm that supplier payments can be funded while customer payouts are pending and that refunds can be covered. The $30 contingency is not a guarantee that this cash requirement is met, especially for furniture.

**Completion gate:** a one-page brief describing what we sell, to whom, and the test budget.

## 2. Explore products and build a shortlist

- [ ] Run `find_products.py` across relevant lighting, furniture, home-decor, and storage categories supported by the script.
- [ ] Run `search_intent.py` for search phrases and trend signals.
- [ ] Run `price_products.py --mode high-ticket` for preliminary pricing.
- [ ] Review approximately 20–30 candidates manually.
- [ ] Check competing Google Shopping listings: prices, images, shipping promises, reviews, and positioning.
- [ ] Record supplier links, exact variants, competitor prices, demand evidence, and differentiation in one research tracker.
- [ ] Shortlist 3–5 cohesive products with credible demand and a clear reason to buy from our store; select one priority product.
- [ ] Evaluate chairs, tables, and mirrors for shipping cost, damage exposure, and return cost before including them in the initial test.

Treat the scripts as screening tools. Autocomplete volume and Amazon reviews alone do not establish purchase intent or profitability.

**Completion gate:** each shortlisted product has evidence supporting its demand, pricing, and proposed angle.

## 3. Verify supplier evidence and actual economics

- [ ] Compare at least two suppliers for priority products.
- [ ] Confirm exact variant, materials, dimensions, inventory, packaging, tracking, and delivery times.
- [ ] For lighting, verify plug/voltage compatibility, installation requirements, and applicable product documentation for the intended market.
- [ ] Confirm damaged-item replacements, return arrangements, and permission to use supplier media.
- [ ] Obtain current photos and videos of the exact variant, including details, assembly, and packaging, without ordering samples.
- [ ] Review recent buyer feedback and delivery evidence; record supplier delivery promises separately from independently corroborated information.
- [ ] Record unresolved quality and delivery uncertainties: these products have not been physically inspected by us.
- [ ] Calculate costs using the exact selected variant rather than the lowest advertised “from” price.
- [ ] Establish a target customer acquisition cost for each product.

**Break-even acquisition cost = selling price − product cost − shipping/import costs − payment fees − expected returns/replacements − other variable costs.**

Target acquisition cost must leave room for profit and overhead. The documented 5–10× markup is a screening hypothesis; it does not establish what buyers will pay.

**Completion gate:** supplier evidence is adequate to support accurate listings, uncertainties are recorded, and economics support a limited test. This is a document/media review, not physical product validation.

## 4. Define the brand and creative direction

- [ ] Choose the store name, domain, and support email.
- [ ] Define colors, fonts, writing tone, and a consistent photography style.
- [ ] Write the main customer promise using substantiated benefits.
- [ ] Create a visual reference board for rooms, backgrounds, lighting, and composition.
- [ ] Establish folders and asset naming that link every image to its SKU and variant.

**Completion gate:** a reusable brand direction for consistent pages and images.

## 5. Create tailored images with Higgsfield or a similar tool

Higgsfield offers reference-photo workflows for studio, lifestyle, and detail images. Test the workflow on authorized reference photos of one selected product before expanding. Use existing/free access initially; any new paid generation must be funded within the $100 cap. See [Higgsfield product photography](https://higgsfield.ai/ai-product-photography).

- [ ] Obtain authorized supplier photos from multiple angles for the exact selected variant.
- [ ] Build a reusable prompt specifying product, room, lighting, camera composition, and details that must remain unchanged.
- [ ] Produce a clean main product image.
- [ ] Produce 2–3 lifestyle images showing credible room placement and scale.
- [ ] Add real detail photographs and an accurate dimensions graphic.
- [ ] Create images for each actual variant.
- [ ] Prepare square, vertical, and landscape crops for the store and advertising.
- [ ] Compare every generated image against supplier reference photos, videos, and specifications: shape, finish, cord, switches, proportions, and included accessories. Do not invent unseen features or describe the product as personally tested.
- [ ] Preserve required AI metadata through editing and export.

Plan for Google's image requirements and AI-content handling from the start. AI-generated images require identifying metadata; AI-generated feed titles and descriptions have dedicated structured attributes. See [Google image requirements](https://support.google.com/merchants/answer/6324350?hl=en) and [AI-generated content](https://support.google.com/merchants/answer/14743464).

**Completion gate:** each launch product has an approved image set that accurately represents what customers receive.

## 6. Write listings and assemble the Shopify website

- [ ] Set up Shopify, the domain, business details, payment processing, shipping, and tax settings.
- [ ] Select and customize a theme around the visual direction.
- [ ] Build the homepage, collections, product pages, About, Contact, FAQ, shipping, and returns pages.
- [ ] Write each listing with a clear title, benefits, verified specifications, dimensions, included items, installation details, and delivery expectations.
- [ ] Add accurate variants, SKU mapping, prices, stock availability, and supplier fulfillment connections.
- [ ] Include verified lighting details such as bulb requirements, dimming compatibility, and color temperature.
- [ ] Optimize images and check the complete mobile buying experience.
- [ ] Add genuine reviews when available.

See the [Shopify launch checklist](https://help.shopify.com/en/manual/intro-to-shopify/initial-setup/new-to-shopify-checklists/general-checklist) for store configuration, policies, and test orders.

**Completion gate:** a customer can understand the product, delivery promise, and return terms, then complete checkout easily.

## 7. Connect measurement, Google listings, and retention

- [ ] Set up Google Merchant Center, Google Ads, GA4, and Search Console.
- [ ] Verify the domain and connect the product feed.
- [ ] Check that feed prices, availability, variants, shipping, and return information match the website.
- [ ] Resolve Merchant Center account issues and product disapprovals.
- [ ] Configure purchase tracking with correct order value and currency.
- [ ] Check that a purchase is counted once, with an appropriate primary conversion for bidding.
- [ ] Configure consent/privacy controls appropriate to the target market.
- [ ] Set up order updates, welcome emails, abandoned-checkout messages, and post-purchase support.
- [ ] Test checkout, cancellation, and refund flows in test mode; verify supplier mapping and tracking-notification setup without placing an unintended supplier order.
- [ ] Document that physical fulfillment and delivery remain untested under the no-samples policy.

Google requires a functional purchasing experience with clear purchase conditions. Accurate transaction values also help advertising optimization. See [Merchant website requirements](https://support.google.com/merchants/answer/12160471?hl=en) and [measurement guidance](https://support.google.com/google-ads/answer/13776350?hl=en).

**Completion gate:** products are eligible to advertise, purchases are measured correctly, and checkout/integration checks pass. Physical delivery remains unverified until actual fulfillment occurs.

## 8. Prepare and launch the first marketing test

- [ ] Choose the initial paid campaign approach: Standard Shopping or Performance Max.
- [ ] Start with one priority product for the United States, supported by the supplier evidence review.
- [ ] Define the daily budget, target acquisition cost, and review checkpoints; cap the initial advertising experiment at $40 or the smaller amount available after setup costs.
- [ ] Keep paid campaigns off until store, tracking, supplier evidence, and order-funding checks pass; use organic interest checks while those are pending.
- [ ] Prepare product-specific headlines, descriptions, images, and video assets for the chosen campaign.
- [ ] Test clear angles: room styling, a useful product feature, or a specific customer use case.
- [ ] Publish supporting organic content: room inspiration, dimensions/fit guidance, installation demonstrations, and product comparisons.
- [ ] Add email signup and a welcome offer only if the economics support it.

Shopping uses product-feed information to match ads to searches. Performance Max can distribute across several Google channels and needs thoughtful creative and measurement. See [Shopping ads](https://support.google.com/google-ads/answer/2454022?hl=en) and [Performance Max](https://support.google.com/google-ads/answer/10724817?hl=en).

**Completion gate:** an affordable test is running with a defined success measure. If setup consumes the available advertising allowance, complete organic interest checks and defer paid campaigns. A small number of clicks or no sales is not conclusive validation or rejection.

## 9. Improve before expanding

- [ ] Review spend, purchases, acquisition cost, and contribution after advertising by product.
- [ ] Diagnose weak points: impressions, clicks, product-page engagement, checkout, or fulfillment.
- [ ] Test changes to images, offers, pages, and pricing in a controlled sequence.
- [ ] Track delivery performance, complaints, damage, returns, and refunds.
- [ ] Pause products that fail the agreed economics or quality thresholds.
- [ ] Propose a separate next-phase budget when results and fulfillment support it; do not increase spending beyond the initial $100 cap without a new budget decision.
- [ ] Add adjacent products and additional paid channels after the initial approach shows repeatable results.
- [ ] Automate repeatable research, creative, and catalog work once the process is proven.

**Immediate milestone:** complete a researched shortlist, gather supplier media and specifications, and produce one product's creative/listing draft within the no-samples policy. Confirm actual setup costs before committing any of the $100 budget.
