# Electrical safety hierarchy: USB vs plug-in vs hardwired
Generated 2026-09-28

**Not legal advice.** Sourced from the NEC, UL standards, CPSC regulations and government
product-safety reports. Have a US product-safety attorney review before relying on it.

## The hierarchy, lowest risk first

1. **USB / battery powered, no mains adapter shipped** - lowest
2. **USB with a certified adapter** (UL 62368-1)
3. **Mains cord-and-plug, NRTL-listed** (UL 153)
4. **Hardwired, NRTL-listed** (UL 1598)
5. Mains cord-and-plug, unlisted
6. **Hardwired, unlisted** - highest

## Catalogue power-source audit

Re-checked every product for low-voltage signals in descriptions, options and variants:

| Product | Power source found | Confidence |
|---|---|---|
| 120LED Floor Lamp | 5V / USB / battery mentioned; "120" refers to LED count, not voltage | likely USB/rechargeable |
| Sunset LED Table Lamp | 5V / USB / battery mentioned | likely USB/rechargeable |
| Vintage Mushroom Night Light | USB mentioned | USB-powered OR lamp-with-USB-port - **verify** |
| Tyst Clock | battery | confirmed non-mains |
| Heion Rice Paper Table Lamp | "Us Plug" option | confirmed mains, plug-in |
| Wabi-Sabi Wooden Floor Lamp | **no plug or voltage anywhere** | **undocumented - ask supplier** |
| Scandinavische Hanglamp | no signals; "Hanglamp" is Dutch for pendant | **likely hardwired - verify** |
| 6 fixtures (ceiling, chandelier, pendant, 3 wall) | hardwired by type | confirmed |

**So 3 of 12 electrical products look low-voltage, not 0.** That materially improves the mix.

## Why USB is genuinely safer

- **NEC Article 411** covers lighting at or below **30V AC / 60V DC**. A USB lamp runs at
  **5V DC** - an order of magnitude below the low-voltage threshold. There is no mains
  potential inside the product at all.
- **UL 153** (Portable Electric Luminaires) explicitly contemplates luminaires "intended to
  operate from **USB, or POE power sources**". **UL 1786 / CSA C22.2 No.256** requires that
  "an integral USB port shall be supplied by a **Class 2 circuit**" - Class 2 being the
  isolated, current-limited output class.
- **Article 411.4(B)** permits a low-voltage system to be an "assembly of **listed parts**" -
  which a USB lamp trivially satisfies if the adapter is listed.
- **A total failure of the lamp cannot energise anything dangerous.** 5V at 2A is 10W. There
  is no arc source and no ignition source inside the fixture.

**The one weak point is the adapter.** Health Canada's assessment of USB chargers: units that
"do not adequately restrict the flow of electric current between the primary and secondary
circuits may result in an electric shock hazard, or overheating that poses a burn or fire
hazard" - and "breakdown of low-quality insulation can create a short circuit between the
primary and secondary circuits allowing dangerous flow of electric current from the AC
circuit."

**Mitigation: ship a certified adapter (UL 62368-1, which replaced 60950-1), or ship no
adapter at all and let the customer use a phone charger.** A certified generic adapter is a
known commodity; an unbranded one is the single most common failure point.

### Two government safety reports that matter

The UK Office for Product Safety published reports on two **"USB Bedside Table Lamp"**
products - one an **AliExpress listing (ID 1005004248437511)** - both rated **high risk of
electric shock**, failing on insulation resistance, electric strength, creepage and clearance:
"accessible metal parts can become live... they would receive an electric shock."

Note what those products are: **mains lamps with USB charging ports**, not USB-powered lamps.
That is a different and more hazardous class, and it is what "USB table lamp" usually means on
marketplaces. **Know which one you are buying.** A product with a USB port is not a USB
product.

## Why plug-in beats hardwired

### The physical differences

- **Installation.** A hardwired fixture requires the customer - or an amateur handyman - to
  make a mains connection behind the wall: correct conductors, a proper ground, correct
  strain relief. **Installation error is then argued about as a product defect.** A plug-in
  lamp has no installation step beyond inserting a plug.
- **Visibility.** A table lamp that begins to fail is **on a table, in the room, and can be
  unplugged in one second**. A ceiling fixture that begins to fail is **inside a ceiling void,
  above insulation, where fires start unnoticed.**
- **De-energising.** Unplug vs find the breaker.
- **Recall mechanics.** "Unplug it and dispose of it, we'll refund you" vs **an electrician
  visit per unit.**

### The evidentiary difference - which is the real answer

- **Hardwired unlisted = you sold a fixture that cannot legally be installed.** NEC 410.6
  requires all luminaires to be listed. An unlisted hardwired fixture fails an inspection in
  virtually every jurisdiction. A plaintiff does not have to prove a manufacturing defect -
  **the violation is on the label.** That is a far easier case to bring.
- **Plug-in unlisted = no code violation.** Nobody inspects a table lamp. The plaintiff must
  prove the product was actually defective and caused the loss - **a materially harder case.**
- **Fire investigation.** After a house fire the fire marshal examines the wiring, and an
  unlisted hardwired fixture is a finding that lands in the insurer's report and then in any
  claim.

Note the honest caveat: **NEC 410.6 applies to both**, and NEC 410.42 permits portable
luminaires to use a **polarized two-wire plug** with "a well-established acceptable field
record." Plug-in is not exempt from listing. It is a **better-documented, lower-consequence,
easier-to-defend** category.

## What to do

1. **Verify the three presumed-USB products.** Confirm USB-powered vs lamp-with-USB-port,
   and if an adapter ships with it, get its certificate (UL 62368-1).
2. **Verify Heion's "Us Plug"** cord and plug listing.
3. **Get a written power spec for the Wabi-Sabi floor lamp** - it currently documents neither
   plug nor voltage.
4. **Verify the Scandinavische Hanglamp.** "Hanglamp" is Dutch for pendant, so it may be
   hardwired while being sold as a plug-in lamp.
5. **Remove the AC 220V variant** from Modern Round Wall Lamp.
6. **Strategic call: lead with USB/battery and plug-in, and either certify or drop the six
   hardwired fixtures.**
