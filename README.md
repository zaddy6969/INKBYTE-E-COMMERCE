# INKBYTE — blue and yellow ecommerce storefront

Open `INKBYTE-preview.html` in a modern browser. It is self-contained, including the hero image, catalogue, styling and scripts. No installation or internet connection is required. Keep JavaScript enabled.

Approved storefront design for `zaddy6969/INKBYTE-E-COMMERCE`. The supplied INKBYTE logo is used unchanged. Its exact blue (`#2c5d87`) and yellow (`#ffc83d`) drive navigation, buttons, accents, product mockups and the footer. The project is prepared for a Git-linked Vercel deployment.

## Included screens

- Home, new items and all-products catalogue.
- Corporate gifts, print and stationery, clothing and bags, wedding invitations, and gift hampers.
- Product details with live name/colour mockups, quantity, optional clothing size, artwork preview and requirements.
- Saved products, cart, contact-and-delivery form, request review and saved-request confirmation.
- Bulk enquiry, contact, about and help pages.

The storefront lists 127 product options in 24 categories. The workbook provides 79 options, including 37 from `Corporate gift` and 42 from `printing`. Those entries retain their source sheet, row and original description. The 48 new options are maintained in `catalogue-additions.json` and added during the build. Visiting cards are listed in packs of 100.

## Preview behaviour

Search recognises terms such as business cards, diary and tshirt. Filters use starting market reference prices, with sorting by name or price. Saved items, cart customisations and the latest request persist in this browser when local storage is available. They do not sync between devices. The help page has a control to remove all saved preview data.

Artwork selection accepts PNG, JPEG or WebP up to 3 MB. The image is shown locally and is not uploaded. Only its filename enters the cart and downloaded request. Reattach original artwork when arranging a real order.

Checkout and enquiry forms save a clearly labelled local request and download it as text. They do not send a message, place an order, reserve stock or collect payment.

## Pricing and proposed content

The workbook's entire `Our price` column is empty. Its market ranges appear as guide prices. Workbook entries without a market price and all 48 new options show `Price on request`. The single-sheet calendar has only a starting value. Cart totals are indicative, and identify incomplete ranges. Personalisation, taxes, delivery and actual minimum quantities require confirmation. INR is assumed for the preview and must be confirmed before publication.

All 127 listings use distinct AI-generated studio product concepts. The product photo stays visible while the name and colour preview appears in a separate personalisation sketch. `product-photos.json` records the product-to-photo assignments, image dimensions and generation prompts. The WebP image sheets are in `dist/assets/products/` and `dist/assets/catalogue-photos.webp`.

## Reference sites reviewed

- [MOO](https://www.moo.com/us/): product presentation, special-finish cards and curated gifting navigation.
- [VistaPrint India](https://www.vistaprint.in/): print and gifting catalogue structure and category navigation.
- [Printo](https://printo.in/): combined custom-print, merchandise and corporate-order journeys.

The design and code are original; no reference site's assets, templates or testimonials were copied.

## Local development

`dist/index.html` is a buildless version with separate CSS, JavaScript and assets. Use any static server with `dist` as its document root. There are no npm dependencies.

Run `python build.py` after editing the catalogue, product photo manifest, page template, styles or scripts. It checks that each product has exactly one photo, then recreates `dist/index.html` and the self-contained `INKBYTE-preview.html`.

The original workbook is not published in the repository. The generated catalogue records the source sheet and row for audit. To regenerate from your own copy, run `python catalogue.py /absolute/path/to/workbook.xlsx`, then run `python build.py`.

Hash routes make all screens work when the HTML is opened directly as a local file. A production implementation should use clean, indexable URLs and production metadata.

## Verification completed

- JavaScript syntax checks and workbook-to-catalogue reconciliation.
- Desktop browsing, business-card search, budget filtering and price sorting.
- Save/unsave, live brand and colour customisation, cart arithmetic and pack-of-100 handling.
- Contact and delivery validation, request review, local saving and text download.
- Mobile layouts at a 390-pixel frame width (375 pixels of content with the browser scrollbar), mobile menu/search, category filters, cart and checkout. Checked for horizontal overflow in these screens.
- Sticky navigation corrected during review.

These are desktop-browser responsive-layout checks. Physical iPhone and Android devices were not tested.

## Production order integration

The approved storefront can be deployed independently of real payment and order integrations. Confirm selling prices and price units, quantities and product specifications, actual artwork/photos, business contact details, shipping and return terms, payment provider, and order/enquiry destination. Production needs secure backend order handling, real validation, inventory/availability, payment verification and final business policies. The present design intentionally remains a reviewable HTML prototype.

## Vercel hosting

The repository root contains `vercel.json`, with framework set to Other, no install/build step, and `dist` as the output directory. The committed static output is deployed directly. No runtime secrets, paid integrations or external services are required for this version. Future pushes to the linked production branch can redeploy automatically.

The hero is an optimised WebP image. The supplied logo is preserved as the original PNG and is sized in CSS. Artwork remains illustrative and order/enquiry flows remain explicitly local demos.
