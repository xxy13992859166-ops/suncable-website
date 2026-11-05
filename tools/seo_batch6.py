"""SEO batch 6 - de-duplicate ten blog pages that share one identical body.

Ten blog files were generated from one template: only the head metadata differed,
the <article> body was byte-identical on all ten (346 words, the same generic
"why solar cable quality matters" text).  Each page promised a topic it did not
deliver ("Top 10 manufacturers" listed no manufacturers).

This batch writes ten distinct bodies, one per page, using only facts already
published on the site (product spec tables, certification marks, lead time, MOQ)
plus standard references (IEC 62930, EN 50618, IEC 62852, IEC 60228, IEC 60529,
IEC 60216, UL 4703).

Also fixes two credibility defects found in the same pass:
  - about.html said "Founded in 2009" and showed a "15+ Years" stat while the
    other 59 pages and its own lede say 20+ years / since 2004.
  - four product pages said "our Xi'an factory"; Xi'an is the registered office
    address, the factory claim on about.html is Shandong.  Wording made neutral.

Idempotent: every rewritten article carries the marker <!-- b6 --> and is
skipped on a second run.
"""

import pathlib
import re

MARK = "<!-- b6 -->"

ARTICLES = {}


def art(name, title, h1, desc, body):
    ARTICLES[name] = dict(title=title, h1=h1, desc=desc, body=body.strip())


# --------------------------------------------------------------------------
art(
    "blog-top-10-solar-cable-manufacturers-china.html",
    "10 Questions to Ask a Solar Cable Manufacturer in China",
    "10 Questions to Ask a Solar Cable Manufacturer in China",
    "Ten questions that separate a PV cable factory from a trading company: "
    "certification scope, test reports, conductor class, MOQ and lead time.",
    """
      <p>The title of this page used to promise a list of ten manufacturers. There is no honest way to publish such a list: Chinese PV cable capacity changes every quarter, most "top ten" lists are paid placements, and a name on someone else's list tells you nothing about whether that factory can issue the certificate your customer's inspector will ask for. So this page answers the question you actually have — how do I tell a real PV cable factory from a trading company that will subcontract my order — with ten questions you can ask any supplier today.</p>

      <h2>Why the questions matter more than the list</h2>
      <p>PV cable is a commodity in appearance and not in fact. Two drums can look identical and differ in conductor stranding class, insulation compound, wall thickness tolerance and weather-resistance classification. The difference does not show up in a photo or a price table; it shows up in year eight on a rooftop, in a failed inspection, or in a string that quietly loses output. A supplier who can answer the ten questions below with documents is a different kind of company from one who answers with adjectives.</p>

      <h2>The ten questions</h2>
      <ol>
        <li><strong>Which standard does the cable hold, and who tested it?</strong> For IEC 62930 or EN 50618 the certificate should come from a recognised body (TÜV Rheinland, TÜV SÜD, DEKRA, UL) and carry a certificate number you can look up yourself.</li>
        <li><strong>Does the certificate cover the size I am buying?</strong> A certificate for 4 mm² does not automatically cover 10 mm². Ask for the certificate scope, not a logo.</li>
        <li><strong>What conductor class is used?</strong> PV cable is normally Class 5 flexible tinned copper to IEC 60228. Aluminium or copper-clad conductors are sold as equivalents in some markets and are not equivalent.</li>
        <li><strong>What is the insulation compound?</strong> Cross-linked polyolefin (XLPO) is the standard for outdoor PV. PVC appears in cheap "solar" cable and does not carry the same UV or thermal performance.</li>
        <li><strong>What is the rated temperature window?</strong> A correct answer distinguishes ambient operating range (−40 °C to +90 °C for EN 50618 cable) from maximum conductor temperature (120 °C).</li>
        <li><strong>Can I see a type-test report, not just a certificate?</strong> Thermal endurance, cold bend, ozone, water immersion and voltage withstand data should exist as a document.</li>
        <li><strong>Are you the factory or a trading company?</strong> Ask for the production address and the extrusion capacity. Then check that the address matches the certificate holder.</li>
        <li><strong>What is your MOQ and your real lead time?</strong> A factory that states a clean MOQ (for example 1 km per colour) and a 7–15 day standard lead time is easier to plan around than one that says "depends".</li>
        <li><strong>Will you ship a sample before the bulk order?</strong> Free or paid, a sample you can cut, measure and bend tells you more than a datasheet.</li>
        <li><strong>Who honours the warranty?</strong> A 25-year claim is only worth the entity behind it. Ask who replaces the cable and in which country the claim is handled.</li>
      </ol>

      <h2>What strong and weak answers look like</h2>
      <table>
        <thead>
          <tr><th>Question</th><th>Strong answer</th><th>Warning sign</th></tr>
        </thead>
        <tbody>
          <tr><td>Certification</td><td>Certificate number plus issuing body, scope by size</td><td>"TUV standard" with no number</td></tr>
          <tr><td>Conductor</td><td>Class 5 tinned copper, IEC 60228</td><td>"High purity copper" with no class</td></tr>
          <tr><td>Factory</td><td>Production address that matches the certificate</td><td>Office address only</td></tr>
          <tr><td>Lead time</td><td>A number, plus what changes it</td><td>"As soon as possible"</td></tr>
        </tbody>
      </table>

      <div class="tip-box">
        <p><strong>A five-minute check:</strong> take the certificate number from the supplier and search it on the issuing body's own database — Certipedia for TÜV Rheinland, Product iQ for UL. If the number does not return the same product description and size range, stop there.</p>
      </div>

      <h2>What to send us</h2>
      <p>If you are shortlisting suppliers now, send us the cable type and size, the quantity in metres and the destination port. We reply with price, lead time and packing, and we will include the certificate scope for the sizes you asked about rather than a logo. Both PV1-F (2-core, 0.6/1 kV) and H1Z2Z2-K (single core, 1 kV) are available with TÜV, UL and CE documentation, MOQ 1 km per colour, samples by DHL or FedEx.</p>
    """,
)

art(
    "blog-mc4-connector-selection-guide.html",
    "MC4 Connector Selection Guide: Choosing Solar Connectors",
    "MC4 Connector Selection Guide: Complete Buyer's Guide 2026",
    "How to choose the right MC4 connector for a PV array: current rating, "
    "IP68 sealing, 1500 V DC compatibility and crimping quality. TUV certified.",
    """
      <p>Most PV array failures that get blamed on cable are actually connector failures. A connector concentrates the current of a whole string into a few square millimetres of contact, sits in the sun for twenty-five years, and is assembled on site by whoever is available. Choosing the right part and crimping it properly matters more than the price difference between two brands.</p>

      <h2>1. Match the voltage and current rating to the string</h2>
      <p>Modern strings are designed for 1500 V DC systems, and the connector must carry the string current with margin. Our MC4-Evo2 set is rated 1500 V DC and 1000 V DC, 41 A (32 A for the Evo2-PA4 variant), which covers residential and commercial string sizes. If your string current is close to the rating, derate for temperature: contact resistance rises with heat, and a connector running at its limit in a hot roof void is a hotspot waiting to happen.</p>

      <h2>2. Check the cable range and the crimp</h2>
      <p>The connector must match the cable cross-section, not approximately but exactly. Our set accepts 1.5–6 mm² Class 5 tinned copper. Three things decide whether the joint survives:</p>
      <ul>
        <li><strong>The right crimping tool.</strong> A generic plier deforms the barrel unevenly; use the crimper specified for the connector series.</li>
        <li><strong>Strand integrity.</strong> No cut strands, no strands folded back outside the barrel.</li>
        <li><strong>A pull check.</strong> After crimping, the joint should not move under a firm axial pull. If it does, cut it off and redo it — a loose crimp is a future fire, not a future repair.</li>
      </ul>

      <h2>3. Sealing is a system, not a gasket</h2>
      <p>IP68 to IEC 60529 is only achieved when the gland compresses against the cable's actual outside diameter and the O-ring seats cleanly. A connector rated IP68 will leak if it is closed on a cable that is too thin, if the O-ring is dry, or if the nut is hand-tightened without the final quarter turn. Torque it, and use the sealing grease supplied with the part, not an arbitrary substitute.</p>

      <h2>4. Never mate two different brands</h2>
      <p>"MC4 compatible" means the shape fits, not that the contact system is tested together. Mating brand A to brand B voids both manufacturers' approvals and is one of the most common causes of water ingress and thermal failure on site. Keep one brand per string, and carry spare pairs of the same type.</p>

      <h2>5. Field practice that prevents callbacks</h2>
      <table>
        <thead>
          <tr><th>Parameter</th><th>What to check</th></tr>
        </thead>
        <tbody>
          <tr><td>Voltage / current</td><td>1500 V DC, 41 A class for string applications</td></tr>
          <tr><td>Cable range</td><td>1.5–6 mm², Class 5 copper, correct gland size</td></tr>
          <tr><td>Sealing</td><td>IP68, O-ring seated, nut torqued, cable OD within gland range</td></tr>
          <tr><td>Mating</td><td>Same brand and series on both sides of every joint</td></tr>
          <tr><td>Support</td><td>Connectors not left hanging on the cable; strain relieved at the rail</td></tr>
          <tr><td>Certification</td><td>TÜV and UL marks on the part, not only on the box</td></tr>
        </tbody>
      </table>

      <div class="tip-box">
        <p><strong>Thermal cycling is the real test.</strong> A joint that measures fine at commissioning can open up after a hundred hot days. Sample-check resistance on a few joints per string after the first summer, and compare strings against each other — a string running a few percent low usually has one bad connector, not a bad module.</p>
      </div>

      <h2>Ordering</h2>
      <p>Send the cable size you are using, the number of pairs, and the system voltage. We supply MC4-Evo2 male/female pairs, IP68, 1500 V DC, TÜV and UL certified, pre-crimped with 1 m of PV cable on each end if you prefer factory terminations over site crimping. Pairs ship with the cable orders, so the connector rating and the cable rating always match.</p>
    """,
)

art(
    "blog-pv-cable-testing-certification.html",
    "PV Cable Testing & Certification: IEC 62930 vs TUV vs UL",
    "PV Cable Testing & Certification: Complete Guide for 2026",
    "PV cable testing and certification explained: IEC 62930, TUV and UL 4703 "
    "test regimes, what each mark covers and what to ask a supplier.",
    """
      <p>Three different things get called "certification" in the PV cable trade: a standard, a type test, and a certificate. They are not interchangeable, and a supplier who cannot separate them usually cannot produce the paperwork either. Here is what each one actually is, and what it does and does not prove about the drum you are buying.</p>

      <h2>The standard defines the test, not the product</h2>
      <p>IEC 62930 and its European counterpart EN 50618 describe a halogen-free, cross-linked photovoltaic cable and the tests it must pass. The standard is a document; it does not certify anything. A manufacturer can design to it, and an independent laboratory can test against it — those are separate steps.</p>

      <h2>What the type tests actually put the cable through</h2>
      <ul>
        <li><strong>Thermal endurance.</strong> Long-duration ageing at elevated temperature, assessed to IEC 60216, is what supports a 25-year service claim. Without it the claim is marketing.</li>
        <li><strong>Cold bend and impact.</strong> The cable is conditioned at −40 °C and bent around a mandrel; a compound that cracks in a northern winter fails here.</li>
        <li><strong>UV and weather resistance.</strong> Accelerated exposure in a weathering chamber, followed by mechanical checks. This is the test that separates XLPO from PVC.</li>
        <li><strong>Ozone, water immersion and shrinkage.</strong> Small-sample tests that catch compound and cross-linking problems.</li>
        <li><strong>Voltage withstand.</strong> Proof that the insulation wall holds at the rated voltage with margin.</li>
      </ul>

      <h2>TÜV, UL and CE are three different claims</h2>
      <table>
        <thead>
          <tr><th>Mark</th><th>Issued by</th><th>What it proves</th><th>How to check</th></tr>
        </thead>
        <tbody>
          <tr><td>IEC 62930 / EN 50618</td><td>Nobody — it is a standard</td><td>That a test regime exists for the product type</td><td>Read the scope; ask for the test report</td></tr>
          <tr><td>TÜV certificate</td><td>TÜV Rheinland, TÜV SÜD or similar</td><td>Type-tested product, with a certificate number and size scope</td><td>Certipedia or the body's own database</td></tr>
          <tr><td>UL listing (UL 4703)</td><td>Underwriters Laboratories</td><td>North American acceptance, file number and product category</td><td>UL Product iQ</td></tr>
          <tr><td>CE marking</td><td>The manufacturer, self-declared</td><td>Declaration of conformity to applicable EU directives</td><td>The declaration document itself</td></tr>
        </tbody>
      </table>
      <p>CE is the one most often misread. It is a self-declaration, not a third-party approval; on its own it says nothing about thermal endurance or UV performance. TÜV and UL are third-party, which is why buyers in Europe and North America ask for them by name.</p>

      <h2>What to ask a supplier, in order</h2>
      <ol>
        <li>The certificate number, the issuing body, and the size range covered.</li>
        <li>The type-test report for thermal endurance and UV, with the test laboratory named.</li>
        <li>Confirmation that the production address on the certificate is the address that will make your order.</li>
        <li>A batch test certificate for the actual production run, not the type test from years ago.</li>
      </ol>

      <div class="tip-box">
        <p><strong>The scope trap.</strong> A certificate that lists 4 mm² does not certify 6 mm², and a certificate held by a trading company does not transfer to the factory that makes the cable. Read the scope line, not the logo on the website.</p>
      </div>

      <h2>Our documentation</h2>
      <p>PV1-F (2-core, 0.6/1 kV, IEC 62930 and VDE AR-N 1000-712) and H1Z2Z2-K (single core, 1 kV, IEC 62930 and VDE 0264) ship with TÜV, UL and CE documentation, TÜV EL 23 A approval on the H1Z2Z2-K range, and 25-year warranty terms. Tell us the sizes you need and we will send the certificate scope for those sizes with the quotation.</p>
    """,
)

art(
    "blog-solar-cable-fault-diagnosis.html",
    "Solar Cable Fault Diagnosis: 7 Common Problems",
    "Solar Cable Fault Diagnosis: 7 Common Problems and Solutions",
    "Seven common PV cable faults and how to prevent them: hot spots, water "
    "ingress, UV cracking, rodent damage and connector failures.",
    """
      <p>PV strings fail slowly and then all at once. The useful signal is almost never a sudden open circuit — it is a string running a few percent below its neighbours for months, a connector warmer than the one next to it, or a jacket that has stopped being flexible. These are the seven faults we see most often on installed arrays, how to recognise each one, and what actually prevents it.</p>

      <h2>1. Hot connector or crimp</h2>
      <p><strong>Symptom:</strong> a connector that is noticeably warm, discoloured, or shows a rising resistance reading between visits. <strong>Cause:</strong> incomplete crimp, wrong barrel for the cable size, or a joint that loosened under thermal cycling. <strong>Fix:</strong> cut back and re-terminate with the specified tool; check a handful of joints per string, not just the failed one.</p>

      <h2>2. Water ingress at the connector</h2>
      <p><strong>Symptom:</strong> green or black corrosion on the contact, a string that fails after rain, sealant squeezed out of the gland. <strong>Cause:</strong> O-ring not seated, nut not torqued, cable outside the gland's diameter range, or two different brands mated together. <strong>Fix:</strong> replace the pair, match gland to cable OD, and keep one brand per string.</p>

      <h2>3. UV cracking and jacket crazing</h2>
      <p><strong>Symptom:</strong> surface crazing, chalking, or a jacket that cracks when bent at a bend radius that should be comfortable. <strong>Cause:</strong> PVC or under-cross-linked compound sold as solar cable; or cable left on a drum in the open for a season before installation. <strong>Fix:</strong> specify XLPO cable tested to IEC 62930 or EN 50618, and cover drums on site.</p>

      <h2>4. Rodent damage</h2>
      <p><strong>Symptom:</strong> chewed jacket, usually at trays, wall penetrations or the first metre above ground. <strong>Cause:</strong> exposed routing in agricultural or rural sites. <strong>Fix:</strong> route in conduit at vulnerable sections, backfill trenches properly, and prefer a harder jacket in these runs rather than relying on the standard cable alone.</p>

      <h2>5. Mechanical damage at supports and edges</h2>
      <p><strong>Symptom:</strong> a clean nick or flattened section where the cable crosses a tray lip, clamp or roof edge. <strong>Cause:</strong> sharp edges, over-tight clamps, or cable pulled around a corner below its bend radius. <strong>Fix:</strong> add edge protection, use cable ties at the correct tension, and respect the radius rule — as a rule of thumb, four times the overall diameter for a fixed bend.</p>

      <h2>6. Thermal cycling loosening terminations</h2>
      <p><strong>Symptom:</strong> torque marks that no longer line up after a year; intermittent string readings. <strong>Cause:</strong> dissimilar expansion rates and joints that were never re-torqued after commissioning. <strong>Fix:</strong> include a re-torque check in the first annual service.</p>

      <h2>7. Mismatched cross-section and long runs</h2>
      <p><strong>Symptom:</strong> a string that is consistently low on output with no fault found. <strong>Cause:</strong> undersized cable on a long DC run, so voltage drop eats the difference. <strong>Fix:</strong> recalculate against the actual run length; a typical design target is to keep DC drop to 1–2 %.</p>

      <table>
        <thead>
          <tr><th>What you see</th><th>Most likely cause</th><th>First action</th></tr>
        </thead>
        <tbody>
          <tr><td>Warm connector</td><td>Crimp or mating fault</td><td>Cut and re-terminate</td></tr>
          <tr><td>Corrosion after rain</td><td>Seal failure</td><td>Replace pair, check gland size</td></tr>
          <tr><td>Cracked jacket</td><td>Wrong compound or UV exposure</td><td>Confirm IEC 62930 cable, replace run</td></tr>
          <tr><td>Chewed jacket</td><td>Rodents</td><td>Conduit at vulnerable sections</td></tr>
          <tr><td>Low string, no fault</td><td>Voltage drop</td><td>Recalculate run length and size</td></tr>
        </tbody>
      </table>

      <div class="tip-box">
        <p><strong>Diagnose by comparison.</strong> Measure every string at the same irradiance and compare them with each other. A fault shows up as one string that differs from its neighbours; chasing one string in isolation usually finds nothing.</p>
      </div>

      <h2>Getting the cable right the first time</h2>
      <p>Six of the seven faults above are decided before the cable arrives on site. If you send us the run lengths, the string current and the destination port, we will confirm whether PV1-F 2-core or H1Z2Z2-K single core suits the layout, and quote with the lead time you need.</p>
    """,
)

art(
    "blog-solar-cable-for-agricultural-solar.html",
    "Solar Cable for Agri-PV Projects: Wiring Solutions",
    "Solar Cable for Agricultural Solar Projects: Agri-PV Solutions",
    "Wiring agrivoltaic and agricultural solar projects: cable routing around "
    "irrigation, rodent protection, UV exposure and connector choice.",
    """
      <p>Agricultural PV is the least forgiving environment a cable will ever see. A rooftop array on an office building deals with sun and heat; an array over a field or on a barn roof deals with irrigation spray, condensation cycles, ammonia, rodents, dust, machinery and, increasingly, people walking under it with tools. Selection decisions that are optional elsewhere are not optional here.</p>

      <h2>Long runs make voltage drop the first decision</h2>
      <p>Agri-PV layouts spread out: arrays follow field boundaries, inverters sit at the edge of the plot, and DC runs of a few hundred metres are normal. At that distance the cable size is set by voltage drop, not by current-carrying capacity. Work the calculation on the real route length — including vertical drops and the loop through the tracker — before you fix a size, and keep the DC loss inside the 1–2 % design target. Oversizing one step is usually cheaper than accepting a permanent 3 % loss for twenty-five years.</p>

      <h2>Irrigation, condensation and standing water</h2>
      <p>Sprinkler overspray and overnight condensation mean the cable sees water far more often than the "outdoor" label implies. Two practical rules:</p>
      <ul>
        <li>Terminate connectors above the local water line and never at the low point of a run.</li>
        <li>Use IP68 connectors and seat them properly — a gland that is a size too large will pass water under spray even though the part is rated IP68.</li>
      </ul>
      <p>Where cable is buried between rows, use a duct or a rated direct-burial construction, keep the trench clear of field drainage, and record the route so the next subsoiling pass does not find it.</p>

      <h2>Livestock buildings: ammonia and rodents</h2>
      <p>Inside poultry or cattle housing the aggressive agents are ammonia and rodents, not sunlight. Route cable in conduit, keep it off ledges where dust collects, and avoid PVC-jacketed product in these buildings — the point of a halogen-free XLPO construction is that it does not embrittle the way PVC does under chemical and thermal load. For runs to fans, feeders and lighting, a steel or rigid conduit is often the cheapest long-term answer.</p>

      <h2>Dust, heat and elevated mounting</h2>
      <p>Panels over crops are usually mounted higher than a standard rooftop, so more cable hangs in air and moves with wind. Support it at shorter intervals than you would on a roof, keep connectors off the ground, and derate for the higher ambient temperature under the array rather than for the weather-station reading.</p>

      <table>
        <thead>
          <tr><th>Site condition</th><th>What the cable has to handle</th><th>Practical answer</th></tr>
        </thead>
        <tbody>
          <tr><td>Long field runs</td><td>Voltage drop over 200–400 m</td><td>Size on drop, keep DC loss to 1–2 %</td></tr>
          <tr><td>Irrigation spray</td><td>Repeated wetting, low points</td><td>IP68 joints, terminate high, duct crossings</td></tr>
          <tr><td>Livestock housing</td><td>Ammonia, rodents, dust</td><td>Conduit, XLPO not PVC</td></tr>
          <tr><td>Elevated mounting</td><td>Wind movement, UV</td><td>Shorter support spacing, cable ties at correct tension</td></tr>
          <tr><td>Machinery traffic</td><td>Impact, snagging</td><td>Ducted or buried routes with recorded depth</td></tr>
        </tbody>
      </table>

      <div class="tip-box">
        <p><strong>Plan the cable route with the agronomist, not after.</strong> Headland turning circles, irrigation mains and subsoiling depth all constrain where a cable can run. Moving a route on paper costs nothing; moving it after commissioning costs a season.</p>
      </div>

      <h2>Specifying the cable</h2>
      <p>For agri-PV we normally quote H1Z2Z2-K single core (1 kV, 1.5–6 mm²) for string runs and PV1-F 2-core (0.6/1 kV, 1.0–6.0 mm²) where the red/black pair simplifies pulling. Both are XLPO insulated, rated −40 °C to +90 °C ambient with 120 °C maximum conductor temperature, and available with TÜV, UL and CE documentation. Send the layout and run lengths and we will come back with the size and the lead time.</p>
    """,
)

art(
    "blog-solar-cable-for-commercial-project.html",
    "Solar Cable for Commercial Projects: Procurement Guide",
    "Solar Cable for Commercial Projects: Complete Sizing & Procurement Guide",
    "Sizing, standards and procurement for commercial rooftop PV: cable schedule, "
    "voltage drop, certification and lead time. TUV & UL certified manufacturer.",
    """
      <p>A commercial rooftop job is won or lost in procurement, not on the roof. The cable schedule arrives late, the sizes get rounded up "to be safe", the certification does not match what the consultant specified, and the drum lengths do not divide into the runs. Each of those costs money, and only one of them is visible on the invoice.</p>

      <h2>Start from the cable schedule, not from a price list</h2>
      <p>Before asking anyone for a price, fix four things: the DC string layout, the run lengths from array to inverter, the AC route to the point of connection, and the ambient temperature the cable will actually sit in. Those four numbers determine every size on the sheet. A supplier quoting against "about 2,000 metres of 4 mm²" is guessing, and so is the price.</p>

      <h2>Sizing: voltage drop first, then ampacity</h2>
      <p>On a commercial roof the runs are long enough that voltage drop usually governs. Set the DC target at 1–2 % and check the AC side separately. Then confirm the conductor still carries the current after derating for the temperature in the tray — a cable sized only against the datasheet ampacity, with no derating for a hot roof void, is a common commissioning finding.</p>

      <h2>The DC and AC sides are different products</h2>
      <table>
        <thead>
          <tr><th>Circuit</th><th>Typical cable</th><th>Why</th></tr>
        </thead>
        <tbody>
          <tr><td>Module to module, string to combiner</td><td>H1Z2Z2-K single core, 1 kV, 1.5–6 mm²</td><td>UV-stable, flexible, standard PV construction</td></tr>
          <tr><td>Array to inverter (2-core layout)</td><td>PV1-F 2-core, 0.6/1 kV, 1.0–6.0 mm²</td><td>Red/black pair, faster pulling, one drum</td></tr>
          <tr><td>Inverter to AC distribution</td><td>450/750 V 3-core to IEC 60228</td><td>Different voltage class and insulation duty</td></tr>
          <tr><td>Battery or storage link</td><td>LSZH DC cable, 0.6/1 kV</td><td>Low smoke, high current, indoor routing</td></tr>
        </tbody>
      </table>

      <h2>Fire, tray and routing</h2>
      <p>Where cable enters the building it stops being an outdoor product. Check the local requirement for flame propagation and smoke on internal routes, keep DC and AC in separate containment where the standard requires it, and do not run PV cable in the same tray as mains without the segregation the inspector will ask for. On a roof, support intervals and edge protection matter more than the cable choice — most mechanical damage happens at a tray lip, not mid-span.</p>

      <h2>Documentation for handover</h2>
      <p>A commercial client will ask for the certificate scope, the batch test certificate, and confirmation that the sizes installed are the sizes certified. Collect them at order time, not at handover: getting a certificate amended after the drum is on site is the slowest possible way to close a project.</p>

      <div class="tip-box">
        <p><strong>Order lengths that divide into runs.</strong> Drum lengths that leave a 40 m offcut per run turn into scrap. Send us the run list and we will match drum lengths to it — it usually saves more than a small unit-price difference.</p>
      </div>

      <h2>What we need to quote</h2>
      <p>Send the run list or cable schedule with sizes and quantities, the destination port, and the certification the consultant specified. We quote PV1-F and H1Z2Z2-K with TÜV, UL and CE documentation, MOQ 1 km per colour, standard lead time 7–15 days, and we reply within two hours on business days.</p>
    """,
)

art(
    "blog-solar-cable-for-off-grid-system.html",
    "Solar Cable for Off-Grid Systems: Complete Wiring Guide 2026",
    "Solar Cable for Off-Grid Systems: Complete Wiring Guide",
    "Off-grid PV wiring: array-to-controller voltage drop, battery bank cabling, "
    "fusing and cable choice for remote and mobile installations.",
    """
      <p>Off-grid systems punish two mistakes that grid-tied systems forgive: voltage drop on long low-voltage runs, and undersized battery cabling. Both show up as heat and lost charging hours rather than as a fault code, which is why they survive for years without being fixed.</p>

      <h2>Array to controller: the drop eats your harvest</h2>
      <p>An off-grid array is often mounted where the sun is, not where the batteries are. If the panels sit 30 m from the controller, that 30 m is in both the positive and negative leg, so the loop is 60 m, and at a 48 V nominal system the current is high enough that drop matters.</p>
      <ul>
        <li>Work on loop length, not one-way length.</li>
        <li>Keep the array-to-controller drop to 1–2 % — every percent here is generation you never get back.</li>
        <li>If the run is long, move to a higher array voltage with a suitable MPPT controller before you buy bigger cable; it is usually cheaper than copper.</li>
      </ul>

      <h2>Battery bank cabling is a current problem, not a voltage problem</h2>
      <p>At 12 or 24 V the currents are large, and short runs hide the loss. Two rules that prevent most battery-side problems:</p>
      <ol>
        <li><strong>Size for current with margin,</strong> and keep every link in a parallel bank the same length and the same cross-section so the strings share current equally.</li>
        <li><strong>Use a low-smoke, halogen-free DC cable indoors.</strong> Battery rooms and enclosures are exactly where you do not want PVC in a fault. Our storage battery DC cable is LSZH, 0.6/1 kV, TÜV certified.</li>
      </ol>

      <h2>Protection belongs in the design, not the shopping list</h2>
      <p>Every source in an off-grid system — array, battery, generator — can feed a fault. Fuse or breaker each one at the point where it connects, size the device to the cable it protects, and make sure the DC rating is a genuine DC rating. An AC breaker used on DC is a fire risk, not a cost saving.</p>

      <h2>Temperature, movement and remote sites</h2>
      <p>Off-grid installations are frequently in the places with the widest temperature swings: unheated cabins, containers, telecom shelters, boats. Cable rated −40 °C to +90 °C ambient with a 120 °C maximum conductor temperature covers that range without becoming brittle in winter. On mobile or temporary installations, add strain relief at every transition and inspect the cable at the same interval as the battery maintenance.</p>

      <table>
        <thead>
          <tr><th>Circuit</th><th>Sizing driver</th><th>Typical cable</th></tr>
        </thead>
        <tbody>
          <tr><td>Array to controller</td><td>Voltage drop over loop length</td><td>H1Z2Z2-K 1 kV, 1.5–6 mm²</td></tr>
          <tr><td>Controller to battery</td><td>Current, short run</td><td>Storage DC cable, LSZH, 0.6/1 kV</td></tr>
          <tr><td>Battery interconnect</td><td>Equal length and section per string</td><td>Storage DC cable, matched links</td></tr>
          <tr><td>Inverter output (AC)</td><td>Voltage class, 3-core</td><td>450/750 V to IEC 60228</td></tr>
        </tbody>
      </table>

      <div class="tip-box">
        <p><strong>Check the loop, not the run.</strong> Half of the off-grid underperformance we get asked about comes from a drop calculation done on one-way length. Double the figure before you choose the size.</p>
      </div>

      <h2>Getting the bill of materials right</h2>
      <p>Send the array voltage, controller model, battery bank voltage and the one-way distances, and we will come back with cable sizes and a matched bill of materials — PV cable, storage DC cable and MC4 connectors with the same ratings, so nothing on the DC side is the weak link.</p>
    """,
)

art(
    "blog-solar-cable-price-trend-2026.html",
    "Solar Cable Price Trends 2026: What Importers Need to Know",
    "Solar Cable Price Trends 2026: Complete Cost Guide for Importers",
    "What actually moves solar cable prices in 2026 — copper, XLPO compound, "
    "freight and drums — and why two quotes are rarely comparable.",
    """
      <p>Every importer asks the same question in a different way: is the price going up, and is this quote fair? The honest answer is that the number on a solar cable quotation is built from five inputs, and four of them have nothing to do with the factory's margin. Understand the five and you can read any quote, including one that looks suspiciously cheap.</p>

      <h2>The five inputs behind every quotation</h2>
      <ul>
        <li><strong>Copper.</strong> The conductor is the largest single material cost in a PV cable, and it moves with the exchange-traded copper price. This is why serious suppliers quote against a copper base date and adjust if the order is placed weeks later.</li>
        <li><strong>The XLPO compound.</strong> Cross-linked polyolefin is a specialty compound, not a commodity plastic. Its price follows the polymer market and the specific grade's availability, and substitution is where cheap cable usually saves money.</li>
        <li><strong>Cross-section mix.</strong> A quote for "4 mm²" and a quote for "4 and 6 mm²" are not comparable per metre. Copper content rises faster than the diameter suggests.</li>
        <li><strong>Drums and packing.</strong> Drum size, returnable versus one-way, and palletisation are real costs and change the freight profile.</li>
        <li><strong>Testing and certification.</strong> Type testing, batch testing and maintaining a certificate scope cost money per size. A supplier with no certificate scope is not necessarily cheaper to run — just less documented.</li>
      </ul>

      <h2>Why two quotes are rarely comparable</h2>
      <table>
        <thead>
          <tr><th>Line</th><th>Ask this</th></tr>
        </thead>
        <tbody>
          <tr><td>Incoterm</td><td>FOB or CIF? Which port, and is unloading included?</td></tr>
          <tr><td>Copper base</td><td>Which copper date and which reference price is the quote tied to?</td></tr>
          <tr><td>Size mix</td><td>Price per size, not a blended average</td></tr>
          <tr><td>Drums</td><td>Drum length, returnable or one-way, deposit?</td></tr>
          <tr><td>Certificate scope</td><td>Which sizes are covered, and is the batch certificate included?</td></tr>
          <tr><td>MOQ</td><td>MOQ per size or per colour, and what happens below it</td></tr>
        </tbody>
      </table>

      <h2>Where a cheap quote hides its cost</h2>
      <p>Three substitutions appear again and again, and all three are invisible on a price sheet: a copper-clad or aluminium conductor presented as equivalent, a PVC or partly cross-linked compound presented as XLPO, and a reduced insulation wall thickness that still passes a visual check. None of these fails at commissioning. They fail in year six, when the array is out of easy reach and the installer has moved on.</p>

      <h2>How to buy against a moving price</h2>
      <ol>
        <li>Fix the copper base date in the quotation, in writing.</li>
        <li>Ask for the price per size, per drum length, delivered to your port.</li>
        <li>Ask what changes the price between quotation and shipment, and by how much notice.</li>
        <li>Keep a second qualified supplier warm — the leverage that protects you in a rising market is a tested alternative, not a threat.</li>
      </ol>

      <div class="tip-box">
        <p><strong>Compare landed cost per metre-year, not price per drum.</strong> A cable that lasts 25 years at a slightly higher unit price is cheaper than one that has to be replaced in year eight, once labour and downtime are counted.</p>
      </div>

      <h2>Get a quote tied to a stated copper date</h2>
      <p>Send the sizes, quantities and destination port and we will quote per size with the copper base date stated on the document, standard lead time 7–15 days, MOQ 1 km per colour, TÜV and UL documentation included. If the market moves before you order, you will see exactly what changed.</p>
    """,
)

art(
    "blog-solar-cable-return-investment.html",
    "Solar Cable ROI: How Quality Cable Saves Money in 25 Years",
    "Solar Cable ROI: How Quality Cables Save Money Over 25 Years",
    "Why certified PV cable pays back over 25 years: failure cost, derating "
    "losses and replacement labour compared with cheap uncertified cable.",
    """
      <p>Cable is a small line in a PV bill of materials and a large line in the lifetime economics of the plant. The reason is simple: everything else in the array can be reached, unbolted and replaced in an afternoon. Cable is installed first, buried under the array, and stays there for twenty-five years. That asymmetry is the whole investment case.</p>

      <h2>Cost per metre is the wrong denominator</h2>
      <p>The useful number is cost per metre-year of service, not cost per metre. Two cables at different prices stop being comparable the moment one of them needs to be replaced, or loses output, before the plant's design life is over. Written as a comparison rather than a formula:</p>
      <ul>
        <li><strong>Certified cable:</strong> higher unit cost, no planned replacement, output held for the design life.</li>
        <li><strong>Uncertified cable:</strong> lower unit cost, plus a replacement event somewhere in year 5–12, plus the labour to reach and re-pull the run, plus the generation lost while it is down.</li>
      </ul>
      <p>The replacement event is what dominates. Re-pulling a string run on a commercial roof means scaffolding or rope access, isolating the string, and a second commissioning — costs that dwarf the saved unit price of the original drum.</p>

      <h2>Three costs that never appear on the invoice</h2>
      <table>
        <thead>
          <tr><th>Cost</th><th>Cheap cable</th><th>Certified cable</th></tr>
        </thead>
        <tbody>
          <tr><td>Replacement labour</td><td>Access, isolation, re-pull, re-terminate</td><td>None planned</td></tr>
          <tr><td>Lost generation</td><td>String offline during diagnosis and repair</td><td>None planned</td></tr>
          <tr><td>Inspection and compliance</td><td>Repeat findings, possible re-test</td><td>Documentation ready at handover</td></tr>
        </tbody>
      </table>

      <h2>Derating and voltage drop are permanent losses</h2>
      <p>A cable with a lower temperature rating, or a smaller cross-section chosen to hit a price, does not fail — it just runs hotter and drops more volts, every day, for the life of the plant. Those losses are silent: no alarm, no fault code, just a plant that produces slightly less than the model predicted. On a long DC run, one step down in cross-section is often worth more than a percent of annual yield.</p>

      <h2>Warranty is only worth the entity behind it</h2>
      <p>"25-year warranty" appears on almost every PV cable datasheet. The question worth asking is who performs under it: which legal entity, in which country, and what evidence they require. A warranty from a trading company that re-labels drums is a promise with no factory behind it. Ask for the certificate holder's name and check it matches the company issuing the warranty.</p>

      <div class="tip-box">
        <p><strong>A one-question test for any supplier:</strong> "If a string fails in year eight because of your cable, who pays for the access and re-pull?" A supplier with a real factory and a real certificate answers with a process. A reseller changes the subject.</p>
      </div>

      <h2>Building the comparison for your project</h2>
      <p>If you are putting together a tender comparison, send us the run lengths, string current and the plant life your client is modelling. We will quote PV1-F or H1Z2Z2-K with the certification scope for the sizes involved, so the alternative in your comparison is documented rather than asserted — MOQ 1 km per colour, 7–15 day lead time on standard sizes.</p>
    """,
)

art(
    "blog-solar-cable-storage-handling.html",
    "Solar Cable Storage & Handling: Prevent Cable Damage",
    "Solar Cable Storage & Handling: Best Practices Guide",
    "How to store and handle solar cable without damaging it: drum handling, "
    "bend radius, UV exposure and moisture control before installation.",
    """
      <p>Most cable that fails early was damaged before it was energised. A drum left in the sun for a season, a run pulled over a sharp edge, a cut end left open in the rain — none of these show up at commissioning, and all of them shorten the service life of a product that is supposed to last twenty-five years. The rules below cost nothing to follow and are the cheapest reliability measure on any project.</p>

      <h2>Drums: upright, off the ground, restrained</h2>
      <ul>
        <li>Store drums upright on their flanges, never lying on the side of the barrel.</li>
        <li>Keep them off bare ground on dunnage so moisture does not wick into the outer layers.</li>
        <li>Chock them so they cannot roll, and never drop a drum off a tailgate — impact damage to the inner layers is invisible from outside.</li>
        <li>Roll a drum only to move it a short distance; for anything longer, lift it.</li>
      </ul>

      <h2>UV, heat and cold before installation</h2>
      <p>XLPO is designed for decades of sunlight, but that assumes installation. Cable stored outdoors for months on an uncovered drum sees the same UV with no thermal path to shed heat, and the outer wraps take the worst of it. Keep drums covered or indoors, and if a drum has been outside for a full season, inspect the outer layer before you pull it into a run.</p>
      <p>Cold matters too. Below freezing, insulation is stiffer and less tolerant of sharp bends. If cable has been stored at low temperature, let it come back toward ambient before pulling, or handle it with a larger bend radius.</p>

      <h2>Bend radius and pulling tension</h2>
      <p>Two numbers prevent most mechanical damage:</p>
      <table>
        <thead>
          <tr><th>Situation</th><th>Rule of thumb</th></tr>
        </thead>
        <tbody>
          <tr><td>Fixed, installed bend</td><td>About 4× the overall cable diameter</td></tr>
          <tr><td>During pulling</td><td>About 15× the overall diameter, never a kink</td></tr>
          <tr><td>Pulling tension</td><td>Pull the conductor, not the jacket; use a swivel and never yank a stalled run</td></tr>
        </tbody>
      </table>
      <p>A kink is permanent. Even if the cable looks straight afterwards, the conductor and insulation at that point have been deformed, and it will be the first place to fail under thermal cycling.</p>

      <h2>Seal every cut end</h2>
      <p>An open end is a wick. Moisture travels along the strands by capillary action and shows up much later as corrosion at a termination metres away. Tape or heat-shrink every cut end, including offcuts returned to store, and never leave a partially used drum with the end hanging in a puddle.</p>

      <h2>On an active site</h2>
      <p>Once installation starts, the risks change: machinery traffic, sharp tray edges, hot work, and cable left lying where the next trade will walk on it. Route runs off the floor as soon as they are pulled, protect edges at every transition, and keep connectors in their packaging until the moment they are mated.</p>

      <div class="tip-box">
        <p><strong>Inspect before you pull, not after.</strong> A two-minute walk along a drum before installation catches jacket damage while it is still the supplier's problem. After the cable is in the tray, it is yours.</p>
      </div>

      <h2>Ordering for less handling</h2>
      <p>Drum lengths that match your runs mean fewer joints, less offcut and less handling — which is where most damage happens. Send us the run list and we will propose drum lengths, with PV1-F or H1Z2Z2-K to the sizes you need, MOQ 1 km per colour and 7–15 day standard lead time.</p>
    """,
)

# --------------------------------------------------------------------------
# Credibility fixes
# --------------------------------------------------------------------------
ABOUT_SUBS = [
    ("Founded in 2009, we have grown", "Founded in 2004, we have grown"),
    ('<div class="number">15+</div><div class="label">Years Experience</div>',
     '<div class="number">20+</div><div class="label">Years Experience</div>'),
]

FACTORY_SUBS = [
    ("Direct from our Xi'an factory. No middlemen.",
     "Direct from our own factory. No middlemen."),
    ("Direct from our Xi'an factory. MOQ 1km per colour and specification.",
     "Direct from our own factory. MOQ 1km per colour and specification."),
]

FACTORY_PAGES = ["pv1-f-solar-cable.html", "solar-cable-ac.html",
                 "solar-cable-combiner.html", "solar-cable-storage.html"]

HEAD_FIELDS = [
    (r"(<meta property=\"og:title\" content=\").*?(\">)", "title"),
    (r"(<meta property=\"og:description\" content=\").*?(\">)", "desc"),
    (r"(<meta name=\"twitter:title\" content=\").*?(\">)", "title"),
    (r"(<meta name=\"twitter:description\" content=\").*?(\">)", "desc"),
    (r"(\"headline\": \").*?(\")", "h1"),
]


def rewrite_article(s, spec):
    m = re.search(r"(?is)(<article class=\"blog-content\">)(.*?)(</article>)", s)
    if not m:
        return s, False
    body = spec["body"]
    inner = "\n  <div class=\"container\">\n" + MARK + "\n" + body + "\n  </div>\n"
    s = s[:m.start(2)] + inner + s[m.end(2):]

    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % spec["title"],
               s, count=1, flags=re.S)
    s = re.sub(r"(?is)(<h1[^>]*>).*?(</h1>)",
               lambda mm: mm.group(1) + spec["h1"] + mm.group(2), s, count=1)
    s = re.sub(r"(<meta name=\"description\" content=\").*?(\">)",
               lambda mm: mm.group(1) + spec["desc"] + mm.group(2), s, count=1)
    for pat, key in HEAD_FIELDS:
        s = re.sub(pat, lambda mm: mm.group(1) + spec[key] + mm.group(2),
                   s, count=1)
    return s, True


def main():
    root = pathlib.Path(".")
    stats = {"articles_rewritten": 0, "about_fixed": 0,
             "factory_wording_fixed": 0, "files_written": 0, "missing": 0}

    for name, spec in ARTICLES.items():
        p = root / name
        if not p.exists():
            print("MISSING", name)
            stats["missing"] += 1
            continue
        s = orig = p.read_text(encoding="utf-8", errors="replace")
        if MARK not in s:
            s, ok = rewrite_article(s, spec)
            if ok:
                stats["articles_rewritten"] += 1
        if s != orig:
            p.write_text(s, encoding="utf-8", newline="")
            stats["files_written"] += 1

    about = root / "about.html"
    if about.exists():
        s = orig = about.read_text(encoding="utf-8", errors="replace")
        for a, b in ABOUT_SUBS:
            if a in s:
                s = s.replace(a, b)
                stats["about_fixed"] += 1
        if s != orig:
            about.write_text(s, encoding="utf-8", newline="")
            stats["files_written"] += 1

    for name in FACTORY_PAGES:
        p = root / name
        if not p.exists():
            continue
        s = orig = p.read_text(encoding="utf-8", errors="replace")
        for a, b in FACTORY_SUBS:
            if a in s:
                n = s.count(a)
                s = s.replace(a, b)
                stats["factory_wording_fixed"] += n
        if s != orig:
            p.write_text(s, encoding="utf-8", newline="")
            stats["files_written"] += 1

    for k in sorted(stats):
        print("%-24s %d" % (k, stats[k]))

    # post-checks
    import hashlib
    bodies = {}
    for name in ARTICLES:
        p = root / name
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"(?is)<article class=\"blog-content\">(.*?)</article>", s)
        raw = re.sub(r"(?is)<[^>]+>", " ", m.group(1)) if m else ""
        words = len(raw.split())
        bodies.setdefault(hashlib.md5(raw.encode()).hexdigest(), []).append(name)
        print("  %-52s %4d words  mark=%s" % (name, words, MARK in s))
    dup = [v for v in bodies.values() if len(v) > 1]
    print("duplicate bodies among the ten:", len(dup))


if __name__ == "__main__":
    main()
